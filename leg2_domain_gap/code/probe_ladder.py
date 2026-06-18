#!/usr/bin/env python3
"""Leg-2 TABULA side — the legibility probe ladder on deepstrain's tone-count code.

Run with the sklearn venv (curvature):
    /Users/sumit/Github/SpaceTime/curvature/.venv/bin/python probe_ladder.py

BRIDGE code. Reads ONLY the `(code, label)` arrays written by extract_codes.py
(`results/codes_*.npz`). It never imports deepstrain, never sees a waveform -- the
§2 blindness boundary, as in leg 1.

Tabula's probe ladder (writeups/legibility_law.md):
  linear decode  = legibility   (here: logistic / ridge, 5-fold CV)
  nonlinear decode = info present (here: kNN)
  scramble signature = linear LOW, nonlinear HIGH.

For each checkpoint we measure, on the INVARIANT (tone label) and the SHORTCUT (loudness):
  within-SIM, within-REAL, and CROSS (fit SIM -> test REAL) legibility.
Transfer axis T_real = the model's own real-noise AUC (logit_real vs y_real).
Then evaluate the frozen predictions P1-P4 (PREREGISTRATION §4).
"""
import json
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import r2_score, roc_auc_score
from sklearn.model_selection import cross_val_predict
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.preprocessing import StandardScaler

RESULTS = Path(__file__).resolve().parent.parent / "results"
CKPTS = ["11_tonecount", "11_tonecount_norm", "11_tonecount_realnoise", "11_tonecount_matched"]
KNN_K = 25


def auc(y, score):
    return roc_auc_score(y, score) if len(np.unique(y)) > 1 else float("nan")


def linear_auc_within(C, y):
    """5-fold CV logistic AUC -- linear legibility of a binary label within one dist."""
    sc = StandardScaler().fit_transform(C)
    p = cross_val_predict(LogisticRegression(max_iter=2000), sc, y, cv=5,
                          method="decision_function")
    return auc(y, p)


def knn_auc_within(C, y):
    sc = StandardScaler().fit_transform(C)
    p = cross_val_predict(KNeighborsClassifier(KNN_K), sc, y, cv=5, method="predict_proba")[:, 1]
    return auc(y, p)


def cross_auc(Ctr, ytr, Cte, yte, knn=False):
    """Fit on one distribution, score the other -- does the legible axis survive the shift?"""
    scaler = StandardScaler().fit(Ctr)
    Xtr, Xte = scaler.transform(Ctr), scaler.transform(Cte)
    if knn:
        m = KNeighborsClassifier(KNN_K).fit(Xtr, ytr)
        return auc(yte, m.predict_proba(Xte)[:, 1])
    m = LogisticRegression(max_iter=2000).fit(Xtr, ytr)
    return auc(yte, m.decision_function(Xte))


def ridge_r2_cross(Ctr, ttr, Cte, tte):
    scaler = StandardScaler().fit(Ctr)
    m = Ridge().fit(scaler.transform(Ctr), ttr)
    return r2_score(tte, m.predict(scaler.transform(Cte)))


def ridge_r2_within(C, t):
    sc = StandardScaler().fit_transform(C)
    return r2_score(t, cross_val_predict(Ridge(), sc, t, cv=5))


# --- ADDED 2026-06-18 (provenance fix): the continuous overtone-SNR faithfulness check.
# The FINDINGS "linear >= kNN on continuous overtone-SNR" numbers were originally produced
# by an exploratory script that was not committed. This reproduces them from the saved
# `osnr_real` arrays so the table is reproducible from code/ alone. Linear = Ridge,
# nonlinear = kNN regressor, both 5-fold CV R^2 within the REAL distribution.
def knn_r2_within(C, t):
    sc = StandardScaler().fit_transform(C)
    return r2_score(t, cross_val_predict(KNeighborsRegressor(KNN_K), sc, t, cv=5))


def main():
    rows = {}
    for ck in CKPTS:
        f = RESULTS / f"codes_{ck}.npz"
        if not f.exists():
            continue
        d = np.load(f)
        Cs, ys, Cr, yr = d["code_sim"], d["y_sim"], d["code_real"], d["y_real"]
        T_real = auc(yr, d["logit_real"])          # transfer axis: model's own real-noise AUC
        T_sim = auc(ys, d["logit_sim"])
        r = {
            "T_real": T_real, "T_sim": T_sim,
            "L_inv_sim": linear_auc_within(Cs, ys),
            "L_inv_real": linear_auc_within(Cr, yr),
            "N_inv_real": knn_auc_within(Cr, yr),
            "L_inv_cross": cross_auc(Cs, ys, Cr, yr),          # fit SIM, test REAL (linear)
            "N_inv_cross": cross_auc(Cs, ys, Cr, yr, knn=True),
            "L_loud_real": ridge_r2_within(Cr, d["loud_real"]),   # shortcut legibility (REAL)
            "L_loud_cross": ridge_r2_cross(Cs, d["loud_sim"], Cr, d["loud_real"]),
            # continuous overtone-SNR faithfulness check (REAL): linear vs nonlinear R^2
            "L_osnr_real": ridge_r2_within(Cr, d["osnr_real"]),
            "N_osnr_real": knn_r2_within(Cr, d["osnr_real"]),
        }
        r["scramble_gap"] = r["N_inv_real"] - r["L_inv_cross"]    # P2: linear-low/nonlinear-high
        rows[ck] = r

    # ---- frozen predictions (PREREGISTRATION §4) ----
    cks = list(rows)
    P1 = all(rows[c]["N_inv_real"] > 0.7 for c in cks)
    early = [c for c in cks if c in
             ("11_tonecount", "11_tonecount_norm", "11_tonecount_realnoise")]
    P2 = all(rows[c]["scramble_gap"] >= 0.20 for c in early)
    Lcross = [rows[c]["L_inv_cross"] for c in cks]
    Tr = [rows[c]["T_real"] for c in cks]
    rho = spearmanr(Lcross, Tr).statistic if len(cks) > 2 else float("nan")
    P3 = (not np.isnan(rho)) and rho >= 0.8
    P4 = all(rows[c]["L_loud_cross"] > rows[c]["L_inv_cross"]
             for c in ("11_tonecount", "11_tonecount_norm") if c in rows)

    print(f"{'checkpoint':26s}{'T_real':>8s}{'L_inv_sim':>11s}{'L_inv_cross':>12s}"
          f"{'N_inv_real':>11s}{'scramble':>10s}{'L_loud_x':>10s}")
    for c in cks:
        r = rows[c]
        print(f"{c:26s}{r['T_real']:8.3f}{r['L_inv_sim']:11.3f}{r['L_inv_cross']:12.3f}"
              f"{r['N_inv_real']:11.3f}{r['scramble_gap']:10.3f}{r['L_loud_cross']:10.3f}")
    print("\ncontinuous overtone-SNR decode (REAL), linear R2 / kNN R2:")
    for c in cks:
        r = rows[c]
        print(f"  {c:26s} {r['L_osnr_real']:.3f} / {r['N_osnr_real']:.3f}")
    print(f"\nP1 invariant-info-present (N_inv_real>0.7 all): {P1}")
    print(f"P2 scramble signature on non-transferring (gap>=0.20): {P2}")
    print(f"P3 legibility tracks transfer (Spearman L_inv_cross vs T_real >=0.8): "
          f"{P3}  (rho={rho:.3f})")
    print(f"P4 shortcut beats invariant early (L_loud_cross>L_inv_cross): {P4}")

    (RESULTS / "probe_ladder.json").write_text(
        json.dumps({"rows": rows, "P1": P1, "P2": P2, "P3": P3, "P4": P4,
                    "rho_Lcross_Treal": rho}, indent=1, default=float))
    print(f"\nwrote {RESULTS / 'probe_ladder.json'}")


if __name__ == "__main__":
    main()

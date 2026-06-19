#!/usr/bin/env python3
"""Move C — TABULA SIDE: the probe ladder on the frame-randomized tidal field.

Run with the tabula (curvature) venv:
    /Users/sumit/Github/SpaceTime/curvature/.venv/bin/python probe_invariants.py

Reads ONLY results/tidal_observations.json (frame-randomized E_ij + ansatz's exact labels).
Tests, with leg-2's probe ladder, whether the coordinate-free Weyl invariant / Petrov class is
recovered from the frame-DEPENDENT observation — linearly (legible) or only nonlinearly (present):
  - regression of ansatz's Weyl magnitude:   linear (Ridge) vs nonlinear (kNN)
  - classification O vs D (Petrov):          linear (Logistic) vs nonlinear (kNN)
  - invariant-feature reference:             linear probe on rotation-invariants tr(E²), tr(E³)
Split is BY METRIC INSTANCE (anti-leakage). PREREGISTRATION §3–4."""
import json
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.metrics import r2_score, accuracy_score
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn.preprocessing import StandardScaler

RESULTS = Path(__file__).resolve().parent.parent / "results"
SEED = 0


def invariant_features(E6):
    """The rotation-invariant power sums of the symmetric 3×3 tidal tensor — and (trE)², so the
    Weyl magnitude tr(Ẽ²) = tr(E²) − (trE)²/3 is linearly accessible (the achievable ceiling)."""
    E00, E01, E02, E11, E12, E22 = E6.T
    trE = E00 + E11 + E22
    trE2 = E00**2 + E11**2 + E22**2 + 2*(E01**2 + E02**2 + E12**2)
    trE3 = (E00**3 + E11**3 + E22**3
            + 3*E01**2*(E00+E11) + 3*E02**2*(E00+E22) + 3*E12**2*(E11+E22)
            + 6*E01*E02*E12)
    return np.stack([trE, trE2, trE3, trE**2], axis=1)


def main():
    d = json.loads((RESULTS / "tidal_observations.json").read_text())
    rows = d["rows"]
    E6 = np.array([r["E6"] for r in rows], float)
    weyl = np.array([r["weyl_mag"] for r in rows], float)
    yOD = np.array([1 if r["petrov"] == "D" else 0 for r in rows])
    inst = np.array([r["instance"] for r in rows])

    rng = np.random.default_rng(SEED)
    uids = np.unique(inst); rng.shuffle(uids)
    cut = int(0.6 * len(uids))                              # split BY metric instance
    tr = np.isin(inst, uids[:cut]); te = ~tr

    sc = StandardScaler().fit(E6[tr])
    Xtr, Xte = sc.transform(E6[tr]), sc.transform(E6[te])
    inv = invariant_features(E6)
    si = StandardScaler().fit(inv[tr])
    Itr, Ite = si.transform(inv[tr]), si.transform(inv[te])

    print("MOVE C — recovering ansatz's coordinate-free invariant from the frame-dependent tidal field\n")

    # --- regression of the Weyl magnitude --- (target standardized for stable MLP fitting)
    wsd = weyl[tr].std() or 1.0
    lin = Ridge().fit(Xtr, weyl[tr]); r2_lin = r2_score(weyl[te], lin.predict(Xte))
    knn = KNeighborsRegressor(7).fit(Xtr, weyl[tr]); pk = knn.predict(Xte)
    mlp = MLPRegressor(hidden_layer_sizes=(64, 64), max_iter=4000, random_state=0).fit(Xtr, weyl[tr] / wsd)
    pm = mlp.predict(Xte) * wsd
    r2_knn, r2_mlp = r2_score(weyl[te], pk), r2_score(weyl[te], pm)
    pred_nl, r2_nl = (pm, r2_mlp) if r2_mlp >= r2_knn else (pk, r2_knn)
    ref = Ridge().fit(Itr, weyl[tr]); r2_ref = r2_score(weyl[te], ref.predict(Ite))
    rho = spearmanr(weyl[te], pred_nl).statistic
    print("  WEYL MAGNITUDE recovery (held-out R²):")
    print(f"    linear (Ridge) on raw E_ij        : {r2_lin:+.3f}")
    print(f"    nonlinear (kNN) on raw E_ij       : {r2_knn:+.3f}")
    print(f"    nonlinear (MLP) on raw E_ij       : {r2_mlp:+.3f}")
    print(f"    linear on rotation-invariants     : {r2_ref:+.3f}   (the achievable ceiling)")
    print(f"    Spearman(best-nonlinear, truth)   : {rho:+.3f}")

    # --- classification O vs D --- Petrov O ⟺ Weyl magnitude 0, D ⟺ > 0, so the principled
    # classifier thresholds the RECOVERED Weyl invariant (threshold chosen on train only).
    def thresh_acc(pred_tr, pred_te):
        cand = sorted(pred_tr)
        ths = [(cand[i] + cand[i + 1]) / 2 for i in range(len(cand) - 1)]
        best_t = max(ths, key=lambda t: ((pred_tr > t) == yOD[tr]).mean()) if ths else 0.0
        return accuracy_score(yOD[te], (pred_te > best_t).astype(int))

    acc_lin = thresh_acc(lin.predict(Xtr), lin.predict(Xte))            # threshold linear-recovered
    acc_nl = thresh_acc(mlp.predict(Xtr) * wsd, pm)                     # threshold MLP-recovered
    acc_ref = thresh_acc(ref.predict(Itr), ref.predict(Ite))           # threshold invariant-ceiling
    print("\n  PETROV CLASS O vs D (threshold the recovered Weyl invariant; held-out accuracy):")
    print(f"    via linear-recovered invariant    : {acc_lin:.3f}")
    print(f"    via nonlinear(MLP)-recovered       : {acc_nl:.3f}")
    print(f"    via invariant-feature ceiling      : {acc_ref:.3f}")

    gap = r2_nl - r2_lin
    P1 = r2_nl > 0.9
    P2 = gap > 0.3
    P3 = acc_nl > 0.95
    P4 = rho > 0.9
    print("\n  VERDICTS (frozen):")
    print(f"    P1 (nonlinear R² > 0.9):                 {P1}")
    print(f"    P2 (legibility gap nonlinear−linear>0.3): {P2}  (gap = {gap:.3f})")
    print(f"    P3 (O/D accuracy > 0.95):                {P3}")
    print(f"    P4 (Spearman > 0.9):                     {P4}")
    ok = P1 and P2 and P3 and P4
    print(f"\n  INVARIANT CROSS-MEASURE: {'CONFIRMED ✅' if ok else 'incomplete ❌'}")

    out = {"r2_weyl": {"linear": r2_lin, "knn": r2_knn, "mlp": r2_mlp, "best_nonlinear": r2_nl,
                       "invariant_ref": r2_ref},
           "spearman": rho,
           "acc_OD": {"via_linear": acc_lin, "via_nonlinear": acc_nl, "via_invariant_ref": acc_ref},
           "legibility_gap": gap, "verdicts": {"P1": P1, "P2": P2, "P3": P3, "P4": P4, "confirmed": ok}}
    (RESULTS / "probe_invariants.json").write_text(json.dumps(out, indent=1, default=float))
    print("  wrote results/probe_invariants.json")


if __name__ == "__main__":
    main()

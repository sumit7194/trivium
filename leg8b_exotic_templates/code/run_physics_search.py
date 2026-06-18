#!/usr/bin/env python3
"""run_physics_search.py

1. Calibrates raw-to-whitened amplitude for physics-grounded templates.
2. Runs the fair head-to-head sensitivity sweeps (ML scorer vs raw comb) on the physics templates.
3. Performs the on-source search on GW150914 post-merger data.
4. Saves all results to results/leg8b_echo_results.json.
"""

import importlib.util
import json
import os
import sys
from pathlib import Path
import numpy as np
import torch

# Add deepstrain's script path to import echolib and v4/v5 code
ECHO_SCRIPTS = Path("/Users/sumit/Github/BlackHole/echoes/scripts")
sys.path.insert(0, str(ECHO_SCRIPTS))

import echolib
from echolib import BAND, DETECTORS, GW150914_DT_PRED, RESULTS, comb_on_env, comb_score, fetch_block, progress

# Import ConvAE from Step 07
spec7 = importlib.util.spec_from_file_location("ml", ECHO_SCRIPTS / "07_ml_scorer.py")
ml = importlib.util.module_from_spec(spec7)
spec7.loader.exec_module(ml)

# Import physics-grounded template generator
sys.path.insert(0, str(Path(__file__).resolve().parent))
from physics_grounded_template import generate_physics_grounded_template

# Parameters matching Step 10
FS = 4096.0
SEG = 3.0
A_REF = 2.0e-21
N_CAL = 8
N_BG = 30
N_TRIALS = 25
AMPS = (0.5, 1.0, 1.5, 2.0, 3.0)

rng = np.random.default_rng(53)


def make_physics_injector(t_seg0, amp, dt, fs):
    n_seg = int(SEG * fs)
    psi = generate_physics_grounded_template(n_seg, fs, dt, amp=amp, f0=250.0, tau=0.02, gamma=0.7, n_echoes=6, t_first=0.1, f_width=40.0)
    
    def injector(times):
        out = np.zeros_like(times)
        t0 = times[0]
        i_start = int(round((t_seg0 - t0) * fs))
        out[i_start : i_start + n_seg] = psi
        return out
        
    return injector


def whitened_segment(raw, center, inj=None):
    """64-s raw slice around center (+ optional injection) -> standard 3-s
    whitened+bandpassed segment starting at center+0.05."""
    sl = raw.crop(center - 30, center + 34)
    if inj is not None:
        sl = sl.copy()
        sl.value[:] = sl.value + inj(sl.times.value)
    w = sl.whiten(4, 2).bandpass(*BAND)
    seg = w.crop(center + 0.05, center + 0.05 + SEG + 0.01).value[: int(SEG * FS)]
    return seg


def main() -> None:
    print("RUNNING LEG 8b: PHYSICS-GROUNDED ECHO SEARCH")
    
    # 1. Load raw strain blocks
    print("Loading H1 and L1 raw strain blocks...")
    raws = {det: fetch_block(det, "GW150914") for det in DETECTORS}
    t0 = float(raws["H1"].t0.value)
    centers = t0 + 308 + 4 * np.arange(45)  # eval-time region, 4-s spacing
    dt_grid = np.arange(0.05, 0.5, 0.005)
    j_pred = int(np.argmin(np.abs(dt_grid - GW150914_DT_PRED)))
    
    # 2. Load saved ML scorers
    print("Loading saved ML scorers...")
    models = {}
    for det in DETECTORS:
        m = ml.ConvAE()
        m.load_state_dict(torch.load(RESULTS / f"07_scorer_{det}.pt", weights_only=True))
        m.eval()
        models[det] = m
        
    # 3. Calibration (X0) by differencing
    print("\nCalibrating raw-to-whitened amplitude for physics templates (differenced)...")
    slopes = {}
    for det in DETECTORS:
        amps_w = []
        for i in range(N_CAL):
            c = float(centers[rng.integers(0, len(centers))])
            inj = make_physics_injector(c + 0.05, A_REF, GW150914_DT_PRED, FS)
            seg_inj = whitened_segment(raws[det], c, inj)
            seg_cln = whitened_segment(raws[det], c)
            diff = seg_inj - seg_cln
            i0 = int((0.1 + GW150914_DT_PRED - 0.05) * FS)
            i1 = int((0.1 + GW150914_DT_PRED + 0.05) * FS)
            amps_w.append(np.max(np.abs(diff[i0:i1])))
        slopes[det] = float(np.median(amps_w)) / A_REF
        print(f"  Calib {det}: whitened SIGNAL amp at A_ref={A_REF:.1e} -> median "
              f"{np.median(amps_w):.2f} (slope: {slopes[det]:.2e})")
    slope = float(np.mean(list(slopes.values())))
    print(f"  Mean calibration slope: {slope:.2e}")
    
    # 4. Background scoring
    print(f"\nComputing background scores (n={N_BG}) for both statistics...")
    def both_scores(c, inj=None):
        tot_ml = np.zeros(len(dt_grid))
        tot_cb = np.zeros(len(dt_grid))
        for det in DETECTORS:
            seg = whitened_segment(raws[det], c, inj)
            tot_ml += comb_on_env(ml.error_envelope(models[det], seg, FS), FS, dt_grid)
            tot_cb += comb_score(seg, FS, dt_grid)
        return float(tot_ml[j_pred]), float(tot_cb[j_pred])

    bg_ml, bg_cb = [], []
    for i in range(N_BG):
        c = float(centers[i % len(centers)])
        a, b = both_scores(c)
        bg_ml.append(a)
        bg_cb.append(b)
        progress("leg8b_bg", i, N_BG)
        
    th_ml = float(np.quantile(bg_ml, 0.95))
    th_cb = float(np.quantile(bg_cb, 0.95))
    print(f"  Background 95th pct thresholds: ML = {th_ml:.3f}, comb = {th_cb:.3f}")
    
    # 5. Injection sweeps (Y2)
    print("\nRunning injection-recovery sensitivity sweeps...")
    eff = {"ml": {}, "comb": {}}
    for amp in AMPS:
        A = amp / slope
        h_ml = h_cb = 0
        for i in range(N_TRIALS):
            c = float(centers[rng.integers(0, len(centers))])
            inj = make_physics_injector(c + 0.05, A, GW150914_DT_PRED, FS)
            a, b = both_scores(c, inj)
            h_ml += a > th_ml
            h_cb += b > th_cb
            progress(f"leg8b_inj_{amp}", i, N_TRIALS)
        eff["ml"][amp] = h_ml / N_TRIALS
        eff["comb"][amp] = h_cb / N_TRIALS
        print(f"  {amp:.1f} sigma-equiv: ML {100*eff['ml'][amp]:3.0f}%   "
              f"comb {100*eff['comb'][amp]:3.0f}%")
              
    # 6. On-source search
    print("\nPerforming on-source search on GW150914...")
    gps_merger = echolib.event_gps("GW150914")
    on_ml, on_cb = both_scores(gps_merger)
    p_ml = (np.sum(np.array(bg_ml) >= on_ml) + 1) / (N_BG + 1)
    p_cb = (np.sum(np.array(bg_cb) >= on_cb) + 1) / (N_BG + 1)
    print(f"  On-source scores: ML = {on_ml:.3f} (p = {p_ml:.3f}), comb = {on_cb:.3f} (p = {p_cb:.3f})")
    
    # Save results
    os.makedirs("/Users/sumit/Github/TheBridge/results", exist_ok=True)
    out_file = Path("/Users/sumit/Github/TheBridge/results/leg8b_echo_results.json")
    results = {
        "slopes": slopes,
        "mean_slope": slope,
        "thresholds": {"ml": th_ml, "comb": th_cb},
        "recovery": {
            "amps": list(AMPS),
            "ml": [eff["ml"][a] for a in AMPS],
            "comb": [eff["comb"][a] for a in AMPS]
        },
        "on_source": {
            "ml_score": on_ml, "ml_p": p_ml,
            "comb_score": on_cb, "comb_p": p_cb
        }
    }
    out_file.write_text(json.dumps(results, indent=2))
    print(f"\nSaved search results to {out_file} ✅")
    
    # Optional best-effort mirror to a local agent "brain" dir, only if it already exists.
    brain_root = Path("/Users/sumit/.gemini/antigravity/brain")
    brain_dir = brain_root / "6d8c4aa5-66fc-4580-85dc-cd0e4dc34fa1"
    if brain_root.exists():
        brain_dir.mkdir(parents=True, exist_ok=True)
    import shutil
    if brain_root.exists():
        shutil.copy(out_file, brain_dir / "leg8b_echo_results.json")


if __name__ == "__main__":
    main()

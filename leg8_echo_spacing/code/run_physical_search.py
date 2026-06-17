#!/usr/bin/env python3
"""run_physical_search.py

Runs the network comb statistic on real GW150914 data at spacings derived from 
the physical wormhole parameter space lambda. Sweeps lambda from the Planck scale 
to macroscopic limits.
"""

import os
import sys
import json
from pathlib import Path
import numpy as np

# Add deepstrain's echoes script path to import echolib
ECHOES_SCRIPTS = Path("/Users/sumit/Github/BlackHole/echoes/scripts")
sys.path.insert(0, str(ECHOES_SCRIPTS))

from echolib import DETECTORS, comb_score, load_segments

# Conversion factor
M_SUN_SECONDS = 4.925490947641267e-06

def analytical_integral(u, lam):
    """Analytical antiderivative of (1+u^2) / sqrt(u^2*(1+lambda^2) + lambda^2)."""
    c = np.sqrt(1 + lam**2)
    term1 = (1.0 / c - lam**2 / (2.0 * c**3)) * np.log(c * u + np.sqrt(c**2 * u**2 + lam**2))
    term2 = (u / (2.0 * c**2)) * np.sqrt(c**2 * u**2 + lam**2)
    return term1 + term2

def compute_delta_t_exact(mass, lam, epsilon, spin=0.0):
    """Compute exact round-trip travel time delta_t [seconds] for given mass, lambda, epsilon, and spin."""
    M_sec = mass * M_SUN_SECONDS
    u_lower = np.sqrt(epsilon)
    u_upper = np.sqrt((1 - 2 * lam**2) / (2 * (1 + lam**2)))
    
    # Check if lambda is too large for the photon sphere to exist outside the throat
    # The photon sphere r_ph = 3M / (1+lambda^2) must be greater than the throat r_throat = 2M(1+epsilon)
    # i.e., 3 / (1+lambda^2) > 2(1+epsilon) => 1+lambda^2 < 1.5 / (1+epsilon)
    # If not, the integral is not well-defined.
    if 1 + lam**2 >= 1.5 / (1.0 + epsilon):
        return 0.0
        
    val = analytical_integral(u_upper, lam) - analytical_integral(u_lower, lam)
    dt_static = 8 * M_sec * val
    
    if spin == 0.0:
        return dt_static
    else:
        h = np.sqrt(1 - spin**2)
        k_factor = (1 + h) / (2.0 * h)
        return dt_static * k_factor

def run_search():
    EVENT = "GW150914"
    mass = 68.0
    spin = 0.69
    
    print(f"Loading GW150914 segments...")
    all_segs = {det: load_segments(EVENT, det) for det in DETECTORS}
    fs = all_segs["H1"].fs
    n_off = min(len(all_segs[d].off) for d in DETECTORS)
    print(f"Loaded {n_off} background segment pairs.")
    
    on = {det: all_segs[det].on for det in DETECTORS}
    
    # We define physical lambda grids
    # Planckian cutoff: epsilon = 1e-38, lambda down to 1e-21 (where dt_rot ≈ 0.28 s)
    lambdas_planck = np.logspace(-21, -1, 41)
    # Macroscopic cutoff: epsilon = 1e-10, lambda down to 1e-15 (where dt_rot ≈ 0.036 s)
    lambdas_macro = np.logspace(-15, -1, 29)
    
    results = {
        "mass": mass,
        "spin": spin,
        "n_background_segments": n_off,
        "planckian": {"static": [], "rotating": []},
        "macroscopic": {"static": [], "rotating": []}
    }
    
    # Helper to run sweep
    def run_sweep(epsilon, lambdas, spin_val):
        on_scores = []
        p_values = []
        dts = []
        
        # Calculate background scores first to get distributions for each lambda
        bg_scores_all_lams = []
        
        # 1. Compute spacing for all lambdas
        valid_lambdas = []
        for lam in lambdas:
            dt = compute_delta_t_exact(mass, lam, epsilon, spin_val)
            if dt > 0.0:
                dts.append(dt)
                valid_lambdas.append(lam)
        
        # Convert valid_lambdas back to array
        valid_lambdas = np.array(valid_lambdas)
        dts = np.array(dts)
        
        # 2. Compute background scores
        print(f"  Computing background scores for epsilon={epsilon:.1e}, spin={spin_val}...")
        bg_scores = np.zeros((n_off, len(valid_lambdas)))
        for i in range(n_off):
            pair = {det: all_segs[det].off[i] for det in DETECTORS}
            total = np.zeros(len(valid_lambdas))
            for det in DETECTORS:
                total += comb_score(pair[det], fs, dts)
            bg_scores[i] = total
            
        # 3. Compute on-source scores and p-values
        print(f"  Computing on-source scores...")
        on_total = np.zeros(len(valid_lambdas))
        for det in DETECTORS:
            on_total += comb_score(on[det], fs, dts)
            
        for j, lam in enumerate(valid_lambdas):
            on_s = float(on_total[j])
            bg_s = bg_scores[:, j]
            p_val = float((np.sum(bg_s >= on_s) + 1) / (n_off + 1))
            
            on_scores.append(on_s)
            p_values.append(p_val)
            
        return {
            "lambdas": valid_lambdas.tolist(),
            "spacings": dts.tolist(),
            "on_scores": on_scores,
            "p_values": p_values
        }
        
    print("\nRunning Planckian cutoff sweeps...")
    results["planckian"]["static"] = run_sweep(1e-38, lambdas_planck, 0.0)
    results["planckian"]["rotating"] = run_sweep(1e-38, lambdas_planck, spin)
    
    print("\nRunning Macroscopic cutoff sweeps...")
    results["macroscopic"]["static"] = run_sweep(1e-10, lambdas_macro, 0.0)
    results["macroscopic"]["rotating"] = run_sweep(1e-10, lambdas_macro, spin)
    
    # Save results
    results_dir = Path("/Users/sumit/Github/TheBridge/results")
    results_dir.mkdir(exist_ok=True)
    out_file = results_dir / "leg8_echo_spacing.json"
    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved search results to {out_file} ✅")

if __name__ == "__main__":
    run_search()

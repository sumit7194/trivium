#!/usr/bin/env python3
"""Leg 7 — Ringdown Intrinsic Dimension: dataset generation.

Generates three ringdown datasets (locked Kerr, free-overtone Kerr, noise-injected)
to probe their intrinsic degrees of freedom.
"""

import os
import sys
import numpy as np

# Insert BlackHole scripts path to import rdlib
sys.path.insert(0, "/Users/sumit/Github/BlackHole/ringdown_spectroscopy/scripts")
import rdlib

FS = 4096.0
SEG = 0.04
N_SAMP = int(SEG * FS)
N_SAMP += N_SAMP % 2  # 164 samples
N_TRAIN = 8000
DEV = "cpu"

kerr220 = rdlib.KerrMap(2, 2, 0)
kerr221 = rdlib.KerrMap(2, 2, 1)

CHI_GRID = np.linspace(0.01, 0.97, 200)
W220 = np.array([kerr220.f_tau(1.0, c) for c in CHI_GRID])
W221 = np.array([kerr221.f_tau(1.0, c) for c in CHI_GRID])


def get_freq_tau(mass, chi):
    i = np.searchsorted(CHI_GRID, chi)
    i = min(max(i, 0), len(CHI_GRID) - 1)
    f1, tau1 = W220[i][0] / mass, W220[i][1] * mass
    f2, tau2 = W221[i][0] / mass, W221[i][1] * mass
    return f1, tau1, f2, tau2


def make_datasets():
    rng = np.random.default_rng(42)
    os.makedirs("results", exist_ok=True)
    
    # Draw mass and spin parameters
    masses = rng.uniform(40, 120, N_TRAIN)
    chis = rng.uniform(0.05, 0.95, N_TRAIN)
    
    t = np.arange(N_SAMP) / FS
    t0 = 0.0
    
    # --- Family 1: Kerr Locked (2D manifold) ---
    print("Generating Family 1 (Kerr Locked)...")
    F1 = np.zeros((N_TRAIN, 2 * N_SAMP), dtype=np.float32)
    for k in range(N_TRAIN):
        f1, tau1, f2, tau2 = get_freq_tau(masses[k], chis[k])
        # Locked overtone amplitude and phase
        amp1 = 5.0
        amp2 = 4.0
        params = [
            dict(f=f1, tau=tau1, amp=amp1, phi=0.0),
            dict(f=f2, tau=tau2, amp=amp2, phi=0.0),
        ]
        x1 = rdlib.damped_sinusoids(t, t0, params)
        x2 = rdlib.damped_sinusoids(t, t0, params)
        F1[k] = np.concatenate([x1, x2])
        
    np.savez("results/obs_rd_locked.npz", obs=F1)
    
    # --- Family 2: Kerr Free (4D manifold) ---
    print("Generating Family 2 (Kerr Free)...")
    F2 = np.zeros((N_TRAIN, 2 * N_SAMP), dtype=np.float32)
    for k in range(N_TRAIN):
        f1, tau1, f2, tau2 = get_freq_tau(masses[k], chis[k])
        # Free overtone amplitude ratio and phase difference
        amp1 = 5.0
        amp2 = amp1 * rng.uniform(0.2, 1.5)
        phi2 = rng.uniform(-np.pi, np.pi)
        params = [
            dict(f=f1, tau=tau1, amp=amp1, phi=0.0),
            dict(f=f2, tau=tau2, amp=amp2, phi=phi2),
        ]
        x1 = rdlib.damped_sinusoids(t, t0, params)
        x2 = rdlib.damped_sinusoids(t, t0, params)
        F2[k] = np.concatenate([x1, x2])
        
    np.savez("results/obs_rd_free.npz", obs=F2)
    
    # --- Family 3: LIGO Noise Injected (Family 1 + Gaussian noise) ---
    print("Generating Family 3 (LIGO Noise)...")
    F3 = np.zeros((N_TRAIN, 2 * N_SAMP), dtype=np.float32)
    for k in range(N_TRAIN):
        # We add unit Gaussian noise in the whitened domain
        noise = rng.normal(0, 1, 2 * N_SAMP)
        F3[k] = F1[k] + noise
        
    np.savez("results/obs_rd_noise.npz", obs=F3)
    print("All datasets generated successfully!")


if __name__ == "__main__":
    make_datasets()

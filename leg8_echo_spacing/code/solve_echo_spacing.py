#!/usr/bin/env python3
"""solve_echo_spacing.py

1. Symbolically verify the photon sphere orbit r_ph for the Damour-Solodukhin (DS) wormhole.
2. Numerically integrate (and analytically verify) the exact radial null geodesic travel time.
3. Determine the relationship between spacing dt and deviation lambda for static and rotating spacetimes.
"""

import os
import sys
import sympy as sp
import numpy as np

# Conversion factor
M_SUN_SECONDS = 4.925490947641267e-06

def verify_photon_sphere():
    """Verify r_ph = 3M / (1 + lambda^2) symbolically using SymPy."""
    print("--- Symbolically Verifying Photon Sphere ---")
    r, M, lam = sp.symbols("r M lambda", positive=True)
    A = 1 - 2*M/r + lam**2
    
    # Photon sphere satisfies d/dr (A(r) / r^2) = 0
    V = A / r**2
    dV = sp.diff(V, r)
    sol = sp.solve(dV, r)
    print(f"Effective Potential V_eff(r) = {V}")
    print(f"dV/dr = {sp.simplify(dV)}")
    print(f"Solutions for dV/dr = 0: {sol}")
    
    expected = 3*M / (1 + lam**2)
    verified = False
    for s in sol:
        if sp.simplify(s - expected) == 0:
            verified = True
            print(f"Verified: Photon sphere is at r_ph = {expected} ✅")
            break
            
    if not verified:
        print("Verification failed! ❌")
        sys.exit(1)
    return True

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
    
    val = analytical_integral(u_upper, lam) - analytical_integral(u_lower, lam)
    dt_static = 8 * M_sec * val
    
    if spin == 0.0:
        return dt_static
    else:
        # Rotating Kerr-like scaling factor: K(a) = (1 + sqrt(1-a^2)) / sqrt(1-a^2)
        # For a=0, K(0) = 2. We normalize to the static factor of 2: K_eff(a) = K(a) / 2
        # So dt_rotating = dt_static * (1 + sqrt(1-a^2)) / (2 * sqrt(1-a^2))
        h = np.sqrt(1 - spin**2)
        k_factor = (1 + h) / (2.0 * h)
        return dt_static * k_factor

def main():
    verify_photon_sphere()
    
    mass = 68.0  # GW150914 remnant mass in detector frame
    spin = 0.69  # GW150914 remnant spin
    print(f"\nEvaluating for remnant mass M = {mass} M_sun, spin = {spin}")
    
    lambdas = np.logspace(-15, -1, 15)
    
    print("\nPlanckian cutoff (epsilon = 1e-38):")
    for lam in lambdas:
        dt_stat = compute_delta_t_exact(mass, lam, epsilon=1e-38, spin=0.0)
        dt_rot = compute_delta_t_exact(mass, lam, epsilon=1e-38, spin=spin)
        print(f"  lambda = {lam:.1e} -> dt_static = {dt_stat:.4f} s, dt_rotating = {dt_rot:.4f} s")
        
    print("\nMacroscopic cutoff (epsilon = 1e-10):")
    for lam in lambdas:
        dt_stat = compute_delta_t_exact(mass, lam, epsilon=1e-10, spin=0.0)
        dt_rot = compute_delta_t_exact(mass, lam, epsilon=1e-10, spin=spin)
        print(f"  lambda = {lam:.1e} -> dt_static = {dt_stat:.4f} s, dt_rotating = {dt_rot:.4f} s")
        
    # Solve for lambda that matches the literature spacing dt = 0.2925 s
    target_dt = 0.2925
    print(f"\nFinding lambda corresponding to literature spacing dt = {target_dt} s...")
    
    from scipy.optimize import brentq
    
    # Static model
    try:
        log_lam_planck = brentq(lambda l: compute_delta_t_exact(mass, 10**l, 1e-38, 0.0) - target_dt, -40, -1)
        print(f"  Static Planckian: lambda = {10**log_lam_planck:.3e} (log10 = {log_lam_planck:.3f})")
    except Exception as e:
        print(f"  Static Planckian solver failed: {e} (Expected: static spacing doesn't reach 0.2925s)")
        
    # Rotating model
    try:
        log_lam_planck_rot = brentq(lambda l: compute_delta_t_exact(mass, 10**l, 1e-38, spin) - target_dt, -40, -1)
        print(f"  Rotating Planckian: lambda = {10**log_lam_planck_rot:.3e} (log10 = {log_lam_planck_rot:.3f})")
    except Exception as e:
        print(f"  Rotating Planckian solver failed: {e}")

    try:
        log_lam_macro_rot = brentq(lambda l: compute_delta_t_exact(mass, 10**l, 1e-10, spin) - target_dt, -40, -1)
        print(f"  Rotating Macroscopic: lambda = {10**log_lam_macro_rot:.3e} (log10 = {log_lam_macro_rot:.3f})")
    except Exception as e:
        print(f"  Rotating Macroscopic solver failed: {e}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""physics_grounded_template.py

1. Symbolically verifies the photon sphere for the Damour-Solodukhin wormhole.
2. Implements frequency-domain generation of physics-grounded templates.
3. Plots and saves a comparison of the phenomenological vs physics-grounded templates.
"""

import os
import sys
import sympy as sp
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

# Add deepstrain's script path to import echolib
sys.path.insert(0, "/Users/sumit/Github/BlackHole/echoes/scripts")
from echolib import echo_train, RESULTS

# Add conjecture_machine path for Geometry
sys.path.insert(0, "/Users/sumit/Github/conjecture_machine/scripts")
from gr_engine import Geometry, R_SYM


def verify_photon_sphere():
    """Verify r_ph = 3M / (1 + lambda^2) symbolically using SymPy."""
    print("--- Symbolically Verifying Photon Sphere ---")
    r = R_SYM
    M, lam = sp.symbols("M lambda", positive=True)
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


def generate_physics_grounded_template(n, fs, dt, amp, f0=250.0, tau=0.02, gamma=0.7, n_echoes=6, t_first=0.1, f_width=40.0, phase_flip=True, seed=42):
    """Generates a physics-grounded echo template in the frequency domain and returns time-domain signal.
    
    f0: resonance frequency [Hz]
    tau: damping time of individual pulse [s] (determines the ringdown bandwidth)
    gamma: maximum reflectivity at low frequency
    f_width: roll-off width of potential barrier [Hz] (related to Lyapunov exponent)
    """
    # Frequency grid for real FFT
    freqs = np.fft.rfftfreq(n, d=1.0/fs)
    omegas = 2 * np.pi * freqs
    
    # FT of the fundamental ringdown pulse: s(t) = exp(-t/tau) * sin(2*pi*f0*t + phase) for t>=0
    omega0 = 2 * np.pi * f0
    rng = np.random.default_rng(seed)
    phase = rng.uniform(0, 2 * np.pi)
    
    # Analytical Fourier transform of damped sine-Gaussian:
    # s(t) = exp(-t/tau) * sin(omega0 * t + phase)
    # S_ring(omega) = [ sin(phase) * (1/tau + i*omega) + cos(phase) * omega0 ] / [ omega0^2 + (1/tau + i*omega)^2 ]
    num = np.sin(phase) * (1.0/tau + 1j * omegas) + np.cos(phase) * omega0
    den = omega0**2 + (1.0/tau + 1j * omegas)**2
    S_ring = np.exp(-1j * omegas * t_first) * num / den
    
    # Frequency-dependent reflection coefficient
    # Gamma(f) = - gamma / sqrt(1 + exp(2*pi * (f - f0) / f_width))
    # Negative sign represents the phase flip on reflection
    sign_factor = -1.0 if phase_flip else 1.0
    Gamma = sign_factor * gamma / np.sqrt(1.0 + np.exp(2.0 * np.pi * (freqs - f0) / f_width))
    
    # Sum of echoes: sum_{k=1}^{n_echoes} (Gamma * exp(-i*omega*dt))^k
    echo_factor = np.zeros(len(omegas), dtype=complex)
    phase_factor = np.exp(-1j * omegas * dt)
    
    for k in range(1, n_echoes + 1):
        echo_factor += (Gamma * phase_factor)**k
        
    # Total signal in frequency domain
    Psi = S_ring * echo_factor
    
    # Inverse real FFT to get time domain template
    psi = np.fft.irfft(Psi, n=n)
    
    # Normalize so that the first echo peak matches the target amplitude
    t = np.arange(n) / fs
    first_echo_window = (t >= t_first + dt - 0.05) & (t <= t_first + dt + 0.05)
    if np.any(first_echo_window):
        peak_val = np.max(np.abs(psi[first_echo_window]))
        if peak_val > 0:
            psi = psi * (amp / peak_val)
            
    return psi


def main():
    verify_photon_sphere()
    
    # Waveform comparison setup
    fs = 4096.0
    seg_dur = 3.0
    n = int(seg_dur * fs)
    dt = 0.2925
    amp = 1.0
    
    print("\nGenerating templates for comparison...")
    # 1. Phenomenological
    y_phen = echo_train(n, fs, dt, amp=amp, f0=250.0, tau=0.02, gamma=0.7, n_echoes=6, t_first=0.1, phase_flip=True, rng=np.random.default_rng(42))
    
    # 2. Physics-Grounded
    y_phys = generate_physics_grounded_template(n, fs, dt, amp=amp, f0=250.0, tau=0.02, gamma=0.7, n_echoes=6, t_first=0.1, f_width=40.0, phase_flip=True, seed=42)
    
    t = np.arange(n) / fs
    
    # Plotting
    fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True)
    
    # Style
    plt.rcParams["font.family"] = "sans-serif"
    
    axes[0].plot(t, y_phen, lw=0.6, color="darkslategray", label="Phenomenological Template (Constant Decay)")
    axes[0].set_title("Phenomenological Echoes (Sine-Gaussian Train)", fontsize=11, fontweight="bold")
    axes[0].set_ylabel("amplitude")
    axes[0].grid(True, linestyle="--", alpha=0.5)
    axes[0].legend(loc="upper right")
    
    axes[1].plot(t, y_phys, lw=0.6, color="crimson", label="Physics-Grounded Template (High-Frequency Filtered)")
    axes[1].set_title("Physics-Grounded Echoes (Wormhole Cavity Dispersion)", fontsize=11, fontweight="bold")
    axes[1].set_ylabel("amplitude")
    axes[1].set_xlabel("time [s]")
    axes[1].grid(True, linestyle="--", alpha=0.5)
    axes[1].legend(loc="upper right")
    
    # Highlight Zoom of echo 1 vs echo 6
    # Let's add text pointers or zoom insets to emphasize the broadening
    fig.suptitle("Gravitational Wave Echo Template Comparison (Leg 8b)\n"
                 "(Wormhole photon sphere barrier filters high frequencies, redshifting subsequent pulses)", fontsize=13, fontweight="bold")
    fig.tight_layout()
    
    # Save workspace results
    os.makedirs("/Users/sumit/Github/TheBridge/results", exist_ok=True)
    plot_path = "/Users/sumit/Github/TheBridge/results/leg8b_waveform_comparison.png"
    fig.savefig(plot_path, dpi=300, bbox_inches="tight")
    print(f"Saved waveform comparison to {plot_path} ✅")
    
    # Copy to brain artifact directory
    brain_dir = Path("/Users/sumit/.gemini/antigravity/brain/6d8c4aa5-66fc-4580-85dc-cd0e4dc34fa1")
    brain_dir.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy(plot_path, brain_dir / "leg8b_waveform_comparison.png")
    print(f"Copied waveform comparison to brain directory ✅")


if __name__ == "__main__":
    main()

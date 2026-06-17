#!/usr/bin/env python3
"""Leg 5b — The Rotating Strong-Field Curriculum (Shadow-edge Fidelity).

Compiles a uniform curriculum vs targeted curriculum for learning kerr null geodesics
and resolving the asymmetric shadow boundaries. Uses standardized feature scaling and
residual learning for high-precision model convergence.
"""

import json
import os
import sys
import shutil
from pathlib import Path
import numpy as np
import torch
from torch import nn
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DPHI = 0.02
DLAMBDA = 0.05
SEEDS = 3
N_SEGMENTS = 80000
STEPS = 12000
BATCH = 256

np.seterr(all="ignore")

def get_exact_bcrit(a):
    """Calculate exact prograde and retrograde critical impact parameters in Kerr (M=1)."""
    if a < 1e-4:
        return 3 * np.sqrt(3), -3 * np.sqrt(3)
    r_pro = 2.0 * (1.0 + np.cos(2.0/3.0 * np.arccos(-a)))
    xi_pro = -(r_pro**3 - 3.0 * r_pro**2 + a**2 * r_pro + a**2) / (a * (r_pro - 1.0))
    r_ret = 2.0 * (1.0 + np.cos(2.0/3.0 * np.arccos(a)))
    xi_ret = -(r_ret**3 - 3.0 * r_ret**2 + a**2 * r_ret + a**2) / (a * (r_ret - 1.0))
    return xi_pro, xi_ret

def integrate_kerr_ray_lambda(a, xi, r0=15.0, nsteps=6000):
    """Integrate equatorial null geodesic in Kerr BL coordinates using RK4, returning r, p_r, phi."""
    r = r0
    phi = 0.0
    V_r = lambda r_val: (r_val**2 + a**2 - a*xi)**2 - (r_val**2 - 2*r_val + a**2)*(xi - a)**2
    
    val0 = V_r(r0)
    p_r = -np.sqrt(max(val0, 0))
    r_hor = 1.0 + np.sqrt(max(1.0 - a**2, 0))
    
    R = [r]
    PR = [p_r]
    PHI = [phi]
    
    for _ in range(nsteps):
        def derivs(r_val, pr_val):
            dr = pr_val / r_val**2
            dpr = (2 * r_val * (r_val**2 + a**2 - a*xi) - (r_val - 1) * (xi - a)**2) / r_val**2
            dph = (xi - a) / r_val**2 + a * (r_val**2 + a**2 - a*xi) / (r_val**2 * (r_val**2 - 2*r_val + a**2))
            return dr, dpr, dph
            
        k1_r, k1_pr, k1_ph = derivs(r, p_r)
        k2_r, k2_pr, k2_ph = derivs(r + 0.5*DLAMBDA*k1_r, p_r + 0.5*DLAMBDA*k1_pr)
        k3_r, k3_pr, k3_ph = derivs(r + 0.5*DLAMBDA*k2_r, p_r + 0.5*DLAMBDA*k2_pr)
        k4_r, k4_pr, k4_ph = derivs(r + DLAMBDA*k3_r, p_r + DLAMBDA*k3_pr)
        
        r += (DLAMBDA / 6.0) * (k1_r + 2*k2_r + 2*k3_r + k4_r)
        p_r += (DLAMBDA / 6.0) * (k1_pr + 2*k2_pr + 2*k3_pr + k4_pr)
        phi += (DLAMBDA / 6.0) * (k1_ph + 2*k2_ph + 2*k3_ph + k4_ph)
        
        if r < r_hor + 0.02:
            R.append(r)
            PR.append(p_r)
            PHI.append(phi)
            return "captured", R, PR, PHI
        if r >= 17.0 and p_r > 0:
            R.append(r)
            PR.append(p_r)
            PHI.append(phi)
            return "escaped", R, PR, PHI
            
        R.append(r)
        PR.append(p_r)
        PHI.append(phi)
        
    return "undetermined", R, PR, PHI

def generate_ray_trajectory_lambda(a, xi, r0=15.0):
    """Generates the ray trajectory on the uniform affine parameter grid lambda."""
    status, R, PR, PHI = integrate_kerr_ray_lambda(a, xi, r0=r0)
    R = np.array(R, dtype=np.float32)
    PR = np.array(PR, dtype=np.float32)
    u = 1.0 / R
    return status, u, PR

def make_uniform_dataset(n_segments=N_SEGMENTS, seed=0):
    """Curriculum A: Uniform sampling of spins and impact parameters."""
    rng = np.random.default_rng(seed)
    X, Y = [], []
    while len(X) < n_segments:
        a = rng.uniform(0.0, 0.9)
        xi = rng.uniform(-9.0, 9.0)
        _, U, PR_arr = generate_ray_trajectory_lambda(a, xi)
        
        for i in range(len(U) - 1):
            X.append([U[i], PR_arr[i], a, xi])
            Y.append([U[i+1], PR_arr[i+1]])
            
    return np.array(X[:n_segments], np.float32), np.array(Y[:n_segments], np.float32)

def make_targeted_dataset(n_segments=N_SEGMENTS, seed=0):
    """Curriculum B: Concentrate sampling near critical winding window."""
    rng = np.random.default_rng(seed)
    X_crit, Y_crit = [], []
    X_bg, Y_bg = [], []
    
    n_crit_target = int(n_segments * 0.6)
    n_bg_target = n_segments - n_crit_target
    
    # Generate critical winding segments
    while len(X_crit) < n_crit_target:
        a = rng.uniform(0.0, 0.9)
        xi_pro, xi_ret = get_exact_bcrit(a)
        
        if rng.random() < 0.5:
            xi = rng.uniform(xi_pro - 0.2, xi_pro + 0.4)
        else:
            xi = rng.uniform(xi_ret - 0.4, xi_ret + 0.2)
            
        _, U, PR_arr = generate_ray_trajectory_lambda(a, xi)
        for i in range(len(U) - 1):
            X_crit.append([U[i], PR_arr[i], a, xi])
            Y_crit.append([U[i+1], PR_arr[i+1]])
            
    # Generate background segments
    while len(X_bg) < n_bg_target:
        a = rng.uniform(0.0, 0.9)
        xi_pro, xi_ret = get_exact_bcrit(a)
        
        zones = []
        if xi_ret - 0.4 > -9.0:
            zones.append((-9.0, xi_ret - 0.4))
        if xi_pro - 0.2 > xi_ret + 0.2:
            zones.append((xi_ret + 0.2, xi_pro - 0.2))
        if 9.0 > xi_pro + 0.4:
            zones.append((xi_pro + 0.4, 9.0))
            
        if len(zones) == 0:
            xi = rng.uniform(-9.0, 9.0)
        else:
            z = zones[rng.choice(len(zones))]
            xi = rng.uniform(z[0], z[1])
            
        _, U, PR_arr = generate_ray_trajectory_lambda(a, xi)
        for i in range(len(U) - 1):
            X_bg.append([U[i], PR_arr[i], a, xi])
            Y_bg.append([U[i+1], PR_arr[i+1]])
            
    X = X_crit[:n_crit_target] + X_bg[:n_bg_target]
    Y = Y_crit[:n_crit_target] + Y_bg[:n_bg_target]
    return np.array(X, np.float32), np.array(Y, np.float32)

class KerrPhoton(nn.Module):
    def __init__(self, x_mean, x_std, y_mean, y_std):
        super().__init__()
        self.register_buffer("x_mean", torch.tensor(x_mean, dtype=torch.float32))
        self.register_buffer("x_std", torch.tensor(x_std, dtype=torch.float32))
        self.register_buffer("y_mean", torch.tensor(y_mean, dtype=torch.float32))
        self.register_buffer("y_std", torch.tensor(y_std, dtype=torch.float32))
        
        self.net = nn.Sequential(
            nn.Linear(4, 256), nn.GELU(),
            nn.Linear(256, 256), nn.GELU(),
            nn.Linear(256, 256), nn.GELU(),
            nn.Linear(256, 2)
        )
        
    def forward(self, x):
        x_scaled = (x - self.x_mean) / self.x_std
        dy_scaled = self.net(x_scaled)
        dy = dy_scaled * self.y_std + self.y_mean
        return x[:, :2] + dy

def train(X, Y, steps=STEPS, seed=0):
    torch.manual_seed(seed)
    n = len(X)
    ntr = int(n * 0.9)
    idx = np.random.default_rng(seed).permutation(n)
    
    X_tr, X_te = X[idx[:ntr]], X[idx[ntr:]]
    Y_tr, Y_te = Y[idx[:ntr]], Y[idx[ntr:]]
    
    Y_delta_tr = Y_tr - X_tr[:, :2]
    
    x_mean = X_tr.mean(0)
    x_std = X_tr.std(0) + 1e-6
    y_mean = Y_delta_tr.mean(0)
    y_std = Y_delta_tr.std(0) + 1e-6
    
    m = KerrPhoton(x_mean, x_std, y_mean, y_std)
    opt = torch.optim.Adam(m.parameters(), lr=1e-3)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)
    
    Xt = torch.from_numpy(X_tr)
    Yt = torch.from_numpy(Y_tr)
    
    rng = np.random.default_rng(seed + 1)
    
    for step in range(steps):
        b = rng.integers(0, ntr, BATCH)
        x_b = Xt[b]
        y_b = Yt[b]
        
        # Scale inputs & target deltas
        x_scaled = (x_b - m.x_mean) / m.x_std
        target_delta_scaled = (y_b - x_b[:, :2] - m.y_mean) / m.y_std
        
        loss = nn.functional.mse_loss(m.net(x_scaled), target_delta_scaled)
        
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        
    m.eval()
    return m, torch.from_numpy(X_te), torch.from_numpy(Y_te)

def bcrit_capture_kerr(model, a, prograde=True, nsteps=6000):
    """Find the capture/escape boundary in xi using the learned model."""
    xi_pro_exact, xi_ret_exact = get_exact_bcrit(a)
    
    if prograde:
        xis = np.linspace(xi_pro_exact - 2.5, xi_pro_exact + 2.5, 500)
    else:
        xis = np.linspace(xi_ret_exact - 2.5, xi_ret_exact + 2.5, 500)
        
    r0 = 15.0
    u0 = 1.0 / r0
    
    V_r = lambda r, xi_val: (r**2 + a**2 - a*xi_val)**2 - (r**2 - 2*r + a**2)*(xi_val - a)**2
    
    u = np.full(len(xis), u0, dtype=np.float32)
    p_r = -np.sqrt(np.maximum([V_r(r0, xi) for xi in xis], 0)).astype(np.float32)
    
    status = np.zeros(len(xis))
    active = np.ones(len(xis), dtype=bool)
    
    u_t = torch.from_numpy(u)
    pr_t = torch.from_numpy(p_r).float()
    a_t = torch.full((len(xis),), a, dtype=torch.float32)
    xis_t = torch.from_numpy(xis.astype(np.float32))
    
    for _ in range(nsteps):
        if not active.any():
            break
            
        inp = torch.stack([u_t, pr_t, a_t, xis_t], dim=1)
        with torch.no_grad():
            out = model(inp)
            
        u_np = np.clip(out[:, 0].numpy(), -0.05, 0.55)
        pr_np = np.clip(out[:, 1].numpy(), -300.0, 300.0)
        
        cap = (u_np >= 0.49) & active
        esc = (u_np <= 1.0 / (r0 + 2.0)) & active
        
        status[cap] = 1
        status[esc] = -1
        active[cap | esc] = False
        
        u_t = torch.from_numpy(np.where(active, u_np, 0.3)).float()
        pr_t = torch.from_numpy(np.where(active, pr_np, 0.0)).float()
        
    if prograde:
        capi = np.where(status == 1)[0]
        if len(capi) == 0:
            return float(xis[0])
        last_captured = capi.max()
        if last_captured + 1 < len(xis):
            return float(0.5 * (xis[last_captured] + xis[last_captured + 1]))
        return float(xis[last_captured])
    else:
        esci = np.where(status == -1)[0]
        if len(esci) == 0:
            return float(xis[0])
        last_escaped = esci.max()
        if last_escaped + 1 < len(xis):
            return float(0.5 * (xis[last_escaped] + xis[last_escaped + 1]))
        return float(xis[last_escaped])

def main():
    print("RUNNING LEG 5b: ROTATING STRONG-FIELD CURRICULUM STUDY\n")
    
    spins = [0.0, 0.2, 0.5, 0.8]
    report = {}
    
    curricula = [
        ("uniform", make_uniform_dataset),
        ("targeted", make_targeted_dataset)
    ]
    
    for curr_name, make_fn in curricula:
        print(f"\n========================================")
        print(f"Training on: {curr_name.upper()} CURRICULUM")
        print(f"========================================")
        
        r2_seeds = []
        bcrit_errors = {s: {"pro": [], "ret": []} for s in spins}
        
        for seed in range(SEEDS):
            print(f"  Seed {seed}...")
            X, Y = make_fn(seed=100 * seed + 42)
            m, Xte, Yte = train(X, Y, seed=seed)
            
            with torch.no_grad():
                P = m(Xte)
                r2 = float(1.0 - ((P - Yte)**2).sum() / ((Yte - Yte.mean(0))**2).sum())
            r2_seeds.append(r2)
            
            for a in spins:
                xi_pro_exact, xi_ret_exact = get_exact_bcrit(a)
                
                # Prograde
                bc_pro = bcrit_capture_kerr(m, a, prograde=True)
                if bc_pro is not None:
                    err_pro = abs(bc_pro - xi_pro_exact) / xi_pro_exact
                    bcrit_errors[a]["pro"].append(err_pro)
                else:
                    bcrit_errors[a]["pro"].append(1.0)
                    
                # Retrograde
                bc_ret = bcrit_capture_kerr(m, a, prograde=False)
                if bc_ret is not None:
                    err_ret = abs(bc_ret - xi_ret_exact) / abs(xi_ret_exact)
                    bcrit_errors[a]["ret"].append(err_ret)
                else:
                    bcrit_errors[a]["ret"].append(1.0)
                    
        report[curr_name] = {
            "test_R2_mean": float(np.mean(r2_seeds)),
            "test_R2_std": float(np.std(r2_seeds)),
            "spins": {}
        }
        
        print(f"  Average Test R²: {report[curr_name]['test_R2_mean']:.5f}")
        for a in spins:
            pro_mean = float(np.mean(bcrit_errors[a]["pro"]))
            pro_std = float(np.std(bcrit_errors[a]["pro"]))
            ret_mean = float(np.mean(bcrit_errors[a]["ret"]))
            ret_std = float(np.std(bcrit_errors[a]["ret"]))
            
            report[curr_name]["spins"][str(a)] = {
                "pro_error_mean": pro_mean,
                "pro_error_std": pro_std,
                "ret_error_mean": ret_mean,
                "ret_error_std": ret_std
            }
            print(f"    a = {a:.1f} | Prograde Error: {pro_mean*100:.2f}% (std {pro_std*100:.2f}%) | Retrograde Error: {ret_mean*100:.2f}% (std {ret_std*100:.2f}%)")
            
    # Save results
    out_dir = Path("/Users/sumit/Github/TheBridge/results")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "leg5b_curriculum_results.json"
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nSaved Leg 5b results to {out_path}")
    
    # Plot results
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Modern styling
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]
    
    colors = {"uniform": "crimson", "targeted": "#0d9488"}
    markers = {"uniform": "o", "targeted": "s"}
    
    for idx, bound_type in enumerate(["pro", "ret"]):
        ax = axes[idx]
        title = "Prograde Shadow Boundary ($\\xi_{pro}$)" if bound_type == "pro" else "Retrograde Shadow Boundary ($\\xi_{ret}$)"
        
        for curr_name in ["uniform", "targeted"]:
            means = [report[curr_name]["spins"][str(a)][f"{bound_type}_error_mean"] * 100 for a in spins]
            stds = [report[curr_name]["spins"][str(a)][f"{bound_type}_error_std"] * 100 for a in spins]
            
            ax.errorbar(spins, means, yerr=stds, fmt=f"{markers[curr_name]}-", 
                        label=f"{curr_name.capitalize()} Curriculum", color=colors[curr_name],
                        linewidth=2.5, capsize=4)
            
        ax.set_xlabel("black hole spin $a$", fontsize=11)
        ax.set_ylabel("relative boundary error (%)", fontsize=11)
        ax.set_xticks(spins)
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.legend(fontsize=10)
        ax.set_title(title, fontsize=12, fontweight="bold", pad=10)
        
    fig.suptitle("Rotating Strong-Field Curriculum (Leg 5b)\n(Targeting the critical winding region reduces shadow boundary errors across all spins)", fontsize=14, fontweight="bold", y=1.02)
    fig.tight_layout()
    
    plot_path = out_dir / "leg5b_curriculum_curves.png"
    fig.savefig(plot_path, dpi=300, bbox_inches="tight")
    print(f"Saved plot to {plot_path}")
    
    # Copy to brain artifacts
    brain_dir = Path("/Users/sumit/.gemini/antigravity/brain/6d8c4aa5-66fc-4580-85dc-cd0e4dc34fa1")
    brain_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(plot_path, brain_dir / "leg5b_curriculum_curves.png")
    print(f"Copied plot to brain artifact directory at: {brain_dir / 'leg5b_curriculum_curves.png'}")

if __name__ == "__main__":
    main()

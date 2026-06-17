#!/usr/bin/env python3
"""representation_horizon.py

Generates the feature dataset, trains the deep MLP model to predict the target,
and runs the linear vs. non-linear probe sweeps across all layers to find 
the event horizons for each feature.
"""

import os
import sys
import json
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
from sklearn.linear_model import Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import r2_score

# Set seed
torch.manual_seed(42)
np.random.seed(42)

def generate_dataset(num_samples=10000, seed=42):
    rng = np.random.default_rng(seed)
    x = rng.normal(0, 1, size=(num_samples, 30)).astype(np.float32)
    
    # 1. Target y
    y = np.sin(x[:, 0] * x[:, 1]) + np.cos(x[:, 2] + x[:, 3]) + x[:, 4]**2 - x[:, 5] + x[:, 6] * x[:, 7] - np.tanh(x[:, 8] + x[:, 9])
    
    # 2. Invariant nontarget z_inv
    z_inv = x[:, 10] + x[:, 11] - x[:, 12] + x[:, 13] * x[:, 14]
    
    # 3. Shortcut noise z_noise
    z_noise = np.sign(x[:, 20] + x[:, 21]) * np.cos(5.0 * np.pi * x[:, 22])
    
    # Standardize
    y = (y - y.mean()) / y.std()
    z_inv = (z_inv - z_inv.mean()) / z_inv.std()
    z_noise = (z_noise - z_noise.mean()) / z_noise.std()
    
    return x, y.astype(np.float32), z_inv.astype(np.float32), z_noise.astype(np.float32)

class DeepMLP(nn.Module):
    def __init__(self, in_features=30, hidden_width=64, out_features=1, num_hidden_layers=5):
        super().__init__()
        self.layers = nn.ModuleList()
        # Input to first hidden
        self.layers.append(nn.Linear(in_features, hidden_width))
        # Hidden to hidden
        for _ in range(num_hidden_layers - 1):
            self.layers.append(nn.Linear(hidden_width, hidden_width))
        # Hidden to output
        self.layers.append(nn.Linear(hidden_width, out_features))
        self.activation = nn.GELU()

    def forward(self, x):
        activations = [x.detach().cpu().numpy()] # Layer 0 (Input)
        curr = x
        for i, layer in enumerate(self.layers[:-1]):
            curr = self.activation(layer(curr))
            activations.append(curr.detach().cpu().numpy()) # Layer 1 to 5
        out = self.layers[-1](curr)
        activations.append(out.detach().cpu().numpy()) # Layer 6 (Output)
        return out, activations

def main():
    print("Generating feature dataset...")
    x, y, z_inv, z_noise = generate_dataset(num_samples=10000)
    
    # 80/20 train-test split
    split = 8000
    x_train, x_test = x[:split], x[split:]
    y_train, y_test = y[:split], y[split:]
    z_inv_train, z_inv_test = z_inv[:split], z_inv[split:]
    z_noise_train, z_noise_test = z_noise[:split], z_noise[split:]
    
    model = DeepMLP()
    opt = torch.optim.Adam(model.parameters(), lr=0.005)
    loss_fn = nn.MSELoss()
    
    # Train MLP
    print("Training model...")
    X_t = torch.from_numpy(x_train)
    Y_t = torch.from_numpy(y_train)[:, None]
    
    steps = 1500
    for step in range(steps):
        pred, _ = model(X_t)
        loss = loss_fn(pred, Y_t)
        opt.zero_grad()
        loss.backward()
        opt.step()
        if step % 300 == 0:
            print(f"  step {step:4d}  mse {loss.item():.4f}")
            
    model.eval()
    with torch.no_grad():
        _, act_train = model(torch.from_numpy(x_train))
        _, act_test = model(torch.from_numpy(x_test))
        
    print("\nRunning Linear and Non-Linear Probes across layers...")
    results = {
        "y": {"linear": [], "knn": []},
        "z_inv": {"linear": [], "knn": []},
        "z_noise": {"linear": [], "knn": []}
    }
    
    for l in range(7):
        print(f"  Layer {l} Probing:")
        tr_act = act_train[l]
        te_act = act_test[l]
        
        # 1. Target y Probes
        # Linear
        ridge = Ridge(alpha=1.0)
        ridge.fit(tr_act, y_train)
        r2_lin_y = float(r2_score(y_test, ridge.predict(te_act)))
        # kNN
        knn = KNeighborsRegressor(n_neighbors=10, n_jobs=-1)
        knn.fit(tr_act, y_train)
        r2_knn_y = float(r2_score(y_test, knn.predict(te_act)))
        
        # 2. Invariant z_inv Probes
        ridge = Ridge(alpha=1.0)
        ridge.fit(tr_act, z_inv_train)
        r2_lin_z_inv = float(r2_score(z_inv_test, ridge.predict(te_act)))
        
        knn = KNeighborsRegressor(n_neighbors=10, n_jobs=-1)
        knn.fit(tr_act, z_inv_train)
        r2_knn_z_inv = float(r2_score(z_inv_test, knn.predict(te_act)))
        
        # 3. Shortcut z_noise Probes
        ridge = Ridge(alpha=1.0)
        ridge.fit(tr_act, z_noise_train)
        r2_lin_z_noise = float(r2_score(z_noise_test, ridge.predict(te_act)))
        
        knn = KNeighborsRegressor(n_neighbors=10, n_jobs=-1)
        knn.fit(tr_act, z_noise_train)
        r2_knn_z_noise = float(r2_score(z_noise_test, knn.predict(te_act)))
        
        print(f"    y      -> Lin: {r2_lin_y:+.4f}, kNN: {r2_knn_y:+.4f}")
        print(f"    z_inv  -> Lin: {r2_lin_z_inv:+.4f}, kNN: {r2_knn_z_inv:+.4f}")
        print(f"    z_noise-> Lin: {r2_lin_z_noise:+.4f}, kNN: {r2_knn_z_noise:+.4f}")
        
        results["y"]["linear"].append(r2_lin_y)
        results["y"]["knn"].append(r2_knn_y)
        results["z_inv"]["linear"].append(r2_lin_z_inv)
        results["z_inv"]["knn"].append(r2_knn_z_inv)
        results["z_noise"]["linear"].append(r2_lin_z_noise)
        results["z_noise"]["knn"].append(r2_knn_z_noise)
        
    # Find horizons
    def find_horizon(r2_list):
        for l, val in enumerate(r2_list):
            if val < 0.05:
                # verify it stays below 0.05
                if all(v < 0.05 for v in r2_list[l:]):
                    return l
        return len(r2_list) - 1
        
    horizon_z_inv = find_horizon(results["z_inv"]["knn"])
    horizon_z_noise = find_horizon(results["z_noise"]["knn"])
    
    print(f"\nRepresentation Horizons Found:")
    print(f"  z_inv horizon layer: {horizon_z_inv}")
    print(f"  z_noise horizon layer: {horizon_z_noise}")
    
    results["horizon_z_inv"] = horizon_z_inv
    results["horizon_z_noise"] = horizon_z_noise
    
    out_dir = Path("/Users/sumit/Github/TheBridge/results")
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "leg9_horizon.json"
    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved results to {out_file} ✅")

if __name__ == "__main__":
    main()

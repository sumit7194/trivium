#!/usr/bin/env python3
"""stress_tests.py

Runs the complete stress-test battery for Leg 10c:
1. Sample size expansion (300 sentences).
2. Random vector steering at Layer 14.
3. Random weights model control.
4. Upstream (early layers) vs. downstream (steered layers) control.
"""

import os
import sys
import json
import re
import random
import numpy as np
import torch
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig
from scipy.stats import pearsonr

# Original 50 sentences
ORIGINAL_SENTENCES = [
    "General relativity is a theory of gravitation developed by Albert Einstein.",
    "The Schwarzschild radius defines the event horizon of a non-rotating black hole.",
    "Light cannot escape from the strong gravitational field inside the horizon.",
    "Gravitational lensing occurs when a massive object bends the path of light.",
    "Quantum mechanics and general relativity are currently incompatible theories.",
    "A neutron star is the collapsed core of a massive supergiant star.",
    "The Big Bang theory describes the expansion and evolution of our universe.",
    "Dark matter and dark energy make up the majority of the cosmic energy density.",
    "A traversable wormhole requires exotic matter to keep its throat open.",
    "The equivalence principle states that gravitational and inertial mass are equal.",
    "Black holes evaporate slowly over time due to Hawking radiation.",
    "An orbit is the gravitationally curved trajectory of an object in space.",
    "Tidal forces stretch and squeeze bodies moving in a non-uniform field.",
    "The photon sphere is a spherical region where gravity is strong enough for light to orbit.",
    "Gravitational waves are ripples in the curvature of spacetime.",
    "We test general relativity using precise measurements of binary pulsars.",
    "A singularity is a point where the curvature of spacetime becomes infinite.",
    "The cosmological constant is associated with the energy density of empty space.",
    "Active galactic nuclei are powered by accretion onto supermassive black holes.",
    "Cosmic inflation describes a period of extremely rapid expansion in the early universe.",
    "The event horizon telescope captured the first direct image of a black hole shadow.",
    "Frame dragging is an effect where a rotating mass drags spacetime with it.",
    "Birkhoff's theorem states that any spherically symmetric vacuum solution is static.",
    "The Tolman-Oppenheimer-Volkoff equation limits the maximum mass of a neutron star.",
    "We search for primordial black holes as candidates for dark matter.",
    "Spacetime is modeled as a four-dimensional pseudo-Riemannian manifold.",
    "Geodesics represent the straightest possible paths in a curved geometry.",
    "The stress-energy tensor describes the density and flux of energy and momentum.",
    "Gauge theories describe physical forces using local symmetry transformations.",
    "No-arbitrage in financial markets is mathematically equivalent to a flat connection.",
    "Hierarchical structures in data are naturally represented in hyperbolic space.",
    "Neural network activations form complex manifolds in high-dimensional space.",
    "We probe latent representations to measure the legibility of features.",
    "Information bottleneck theory explains how networks compress irrelevant features.",
    "Roger Penrose proved the singularity theorems using topological methods.",
    "Stephen Hawking discovered that black holes have a finite thermodynamic temperature.",
    "The no-hair theorem states that stationary black holes depend only on three parameters.",
    "Quantum gravity aims to describe the quantum behavior of spacetime.",
    "The holographic principle suggests that a volume of space is encoded on its boundary.",
    "A de Sitter universe has a positive cosmological constant and expands exponentially.",
    "Anti-de Sitter space has a negative cosmological constant and is highly symmetric.",
    "The Oppenheimer-Snyder model describes the gravitational collapse of a dust cloud.",
    "We model the cosmic microwave background radiation to measure cosmological parameters.",
    "The Keck observatory measured the orbits of stars around the Sgr A* black hole.",
    "We use numerical relativity to simulate the merger of two black holes.",
    "A standard candle is an astronomical object with a known intrinsic luminosity.",
    "Redshift measures the expansion of light waves as they travel through space.",
    "The Friedmann equations describe the expansion of space in homogeneous universes.",
    "A cosmic string is a hypothetical 1-D topological defect in spacetime.",
    "The Weak Equivalence Principle is tested with high precision in space experiments."
]

def generate_additional_sentences(count=250):
    random.seed(42)
    subjects = [
        "General relativity", "Quantum mechanics", "A supermassive black hole", "The Schwarzschild radius",
        "A neutron star", "Dark matter", "Dark energy", "Spacetime curvature", "A gravitational wave",
        "An event horizon", "The equivalence principle", "Hawking radiation", "The cosmological constant",
        "The photon sphere", "Frame dragging", "Birkhoff's theorem", "The TOV equation", "A cosmic string",
        "Hyperbolic space", "Information bottleneck theory", "Singularity theorems", "The holographic principle"
    ]
    verbs = [
        "describes", "governs", "influences", "limits", "dictates", "modulates", "regulates", "warps",
        "bends", "shapes", "constrains", "defines", "explains", "predicts", "determines"
    ]
    objects = [
        "the propagation of light", "the evolution of the universe", "the geometry of spacetime",
        "the dynamics of massive bodies", "the behavior of quantum particles", "the structure of stars",
        "the information flow in networks", "the path of geodesics", "the properties of horizons",
        "the thermodynamic state of black holes", "the expansion rate of space", "the deflection of rays"
    ]
    qualifiers = [
        "in strong fields", "near the singularity", "across cosmic scales", "in flat space",
        "under extreme density", "with high precision", "at the quantum scale", "for rotating systems"
    ]
    sentences = []
    while len(sentences) < count:
        s = random.choice(subjects)
        v = random.choice(verbs)
        o = random.choice(objects)
        q = random.choice(qualifiers)
        sent = f"{s} {v} {o} {q}."
        if sent not in sentences:
            sentences.append(sent)
    return sentences

ALL_SENTENCES = ORIGINAL_SENTENCES + generate_additional_sentences(250)

TARGET_WORDS = {"currently", "incompatible", "requires", "exotic", "limits", "candidates", "hypothetical"}
CONTROL_WORDS = {"theory", "mass", "star", "space", "light", "field", "core"}

class AdditiveSteeringHook:
    def __init__(self, layer_idx, virtue_vector, alpha):
        self.layer_idx = layer_idx
        self.alpha = alpha
        v = torch.tensor(virtue_vector, dtype=torch.float32)
        self.v_normalized = (v / (v.norm() + 1e-10)).unsqueeze(0).unsqueeze(0)
        self.handle = None

    def hook_fn(self, module, input, output):
        hidden = output[0] if isinstance(output, tuple) else output
        device = hidden.device
        v = self.v_normalized.to(device).to(hidden.dtype)
        hidden = hidden + self.alpha * v
        if isinstance(output, tuple):
            return (hidden,) + output[1:]
        return hidden

    def attach(self, model):
        layer = model.model.layers[self.layer_idx]
        self.handle = layer.register_forward_hook(self.hook_fn)

    def detach(self):
        if self.handle:
            self.handle.remove()
            self.handle = None

def find_word_token_indices(tokenizer, sentence, input_ids_list, words_set):
    token_spans = []
    current_text = ""
    for idx, tid in enumerate(input_ids_list):
        token_text = tokenizer.decode([tid])
        start_char = len(current_text)
        current_text += token_text
        end_char = len(current_text)
        token_spans.append((start_char, end_char))
        
    indices = []
    for word in words_set:
        for match in re.finditer(rf"\b{re.escape(word)}\b", sentence, re.IGNORECASE):
            start_char, end_char = match.span()
            for token_idx, (t_start, t_end) in enumerate(token_spans):
                if max(start_char, t_start) < min(end_char, t_end):
                    if token_idx not in indices:
                        indices.append(token_idx)
    return indices

def compute_gravity_metrics_for_layers(model, tokenizer, sentences, device, layers, hook=None):
    if hook:
        hook.attach(model)
        
    decay_exps = {l: [] for l in layers}
    correlations = {l: [] for l in layers}
    slopes = {l: [] for l in layers}
    lensing_ratios = {l: [] for l in layers}
    mass_ratios = {l: [] for l in layers}
    
    for s_idx, sent in enumerate(sentences):
        inputs = tokenizer(sent, return_tensors="pt").to(device)
        input_ids_list = inputs["input_ids"][0].tolist()
        seq_len = len(input_ids_list)
        if seq_len < 5:
            continue
            
        target_indices = find_word_token_indices(tokenizer, sent, input_ids_list, TARGET_WORDS)
        control_indices = find_word_token_indices(tokenizer, sent, input_ids_list, CONTROL_WORDS)
        
        with torch.no_grad():
            outputs = model(**inputs, output_attentions=True)
            
        # Precompute distance matrix for H2
        dist_matrix = np.abs(np.arange(seq_len)[:, None] - np.arange(seq_len))
        
        # Precompute indices for H3 lensing
        idx_i = np.arange(seq_len - 2)
        idx_j = idx_i + 1
        idx_k = idx_i + 2
        
        for l in layers:
            attn = outputs.attentions[l][0].mean(dim=0).cpu().numpy()
            
            # 1. Vectorized Decay Exponent
            r_vals = []
            a_vals = []
            for r in range(1, seq_len):
                diag1 = np.diagonal(attn, offset=r)
                diag2 = np.diagonal(attn, offset=-r)
                pairs = np.concatenate([diag1, diag2])
                if len(pairs) > 0:
                    r_vals.append(r)
                    a_vals.append(float(np.mean(pairs)))
            
            r_arr = np.array(r_vals)
            a_arr = np.array(a_vals)
            mask = a_arr > 0
            if np.sum(mask) >= 3:
                log_r = np.log(r_arr[mask])
                log_a = np.log(a_arr[mask])
                slope, _ = np.polyfit(log_r, log_a, 1)
                decay_exps[l].append(float(-slope))
            else:
                decay_exps[l].append(0.0)
                
            # 2. Vectorized Horizon & Mass
            mass = attn.sum(axis=0)
            mask_threshold = attn >= 0.05
            hor_arr = np.max(dist_matrix * mask_threshold, axis=0)
            
            mass_arr = np.array(mass)
            if len(mass_arr) >= 3 and np.std(hor_arr) > 0 and np.std(mass_arr) > 0:
                corr, _ = pearsonr(mass_arr, hor_arr)
                slope, _ = np.polyfit(mass_arr, hor_arr, 1)
                correlations[l].append(float(corr))
                slopes[l].append(float(slope))
                
            # 3. Vectorized Lensing
            med_mass = np.median(mass)
            attn_ki = attn[idx_k, idx_i]
            mass_j = mass[idx_j]
            high_mask = mass_j > med_mass
            
            lens_high = attn_ki[high_mask]
            lens_low = attn_ki[~high_mask]
            
            if len(lens_high) > 0 and len(lens_low) > 0 and np.mean(lens_low) > 0:
                lensing_ratios[l].append(float(np.mean(lens_high) / np.mean(lens_low)))
                
            # 4. Token Mass Redirection
            if target_indices and control_indices:
                target_mass = np.mean([mass[idx] for idx in target_indices])
                control_mass = np.mean([mass[idx] for idx in control_indices])
                if control_mass > 0:
                    mass_ratios[l].append(float(target_mass / control_mass))
                    
    if hook:
        hook.detach()
        
    # Average over sentences for each layer
    summary = {}
    for l in layers:
        summary[l] = {
            "decay_exponent": float(np.mean(decay_exps[l])) if decay_exps[l] else 0.0,
            "horizon_correlation": float(np.mean(correlations[l])) if correlations[l] else 0.0,
            "horizon_slope": float(np.mean(slopes[l])) if slopes[l] else 0.0,
            "lensing_ratio": float(np.mean(lensing_ratios[l])) if lensing_ratios[l] else 0.0,
            "epistemic_mass_ratio": float(np.mean(mass_ratios[l])) if mass_ratios[l] else 0.0
        }
    return summary

def main():
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-4B")
    
    # Paths
    vector_path = Path("/Users/sumit/Github/Phronesis/mvp/results/vectors/qwen3-4b/triplets-intellectual-humility/last_token/layer_14_virtue_vector.npy")
    virtue_vector = np.load(vector_path)
    
    # Generate random control vector of the same norm
    np.random.seed(42)
    random_vector = np.random.normal(size=virtue_vector.shape)
    random_vector = random_vector / (np.linalg.norm(random_vector) + 1e-10) * np.linalg.norm(virtue_vector)
    
    # Result container
    stress_results = {}
    
    # ─── TEST 1 & TEST 2: RUN SWEEPS ON TRAINED MODEL (300 SENTENCES) ───
    print("\n--- TEST 1 & 2: Running sweeps on Trained Model (300 Sentences) ---")
    print("Loading Pretrained Model...")
    model_trained = AutoModelForCausalLM.from_pretrained(
        "Qwen/Qwen3-4B", torch_dtype=torch.float16, device_map=None, attn_implementation="eager"
    ).to(device)
    model_trained.eval()
    
    alphas = [-3.0, -1.0, 0.0, 1.0, 3.0]
    steer_layer = 14
    steered_layers = list(range(15, 36))
    all_layers = list(range(36))
    
    humility_sweep = {}
    random_vec_sweep = {}
    early_vs_late_data = {}
    
    # 1. Humility Steering Sweep
    print("Running Humility Steering Sweeps...")
    for alpha in alphas:
        print(f"  alpha = {alpha:.1f}...")
        hook = AdditiveSteeringHook(steer_layer, virtue_vector, alpha) if alpha != 0.0 else None
        
        # For the early layer control check (Test 4), we extract all layers under humility steering
        layer_summary = compute_gravity_metrics_for_layers(
            model_trained, tokenizer, ALL_SENTENCES, device, all_layers, hook=hook
        )
        
        # Save early layer checks
        early_vs_late_data[str(alpha)] = layer_summary
        
        # Compute mean metrics over steered layers (15-35) for Test 1 (Sample expansion)
        humility_sweep[str(alpha)] = {
            "decay_exponent": float(np.mean([layer_summary[l]["decay_exponent"] for l in steered_layers])),
            "horizon_correlation": float(np.mean([layer_summary[l]["horizon_correlation"] for l in steered_layers])),
            "horizon_slope": float(np.mean([layer_summary[l]["horizon_slope"] for l in steered_layers])),
            "lensing_ratio": float(np.mean([layer_summary[l]["lensing_ratio"] for l in steered_layers])),
            "epistemic_mass_ratio": float(np.mean([layer_summary[l]["epistemic_mass_ratio"] for l in steered_layers]))
        }
        
    stress_results["humility_steering"] = humility_sweep
    stress_results["early_vs_late_raw"] = early_vs_late_data
    
    # 2. Random Vector Steering Sweep (T2)
    print("Running Random Vector Steering Sweeps...")
    for alpha in alphas:
        print(f"  alpha = {alpha:.1f}...")
        hook = AdditiveSteeringHook(steer_layer, random_vector, alpha) if alpha != 0.0 else None
        layer_summary = compute_gravity_metrics_for_layers(
            model_trained, tokenizer, ALL_SENTENCES, device, steered_layers, hook=hook
        )
        random_vec_sweep[str(alpha)] = {
            "decay_exponent": float(np.mean([layer_summary[l]["decay_exponent"] for l in steered_layers])),
            "horizon_correlation": float(np.mean([layer_summary[l]["horizon_correlation"] for l in steered_layers])),
            "horizon_slope": float(np.mean([layer_summary[l]["horizon_slope"] for l in steered_layers])),
            "lensing_ratio": float(np.mean([layer_summary[l]["lensing_ratio"] for l in steered_layers])),
            "epistemic_mass_ratio": float(np.mean([layer_summary[l]["epistemic_mass_ratio"] for l in steered_layers]))
        }
    stress_results["random_vector_steering"] = random_vec_sweep
    
    # Clean up memory
    del model_trained
    if device == "mps":
        torch.mps.empty_cache()
    import gc
    gc.collect()
    
    # ─── TEST 3: RANDOM WEIGHTS MODEL CONTROL ───
    print("\n--- TEST 3: Running Random Weights Model ---")
    config = AutoConfig.from_pretrained("Qwen/Qwen3-4B")
    config.attn_implementation = "eager"
    config.torch_dtype = torch.float16
    model_random = AutoModelForCausalLM.from_config(config, torch_dtype=torch.float16, attn_implementation="eager")
    model_random = model_random.to(device)
    model_random.eval()
    
    # Run baseline (no steering) on 100 sentences to check for architecture bias
    print("Extracting gravity metrics from Random Model...")
    random_model_summary = compute_gravity_metrics_for_layers(
        model_random, tokenizer, ALL_SENTENCES[:100], device, steered_layers, hook=None
    )
    
    stress_results["random_model_baseline"] = {
        "decay_exponent": float(np.mean([random_model_summary[l]["decay_exponent"] for l in steered_layers])),
        "horizon_correlation": float(np.mean([random_model_summary[l]["horizon_correlation"] for l in steered_layers])),
        "horizon_slope": float(np.mean([random_model_summary[l]["horizon_slope"] for l in steered_layers])),
        "lensing_ratio": float(np.mean([random_model_summary[l]["lensing_ratio"] for l in steered_layers])),
        "epistemic_mass_ratio": float(np.mean([random_model_summary[l]["epistemic_mass_ratio"] for l in steered_layers]))
    }
    print(f"Random Model Baseline Results:")
    print(f"  Decay Exponent:      {stress_results['random_model_baseline']['decay_exponent']:.4f}")
    print(f"  Horizon Correlation: {stress_results['random_model_baseline']['horizon_correlation']:.4f}")
    print(f"  Horizon Slope:       {stress_results['random_model_baseline']['horizon_slope']:.4f}")
    print(f"  Lensing Ratio:       {stress_results['random_model_baseline']['lensing_ratio']:.4f}")
    print(f"  Epistemic Mass Ratio:{stress_results['random_model_baseline']['epistemic_mass_ratio']:.4f}")
    
    # Save results
    out_dir = Path("/Users/sumit/Github/TheBridge/results")
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "leg10c_stress_results.json"
    with open(out_file, "w") as f:
        json.dump(stress_results, f, indent=2)
    print(f"\nSaved stress-test results to {out_file} ✅")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""steer_attention_gravity.py

Loads Qwen3-4B, applies additive activation steering along the intellectual humility
virtue vector at Layer 14, sweeps steering scales, and computes the attention gravity
metrics (decay, horizon correlation/slope, lensing, and target token mass redirection).
"""

import os
import sys
import json
import re
import numpy as np
import torch
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer
from scipy.stats import pearsonr

# 50 diverse sentences for testing (same as Leg 10)
SENTENCES = [
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
        # Additive steering: h' = h + alpha * v_normalized
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

def load_model_and_vector():
    print("Loading Qwen3-4B...")
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-4B")
    model = AutoModelForCausalLM.from_pretrained(
        "Qwen/Qwen3-4B", torch_dtype=torch.float16, device_map=None, attn_implementation="eager"
    )
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model = model.to(device)
    model.eval()
    print(f"Loaded model successfully on {device}")
    
    # Load virtue vector
    vector_path = Path("/Users/sumit/Github/Phronesis/mvp/results/vectors/qwen3-4b/triplets-intellectual-humility/last_token/layer_14_virtue_vector.npy")
    if not vector_path.exists():
        raise FileNotFoundError(f"Virtue vector not found at {vector_path}")
    virtue_vector = np.load(vector_path)
    print(f"Loaded intellectual humility vector from {vector_path} (shape: {virtue_vector.shape})")
    
    return model, tokenizer, virtue_vector, device

def find_word_token_indices(tokenizer, sentence, input_ids_list, words_set):
    import re
    # Reconstruct the token spans by decoding prefixes
    token_spans = []
    current_text = ""
    for idx, tid in enumerate(input_ids_list):
        token_text = tokenizer.decode([tid])
        start_char = len(current_text)
        current_text += token_text
        end_char = len(current_text)
        token_spans.append((start_char, end_char))
        
    # Find matching character spans for words in the sentence
    indices = []
    for word in words_set:
        for match in re.finditer(rf"\b{re.escape(word)}\b", sentence, re.IGNORECASE):
            start_char, end_char = match.span()
            # Find tokens that overlap with this character range
            for token_idx, (t_start, t_end) in enumerate(token_spans):
                if max(start_char, t_start) < min(end_char, t_end):
                    if token_idx not in indices:
                        indices.append(token_idx)
    return indices

def main():
    model, tokenizer, virtue_vector, device = load_model_and_vector()
    
    # We steer at layer 14, and analyze steered layers 15 to 35 (inclusive)
    steer_layer = 14
    steered_layers = list(range(15, 36))
    
    alphas = [-3.0, -1.0, 0.0, 1.0, 3.0]
    results_by_alpha = {}
    
    for alpha in alphas:
        print(f"\nRunning sweep with steering alpha = {alpha:.1f}...")
        
        # Attach steering hook (skip if alpha is 0.0)
        hook = None
        if alpha != 0.0:
            hook = AdditiveSteeringHook(steer_layer, virtue_vector, alpha)
            hook.attach(model)
            
        # Accumulators for this alpha
        alpha_decay_exponents = []
        alpha_correlations = []
        alpha_slopes = []
        alpha_lensing_ratios = []
        alpha_mass_ratios = []
        
        for s_idx, sent in enumerate(SENTENCES):
            inputs = tokenizer(sent, return_tensors="pt").to(device)
            input_ids_list = inputs["input_ids"][0].tolist()
            seq_len = len(input_ids_list)
            if seq_len < 5:
                continue
                
            # Find indices of target and control tokens
            target_indices = find_word_token_indices(tokenizer, sent, input_ids_list, TARGET_WORDS)
            control_indices = find_word_token_indices(tokenizer, sent, input_ids_list, CONTROL_WORDS)
            
            with torch.no_grad():
                outputs = model(**inputs, output_attentions=True)
                
            # Compute metrics for this sentence across all steered layers
            for l in steered_layers:
                attn = outputs.attentions[l][0].mean(dim=0).cpu().numpy() # (seq_len, seq_len)
                
                # 1. Decay Exponent (H1)
                r_vals = []
                a_vals = []
                for r in range(1, seq_len):
                    pairs = [attn[i, j] for i in range(seq_len) for j in range(seq_len) if abs(i - j) == r]
                    if pairs:
                        r_vals.append(r)
                        a_vals.append(float(np.mean(pairs)))
                
                r_arr = np.array(r_vals)
                a_arr = np.array(a_vals)
                mask = a_arr > 0
                if np.sum(mask) >= 3:
                    log_r = np.log(r_arr[mask])
                    log_a = np.log(a_arr[mask])
                    slope, _ = np.polyfit(log_r, log_a, 1)
                    decay_exponent = float(-slope)
                else:
                    decay_exponent = 0.0
                alpha_decay_exponents.append(decay_exponent)
                
                # 2. Token Mass and Horizon Scaling (H2)
                mass = attn.sum(axis=0) # (seq_len,)
                horizons = []
                for j in range(seq_len):
                    h_rad = 0
                    for i in range(seq_len):
                        if attn[i, j] >= 0.05:
                            h_rad = max(h_rad, abs(i - j))
                    horizons.append(h_rad)
                
                mass_arr = np.array(mass)
                hor_arr = np.array(horizons)
                if len(mass_arr) >= 3 and np.std(hor_arr) > 0 and np.std(mass_arr) > 0:
                    corr, _ = pearsonr(mass_arr, hor_arr)
                    slope, _ = np.polyfit(mass_arr, hor_arr, 1)
                    alpha_correlations.append(float(corr))
                    alpha_slopes.append(float(slope))
                
                # 3. Lensing (H3)
                lens_high = []
                lens_low = []
                med_mass = np.median(mass)
                for i in range(seq_len - 2):
                    j = i + 1
                    k = i + 2
                    if mass[j] > med_mass:
                        lens_high.append(float(attn[k, i]))
                    else:
                        lens_low.append(float(attn[k, i]))
                if lens_high and lens_low and np.mean(lens_low) > 0:
                    lensing_ratio = float(np.mean(lens_high) / np.mean(lens_low))
                    alpha_lensing_ratios.append(lensing_ratio)
                    
                # 4. Token Mass Redirection (H4)
                if target_indices and control_indices:
                    target_mass = np.mean([mass[idx] for idx in target_indices])
                    control_mass = np.mean([mass[idx] for idx in control_indices])
                    if control_mass > 0:
                        alpha_mass_ratios.append(float(target_mass / control_mass))
                        
            if (s_idx + 1) % 10 == 0:
                print(f"  Processed {s_idx + 1}/{len(SENTENCES)} sentences...")
                
        # Detach hook if attached
        if hook:
            hook.detach()
            
        # Store mean values across all sentences and steered layers
        results_by_alpha[str(alpha)] = {
            "decay_exponent": float(np.mean(alpha_decay_exponents)),
            "horizon_correlation": float(np.mean(alpha_correlations)) if alpha_correlations else 0.0,
            "horizon_slope": float(np.mean(alpha_slopes)) if alpha_slopes else 0.0,
            "lensing_ratio": float(np.mean(alpha_lensing_ratios)) if alpha_lensing_ratios else 0.0,
            "epistemic_mass_ratio": float(np.mean(alpha_mass_ratios)) if alpha_mass_ratios else 0.0
        }
        
        print(f"Alpha {alpha:.1f} Results:")
        print(f"  Decay Exponent:      {results_by_alpha[str(alpha)]['decay_exponent']:.4f}")
        print(f"  Horizon Correlation: {results_by_alpha[str(alpha)]['horizon_correlation']:.4f}")
        print(f"  Horizon Slope:       {results_by_alpha[str(alpha)]['horizon_slope']:.4f}")
        print(f"  Lensing Ratio:       {results_by_alpha[str(alpha)]['lensing_ratio']:.4f}")
        print(f"  Epistemic Mass Ratio:{results_by_alpha[str(alpha)]['epistemic_mass_ratio']:.4f}")

    # Save summary results
    out_dir = Path("/Users/sumit/Github/TheBridge/results")
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "leg10b_steered_gravity.json"
    with open(out_file, "w") as f:
        json.dump(results_by_alpha, f, indent=2)
    print(f"\nSaved sweep results to {out_file} ✅")

if __name__ == "__main__":
    main()

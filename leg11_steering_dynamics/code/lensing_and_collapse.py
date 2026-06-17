#!/usr/bin/env python3
"""lensing_and_collapse.py

Runs fine-grained sweeps of steering alpha vs lensing ratio, and generation tests
to quantify the qualitative and quantitative collapse of model coherence.
"""

import os
import sys
import json
import numpy as np
import torch
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer

# 50 diverse sentences for lensing sweep (same as Leg 10d)
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

# 5 prompts for coherence/collapse sweeps
PROMPTS = [
    "The primary goal of science is",
    "When faced with a hard mathematical problem, a researcher should",
    "Artificial intelligence will shape the future by",
    "In history, the most successful societies were those that",
    "To understand the universe, one must first study"
]

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

def main():
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Using device: {device}")
    
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-4B")
    # Make sure we set padding side for generation
    tokenizer.pad_token = tokenizer.eos_token
    
    model = AutoModelForCausalLM.from_pretrained(
        "Qwen/Qwen3-4B", torch_dtype=torch.float16, device_map=None, attn_implementation="eager"
    ).to(device)
    model.eval()
    
    # Load virtue vector
    vector_path = Path("/Users/sumit/Github/Phronesis/mvp/results/vectors/qwen3-4b/triplets-intellectual-humility/last_token/layer_14_virtue_vector.npy")
    virtue_vector = np.load(vector_path)
    
    steer_layer = 14
    steered_layers = list(range(15, 36))
    
    # Part 1: Fine-Grained Lensing Sweep
    # Alphas from 0.0 to 50.0 in steps of 2.0
    lensing_alphas = np.arange(0.0, 52.0, 2.0).tolist()
    lensing_results = {}
    
    print("\n--- Starting Fine-Grained Lensing Sweep ---")
    for alpha in lensing_alphas:
        print(f"Running lensing sweep for alpha = {alpha:.1f}...")
        hook = AdditiveSteeringHook(steer_layer, virtue_vector, alpha) if alpha != 0.0 else None
        if hook:
            hook.attach(model)
            
        alpha_lensing_ratios = []
        
        for sent in SENTENCES:
            inputs = tokenizer(sent, return_tensors="pt").to(device)
            seq_len = inputs["input_ids"].shape[1]
            if seq_len < 5:
                continue
                
            with torch.no_grad():
                outputs = model(**inputs, output_attentions=True)
                
            idx_i = np.arange(seq_len - 2)
            idx_j = idx_i + 1
            idx_k = idx_i + 2
            
            for l in steered_layers:
                attn = outputs.attentions[l][0].mean(dim=0).cpu().numpy()
                mass = attn.sum(axis=0)
                
                med_mass = np.median(mass)
                attn_ki = attn[idx_k, idx_i]
                mass_j = mass[idx_j]
                high_mask = mass_j > med_mass
                lens_high = attn_ki[high_mask]
                lens_low = attn_ki[~high_mask]
                if len(lens_high) > 0 and len(lens_low) > 0 and np.mean(lens_low) > 0:
                    alpha_lensing_ratios.append(float(np.mean(lens_high) / np.mean(lens_low)))
                    
        if hook:
            hook.detach()
            
        lensing_results[str(alpha)] = float(np.mean(alpha_lensing_ratios)) if alpha_lensing_ratios else 1.0
        print(f"  Alpha {alpha:.1f} Lensing Ratio: {lensing_results[str(alpha)]:.4f}")
        
    # Part 2: Qualitative Coherence & Collapse Sweep
    # Alphas to test generation
    gen_alphas = [0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0]
    gen_results = {}
    
    print("\n--- Starting Generation Coherence/Collapse Sweep ---")
    for alpha in gen_alphas:
        print(f"Running generation sweep for alpha = {alpha:.1f}...")
        hook = AdditiveSteeringHook(steer_layer, virtue_vector, alpha) if alpha != 0.0 else None
        if hook:
            hook.attach(model)
            
        alpha_generations = []
        alpha_entropies = []
        
        for prompt in PROMPTS:
            inputs = tokenizer(prompt, return_tensors="pt").to(device)
            
            with torch.no_grad():
                gen_outputs = model.generate(
                    **inputs,
                    max_new_tokens=50,
                    temperature=0.7,
                    top_p=0.9,
                    do_sample=True,
                    return_dict_in_generate=True,
                    output_scores=True
                )
            
            # Decode generated text
            gen_text = tokenizer.decode(gen_outputs.sequences[0], skip_special_tokens=True)
            
            # Calculate token-wise generation entropy
            step_entropies = []
            for score in gen_outputs.scores:
                # score shape: (1, vocab_size)
                probs = torch.softmax(score[0], dim=-1)
                entropy = -torch.sum(probs * torch.log2(probs + 1e-10))
                step_entropies.append(float(entropy.item()))
                
            mean_ent = float(np.mean(step_entropies)) if step_entropies else 0.0
            
            alpha_generations.append({
                "prompt": prompt,
                "output": gen_text,
                "entropy": mean_ent
            })
            alpha_entropies.append(mean_ent)
            
        if hook:
            hook.detach()
            
        gen_results[str(alpha)] = {
            "mean_generation_entropy": float(np.mean(alpha_entropies)),
            "samples": alpha_generations
        }
        print(f"  Alpha {alpha:.1f} Mean Gen Entropy: {gen_results[str(alpha)]['mean_generation_entropy']:.4f}")
        print(f"  Sample Output: '{alpha_generations[0]['output']}'\n")
        
    # Combine and save results
    output_data = {
        "lensing_sweep": lensing_results,
        "generation_sweep": gen_results
    }
    
    out_dir = Path("/Users/sumit/Github/TheBridge/results")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "leg11_lensing_collapse.json"
    with open(out_path, "w") as f:
        json.dump(output_data, f, indent=2)
        
    print(f"\nSaved results successfully to {out_path}")

if __name__ == "__main__":
    main()

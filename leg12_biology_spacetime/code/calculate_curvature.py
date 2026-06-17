#!/usr/bin/env python3
"""calculate_curvature.py

Queries the STRING database for a PPI network, implements weighted Forman-Ricci curvature (FRC),
and sweeps chaperone node weights to simulate cell stress and test geometric warping.
"""

import os
import sys
import json
import argparse
import subprocess
import numpy as np
import networkx as nx
from pathlib import Path

# Yeast configuration
YEAST_STRESS = ["HSP82", "SSA1", "HSF1", "SLT2", "YAP1"]
YEAST_CONTROL = ["TDH3", "ACT1", "TUB1"]

# Human configuration
HUMAN_STRESS = ["HSP90AA1", "HSPA1A", "HSF1", "MAPK1", "TP53"]
HUMAN_CONTROL = ["GAPDH", "ACTB", "TUBB"]

def run_string_query(species, identifiers, add_nodes, output_path):
    """Calls the string-database CLI tool to fetch the PPI network."""
    cli_path = "/Users/sumit/.gemini/config/plugins/science/skills/string_database/scripts/string_cli.py"
    cmd = [
        "uv", "run", cli_path, "network",
        "--species", str(species),
        "--identifiers"
    ] + identifiers + [
        "--add_nodes", str(add_nodes),
        "--required_score", "400",
        "--output", str(output_path)
    ]
    
    print(f"Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

def calculate_forman_curvature(G, vertex_weights):
    """Calculates weighted Forman-Ricci curvature for all edges in graph G.
    
    Formula:
    Ric(e) = w_e * ( w(v1)/w_e + w(v2)/w_e - sum_{e_v1 ~ e} w(v1)/sqrt(w_e * w_e_v1) - sum_{e_v2 ~ e} w(v2)/sqrt(w_e * w_e_v2) )
    """
    frc = {}
    for u, v, d in G.edges(data=True):
        w_e = d["weight"]
        w_u = vertex_weights.get(u, 1.0)
        w_v = vertex_weights.get(v, 1.0)
        
        # Term 1: node weight contributions divided by edge weight
        t1 = (w_u + w_v) / w_e
        
        # Term 2: incident edges at node u (excluding e itself)
        sum_u = 0.0
        for neighbor in G.neighbors(u):
            if neighbor == v:
                continue
            w_e_u = G[u][neighbor]["weight"]
            sum_u += w_u / np.sqrt(w_e * w_e_u)
            
        # Term 3: incident edges at node v (excluding e itself)
        sum_v = 0.0
        for neighbor in G.neighbors(v):
            if neighbor == u:
                continue
            w_e_v = G[v][neighbor]["weight"]
            sum_v += w_v / np.sqrt(w_e * w_e_v)
            
        # Total curvature of the edge
        edge_ric = w_e * (t1 - sum_u - sum_v)
        frc[(u, v)] = float(edge_ric)
        
    return frc

def main():
    parser = argparse.ArgumentParser(description="Calculate biological network curvature under stress.")
    parser.add_argument("--species", type=int, default=4932, help="NCBI Taxon ID (4932 for yeast, 9606 for human)")
    parser.add_argument("--add_nodes", type=int, default=15, help="Number of neighbors to add from STRING")
    args = parser.parse_args()
    
    # Select configs based on species
    if args.species == 4932:
        stress_group = YEAST_STRESS
        control_group = YEAST_CONTROL
        species_name = "Yeast (4932)"
    elif args.species == 9606:
        stress_group = HUMAN_STRESS
        control_group = HUMAN_CONTROL
        species_name = "Human (9606)"
    else:
        print(f"Error: Unsupported species Taxon ID {args.species}. Use 4932 or 9606.")
        sys.exit(1)
        
    print(f"\n--- Leg 12: Biological Spacetime Curvature for {species_name} ---")
    
    # Query STRING to get network
    temp_dir = Path("/tmp")
    temp_dir.mkdir(parents=True, exist_ok=True)
    tsv_path = temp_dir / f"string_network_{args.species}.tsv"
    
    all_query_genes = stress_group + control_group
    run_string_query(args.species, all_query_genes, args.add_nodes, tsv_path)
    
    # Build Graph from TSV
    G = nx.Graph()
    with open(tsv_path, "r") as f:
        header = f.readline().strip().split("\t")
        name_a_idx = header.index("preferredName_A")
        name_b_idx = header.index("preferredName_B")
        score_idx = header.index("score")
        
        for line in f:
            parts = line.strip().split("\t")
            if not parts or len(parts) < max(name_a_idx, name_b_idx, score_idx):
                continue
            node_a = parts[name_a_idx]
            node_b = parts[name_b_idx]
            score = float(parts[score_idx]) # STRING scores are between 0.0 and 1.0
            
            G.add_edge(node_a, node_b, weight=score)
            
    print(f"Graph loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges.")
    
    # Identify stress and control nodes that actually exist in the graph
    existing_stress = [n for n in stress_group if n in G]
    existing_control = [n for n in control_group if n in G]
    print(f"Stress group nodes in graph: {existing_stress}")
    print(f"Control group nodes in graph: {existing_control}")
    
    # We will sweep stress scale gamma from 1.0 to 10.0
    gammas = np.arange(1.0, 11.0, 1.0).tolist()
    sweep_results = {}
    
    for gamma in gammas:
        # Define vertex weights
        vertex_weights = {}
        for node in G.nodes():
            if node in existing_stress:
                vertex_weights[node] = gamma
            else:
                vertex_weights[node] = 1.0
                
        # Calculate Curvature
        frc = calculate_forman_curvature(G, vertex_weights)
        
        # Segment edge curvatures
        chaperone_curvs = []
        control_curvs = []
        all_curvs = list(frc.values())
        
        for (u, v), curv in frc.items():
            # Chaperone-connected if either endpoint is in the stress group
            is_chaperone = (u in existing_stress) or (v in existing_stress)
            # Housekeeping-connected if both endpoints are in the control group
            is_control_only = (u in existing_control) and (v in existing_control)
            
            if is_chaperone:
                chaperone_curvs.append(curv)
            elif is_control_only:
                control_curvs.append(curv)
                
        mean_chaperone = float(np.mean(chaperone_curvs)) if chaperone_curvs else 0.0
        mean_control = float(np.mean(control_curvs)) if control_curvs else 0.0
        var_all = float(np.var(all_curvs))
        
        sweep_results[str(gamma)] = {
            "mean_chaperone_frc": mean_chaperone,
            "mean_control_frc": mean_control,
            "var_all_frc": var_all,
            "edges": [{"node_A": u, "node_B": v, "frc": val} for (u, v), val in frc.items()]
        }
        
        print(f"Gamma = {gamma:.1f} | Mean Chaperone FRC: {mean_chaperone:.4f} | Mean Control FRC: {mean_control:.4f} | Total Variance: {var_all:.4f}")
        
    # Save results
    out_dir = Path("/Users/sumit/Github/TheBridge/results")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "leg12_biology_results.json"
    with open(out_path, "w") as f:
        json.dump({
            "species": args.species,
            "gammas": sweep_results
        }, f, indent=2)
        
    print(f"Saved Leg 12 results to {out_path}")

if __name__ == "__main__":
    main()

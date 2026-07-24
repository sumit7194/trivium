#!/usr/bin/env python3
"""A1 — the too-clean audit: sweep the bridge's results for machine-precision agreements, classify each.

    python3 audit.py

Gate A1 frozen in ../PREREGISTRATION.md. L2 made mechanical: any numerical-method agreement tighter than
the method's order predicts must be exact-by-construction or it is a bug suspect. The sweep is automatable;
the classification carries a frozen baseline (below) built from knowledge of how each result was produced.
A candidate not covered by the baseline is UNCLASSIFIED ⇒ SUSPICIOUS ⇒ the guard fires.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # TheBridge/
OUT = Path(__file__).resolve().parent.parent / "results"

TOO_CLEAN = 1e-10
KEYWORDS = re.compile(r"byte-identical|resolution-independent|machine precision|1\.000000|"
                      r"1e-1[0-9]|1e-[2-9][0-9]|[0-9]\.[0-9]*e-1[0-9]", re.I)

# ---- frozen classification baseline: (path substring) -> (tag, reason) --------------------------------
# EXACT-OK = exact arithmetic or a provable exact symmetry; KNOWN-BUG = K2 (caught); CITED = sister-owned.
BASELINE = [
    ("legZ_jacobian",        "EXACT-OK",  "SymPy exact: det expands to −2 identically; rational collisions"),
    ("S1_schiemann",         "EXACT-OK",  "exact integer lattice arithmetic (theta counts, Siegel buckets)"),
    ("legY_ck",              "EXACT-OK",  "symbolic CK certificate (byte-identical = same polynomial)"),
    ("legU_kk6",             "EXACT-OK",  "within-shell degeneracy 0.00% = exact x↔y grid symmetry (Φ1=Φ2)"),
    ("legX_entropic/results","EXACT-OK",  "C1/C2 mpmath algebraic identities (εe^±2r) at dps=60; C3 Fock exact"),
    ("K1_squeezed",          "EXACT-OK",  "Fock-vs-Gaussian certification (both exact up to arithmetic prec.)"),
    ("K4_bumpy",             "EXACT-OK",  "exact symbolic GR (leftover-zero to all orders in ε)"),
    ("V1_relent",            "EXACT-OK",  "positivity to −6e-59 = mpmath round-off of a proven-nonneg quantity"),
    ("V3_flat_tori",         "EXACT-OK",  "SL(2,ℤ) control 1e-16 = isometric lattices by construction"),
    ("K2_isospectral",       "KNOWN-BUG", "the disconnected-grid triviality; exactness RETRACTED, caught by tabula"),
    # --- added after A1's first-run adjudication (each machine-precision value traced to its reason) ---
    ("M4_drum_coupling",     "EXACT-OK",  "uniform-coupling splits ~1e-13 = exact operator identity H=−∇²+cI "
                                          "(shifts all eigenvalues by c, preserves differences on ANY grid; "
                                          "NOT the K2 phantom — verified: M4 substance rebuilt on connected grid)"),
    ("K3_clausius_patch",    "EXACT-OK",  "K3d coherent control Σ/δQ=1.000000 = Longo's theorem exactly "
                                          "(displacement ⇒ ΔS=0 ⇒ Σ=δQ), same mechanism as K1's EXACT-OK"),
    ("K5_drum_learnability", "KNOWN-BUG", "prose quotes the K2 disconnected-grid bug (max|L₂−L₁|=0), not a new value"),
    ("V2_cft_calibration",   "EXACT-OK",  "gapped_pseudo_c 6e-11 = correct physics (gapped ⟹ c=0 control); "
                                          "R²=1.000000 = fit of the theoretically-exact CFT log-form (over-precise print)"),
]


def classify(path_str):
    for sub, tag, reason in BASELINE:
        if sub in path_str:
            return tag, reason
    return "UNCLASSIFIED", "no baseline entry — numerical-method exactness with no recorded construction reason"


def walk_json(obj, prefix=""):
    """Yield (keypath, value) for numeric leaves that are too-clean (0 < |x| < TOO_CLEAN)."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk_json(v, f"{prefix}/{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_json(v, f"{prefix}[{i}]")
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        if 0 < abs(obj) < TOO_CLEAN:
            yield prefix, obj


def main():
    print("A1 — the too-clean audit (gate frozen in PREREGISTRATION.md)\n")
    candidates = []          # (relpath, kind, detail)

    # ---- sweep results JSONs for too-clean numeric leaves
    for jf in sorted(ROOT.glob("**/results/*.json")):
        if "A1_tooclean" in str(jf):
            continue
        try:
            data = json.loads(jf.read_text())
        except Exception:
            continue
        for kp, val in walk_json(data):
            candidates.append((str(jf.relative_to(ROOT)), "json-value", f"{kp} = {val:g}"))

    # ---- sweep prose for exactness keywords
    for md in sorted(list(ROOT.glob("**/FINDINGS.md")) + list(ROOT.glob("**/PREREGISTRATION.md"))
                     + list(ROOT.glob("*.md"))):
        if "A1_tooclean" in str(md):
            continue
        for i, line in enumerate(md.read_text().splitlines(), 1):
            if KEYWORDS.search(line):
                candidates.append((str(md.relative_to(ROOT)), "prose", f"L{i}: {line.strip()[:90]}"))

    # ---- classify by source file
    tally = {}
    suspicious = []
    for relpath, kind, detail in candidates:
        tag, reason = classify(relpath)
        tally[tag] = tally.get(tag, 0) + 1
        if tag == "UNCLASSIFIED":
            suspicious.append((relpath, kind, detail))

    # ---- report grouped by source
    by_file = {}
    for relpath, kind, detail in candidates:
        by_file.setdefault(relpath, []).append((kind, detail))
    print(f"  swept {len(candidates)} too-clean candidates across {len(by_file)} files\n")
    print(f"  classification tally: {tally}\n")

    seen_files = sorted(by_file)
    for relpath in seen_files:
        tag, reason = classify(relpath)
        n = len(by_file[relpath])
        mark = {"EXACT-OK": "✅", "KNOWN-BUG": "🔧", "UNCLASSIFIED": "⚠️ SUSPICIOUS"}.get(tag, tag)
        print(f"  {mark:14} {relpath}  ({n} hits)")
        print(f"                 → {reason}")

    survived = len(suspicious) == 0
    print(f"\n  A1-gate: SUSPICIOUS (unclassified numerical exactness) = {len(suspicious)}")
    if suspicious:
        print("     the guard fired — audit these before trusting them:")
        for relpath, kind, detail in suspicious[:20]:
            print(f"        {relpath}: {detail}")
    print(f"     →  {'SURVIVES ✅ — every too-clean agreement is exact-by-construction or the caught K2 bug'
                     if survived else 'KILLED ❌ — a new too-clean numerical agreement lacks a construction reason'}")

    OUT.mkdir(exist_ok=True)
    (OUT / "audit.json").write_text(json.dumps({
        "too_clean_threshold": TOO_CLEAN, "n_candidates": len(candidates), "n_files": len(by_file),
        "tally": tally, "baseline": [{"match": s, "tag": t, "reason": r} for s, t, r in BASELINE],
        "suspicious": suspicious, "survived": survived,
        "verdict": ("Every machine-precision agreement in the bridge's corpus classifies as "
                    "exact-by-construction (SymPy/integer/symbolic/exact-symmetry) or the already-caught K2 "
                    "bug; no unexplained numerical-method exactness remains. Standing guard: a re-run "
                    "surfacing a candidate outside the baseline is a new suspect."
                    if survived else
                    "A too-clean numerical agreement with no construction reason was found — a K2-style bug "
                    "suspect; see suspicious list."),
    }, indent=1))
    print(f"\n  wrote results/audit.json")


if __name__ == "__main__":
    main()

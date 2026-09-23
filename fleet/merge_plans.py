"""Merge the six fleet plan lists into one register (2026-09-23).

Rules (FLEET_PLAN.md §1):
  * scores are the OWNER's where an owner scored the item; otherwise the proposer's
  * odds P = chance the item's STATED success criterion is met (one definition fleet-wide)
  * tabula's Chance is 1-5, converted by TABULA_P below -- PROVISIONAL, awaiting tabula's confirmation
  * moonshot index M = I x D x (1 - P)   (cuspis's bounded form; the user's original question)
  * portfolio value EV = I x P           (what to actually run)
Numbers are computed here, never typed by hand into the plan.
"""
TABULA_P = {1: .05, 2: .15, 3: .30, 4: .50, 5: .75}   # PROVISIONAL mapping

# (id, thread, item, owner, support, I, D, P, sources, status, note)
R = [
 # ---------------- K: hidden symmetry & integrability ----------------
 ("K1","K","Lorentzian vacuum rank>=3 Killing tensor, FUNCTIONALLY INDEPENDENT (or class-restricted no-go)","ansatz","tabula (N check)",5,5,.05,"ansatz#1, B-1, H-2","open; polynomial sense DONE (EXP-002, verified V5)",""),
 ("K2","K","Is SW-IV sigma=0 the only harmonic classified planar superintegrable potential?","ansatz","",2,2,.70,"H-3","open","bounds where K1 may look"),
 ("K3","K","Sealed blind numerical screen of the rank-3 vacuum object","tabula","ansatz supplies, sealed",3,2,.80,"H-1","open","3rd method after author (exact) and V5 (independent exact)"),
 ("K4","K","BUILD the proof instrument (Kovacic / Morales-Ramis) with controls ZV d=2 must fail, Kerr must pass","UNOWNED","ansatz supplies metrics",3,4,.60,"X-1","decision","unlocks K5-K8, K20"),
 ("K5","K","All-rank non-integrability of Manko-Novikov","K4 owner","ansatz E rung; tabula/quantum N rung",4,4,.25,"B-9","open; owner score pending","R-7: ansatz to score"),
 ("K6","K","Tomimatsu-Sato d=2: exact ranks 2-6 + Morales-Ramis attempt","ansatz","K4 owner (M side)",4,4,.40,"ansatz#9, A-9","open",""),
 ("K7","K","All-rank non-integrability for scalar-Gauss-Bonnet (higher-order VEs at O(zeta chi^2))","K4 owner","ansatz E lower rung",5,5,.10,"ansatz#3, A-3","after K5",""),
 ("K8","K","Is the dynamical Chern-Simons black hole integrable? (literature contradicts itself)","ansatz","K4 owner (M), tabula/quantum (N), bridge adjudicates",4.5,5,.15,"ansatz#4","open","R-11: was missing from the synthesis"),
 ("K9","K","Integrability tests at EMRI spins on an exact-in-spin O(coupling) substrate","ansatz","tabula (orbit chaos), deepstrain (QNMs)",4.5,4.5,.35,"ansatz#5","open",""),
 ("K10","K","A-priori bound on the pole order of a surviving rational integral (Kruglikov)","K4 owner","ansatz (counts)",4,4,.20,"ansatz#6","open","ansatz wants someone else to lead"),
 ("K11","K","Rational-integral search engine at finite deformation","ansatz","",4,4,.25,"ansatz#7","open",""),
 ("K12","K","Do Carter-keeping deformations keep it at SECOND order?","ansatz","tabula (drift screen)",4,4,.50,"ansatz#8","open",""),
 ("K13","K","Orbital fingerprint of algebraic integrability structures","tabula","ansatz supplies, sealed",4,3,.25,"ansatz#10","open","ansatz wants N to lead"),
 ("K14","K","Blind-recover the Papadopoulos-Kokkotas family, then screen outside it for rank 4","tabula","ansatz",5,5,TABULA_P[1],"tabula#1","open",""),
 ("K15","K","Separated-pair screen on ansatz's real deformed-Kerr catalogue","tabula","ansatz (catalogue, read-only)",3,3,TABULA_P[4],"tabula#16","open",""),
 ("K16","K","Geodesic Carter vs wave-equation separability","ansatz","deepstrain (R check)",3,3,.60,"ansatz#11","open",""),
 ("K17","K","One certificate format for exact nulls / proofs / certified numbers","ansatz","bridge (checker); all adopt",3,3,.85,"ansatz#14, X-2, tabula s166, V7","open",""),
 ("K18","K","delta-K library test (leg 6), sealed, on request","ansatz","bridge",3,2,.80,"ansatz#15","on request",""),
 ("K19","K","Computer-assisted proof of chaos in a black-hole spacetime","quantum","bridge; target from K5",5,5,.10,"B-5","after K5",""),
 ("K20","K","Numerically locate/certify Manko-Novikov's chaotic sea (feeds K19)","bridge","quantum",2,3,.50,"B-17, G4","open",""),
 ("K21","K","Closed-form rotating scalar-Gauss-Bonnet black hole","ansatz","",5,4,.015,"ansatz#2, B-2","PARKED until K22",""),
 ("K22","K","Blind rediscovery of the 2026 exact rotating hairy BH (control for K21)","ansatz","",3,4,.20,"B-11","open; owner score pending","R-7"),
 ("K23","K","Why the physical BH carries a principal tensor","UNOWNED","",5,5,.05,"B-4","PARKED (no owner)",""),
 # ---------------- Q: real data & QNMs ----------------
 ("Q1","Q","Quantum-ringdown / area-quantisation tail in GW250114","deepstrain","UNOWNED theory template",5,5,.01,"M1","blocked: no theory owner",""),
 ("Q2","Q","Eccentric subsolar search on O4","deepstrain","",5,5,.01,"M2","open",""),
 ("Q3","Q","Adjudicate the 5.4-sigma scalar-polarisation claim (ONE session only)","deepstrain","bridge (audit)",5,3,.70,"M6","open","P = clean answer; a REAL signal is <1%"),
 ("Q4","Q","Echo step-up: phase-marginalised likelihood + GWTC-5 + GW190521","deepstrain","",4,4,.02,"M9, B-19","open",""),
 ("Q5","Q","Isospectrality-breaking test on GW250114","deepstrain","ansatz (axial-polar splitting from METRICS)",4,4,.05,"M4, B-10a","open",""),
 ("Q6","Q","Re-score LVK's O4a subsolar trigger list","deepstrain","",3.5,2,.05,"M11, B-18","NEXT UP",""),
 ("Q7","Q","S251112cm tidal PBH discriminator","deepstrain","",5,4,.20,"M5","blocked: strain not public",""),
 ("Q8","Q","Independent test of GW250114 'direct wave' (Nature 2026)","deepstrain","",5,4,.25,"M3","open",""),
 ("Q9","Q","GW-memory stacking cross-check","bridge","deepstrain",4,4,.20,"M10","open","deepstrain: suits a statistics-audit lane"),
 ("Q10","Q","Nonlinear quadratic mode in GW250114","deepstrain","",4,5,.30,"M8","open",""),
 ("Q11","Q","GW231123 ringdown (microglitch preflight first)","deepstrain","",3,3,.15,"M13","open",""),
 ("Q12","Q","Is the GWTC-4 GR tension a finite-SNR bias?","bridge","deepstrain (injections)",4,3,.40,"M7","open","deepstrain: suits a statistics session"),
 ("Q13","Q","Train the NPE on IMR/NR waveforms","deepstrain","",3,4,.50,"M12","open",""),
 ("Q14","Q","Fine-timing hybrid trigger-to-verify coincidence","deepstrain","",3,3,.50,"M14","open",""),
 ("Q15","Q","Deep-FAR estimator-bias methods note","deepstrain","bridge (review)",3,2,.80,"M15","open",""),
 ("Q16","Q","Pole structure of the sGB QNM spin series","deepstrain","ansatz (symbolic check)",2,3,.50,"B-15","open",""),
 ("Q17","Q","L3 null vs the orthonormal-mode GW250114 analysis","deepstrain","",3,2,.60,"B-16","open; owner score pending","R-8"),
 ("Q18","Q","Table-reproduction audit of recent GR/QNM papers","deepstrain","ansatz",2,1,.80,"B-20","open",""),
 ("Q19","Q","GR from real astronomy data (S2 / Hulse-Taylor)","tabula","deepstrain may claim",4,4,TABULA_P[2],"tabula#6","open",""),
 # ---------------- C: corner entanglement ----------------
 ("C1","C","Absolute upper bound on kappa/C_T","cuspis","",5,5,.03,"CF-1","open",""),
 ("C2a","C","Why the corner band is narrow -- tripartite-information route","cuspis","",5,5,.05,"CF-2, B-3","open","METHOD SPLIT with C2b"),
 ("C2b","C","Why the corner band is narrow -- bound + remainder route","quantum","",5,4,.15,"V3, B-3","open","METHOD SPLIT with C2a"),
 ("C3","C","First von Neumann kappa for an interacting CFT (Ising)","UNOWNED","",5,5,.08,"CF-3","PARKED (no instrument)",""),
 ("C4","C","Corner entanglement on the fuzzy sphere","UNOWNED","",5,5,.10,"CF-4, V4","PARKED (no instrument)",""),
 ("C5","C","1/N correction to kappa/C_T for large-N O(N)","cuspis","",4,5,.10,"CF-5","open (open to anyone)",""),
 ("C6","C","Test the theta^{2eta} small-angle term at Ising/O(N)","UNOWNED","",4,5,.10,"CF-6","PARKED (new instrument)",""),
 ("C7","C","Numerical bootstrap of the n=2 replica twist line","UNOWNED","",4,5,.10,"CF-7","PARKED (no instrument)",""),
 ("C8","C","Non-perturbative / top-down holographic corner function","cuspis","",4,5,.15,"CF-8","open (open to anyone)",""),
 ("C9","C","Prove the rectangle bound / concavity at n=1","cuspis","",4,4,.20,"CF-9","open",""),
 ("C10","C","What orders kappa/C_T across theories","cuspis","",3,4,.10,"CF-10","open",""),
 ("C11","C","Reflection positivity of the corner function at n=1","cuspis","",3,4,.15,"CF-11","open",""),
 ("C12","C","A SECOND instrument for free-field values below 45 deg","UNOWNED","",3,4,.35,"CF-12, V8, B-13","decision","lattice route infeasible (R-3); V8 awaits amendment"),
 ("C13","C","Independent analytic a0 for the free scalar (incl. log theta)","cuspis","",3,4,.40,"CF-13","open",""),
 ("C14","C","Identify the Painleve system behind the Casini-Huerta ODEs","quantum","tau-function side OPEN",5,5,.05,"V1","open",""),
 ("C15","C","Closed form for a(theta) via PSLQ","quantum","",5,5,.075,"V2","open",""),
 ("C16","C","kappa to 30 digits via Painleve V","quantum","",4,4,.80,"V5","awaits amendment decision?","closed form is a 20% stretch"),
 ("C17","C","Test the new cusp-bootstrap inequalities (ONE owner)","cuspis","quantum: precision scalar coeffs, non-independent",3,1,.90,"CF-22, V6","NEXT UP","R: duplicate resolved to cuspis"),
 ("C18","C","Certified (interval-arithmetic) a(pi/2)","quantum","",3,4,.40,"V7","open","shares tooling with K19"),
 ("C19","C","Fifth out-of-family regulator (lattice)","quantum","",3,3,.50,"V9","open",""),
 ("C20","C","Continuum a(2pi/3), a(pi/3)","quantum","",3,1,.95,"V11","NEXT UP",""),
 ("C21","C","Is Ising's Renyi-2 corner function a multiple of free?","cuspis","",3,2,.60,"CF-17","open",""),
 ("C22","C","Scalar run to masses >=14 (reach 5-10 deg)","cuspis","",2,2,.70,"CF-18","open",""),
 ("C23","C","Quantum Darwinism in a critical environment","quantum","",4,4,.15,"H3, B-8","not yet well-posed",""),
 ("C24","C","kappa/F0 normalisation audit and the kappa/F0 <= 0.622 conjecture","bridge","cuspis",2,1,.90,"CF-23","open","cuspis suggested the bridge"),
 # ---------------- L: representation learning (tabula) ----------------
 ("L1","L","Walrus 'murky physics' explained by the legibility law","tabula","Phronesis (real-model gate)",5,5,TABULA_P[2],"tabula#2","open",""),
 ("L2","L","Embodied RL agent in curved spacetime","tabula","",5,5,TABULA_P[2],"tabula#3","open",""),
 ("L3","L","Learned time-dependent geometry (road to a discovered GW)","tabula","",5,4,TABULA_P[2],"tabula#4","open",""),
 ("L4","L","Discover the field law (Phase F)","tabula","",5,4,TABULA_P[2],"tabula#5","open",""),
 ("L5","L","Grid cells in curved worlds","tabula","",4,4,TABULA_P[3],"tabula#7","open",""),
 ("L6","L","Legibility -> deployment (causal use)","tabula","",5,3,TABULA_P[3],"tabula#8","open",""),
 ("L7","L","Kepler -> Newton transformers read with emit-or-certify","tabula","",5,3,TABULA_P[3],"tabula#9","open",""),
 ("L8","L","Does an LLM hold a light cone?","OPEN-SEAT","Phronesis?",3,3,TABULA_P[1],"tabula#10","open",""),
 ("L9","L","3+1 Kaluza-Klein with a vector potential","tabula","quantum (target, blind)",3,4,TABULA_P[3],"tabula#11","open",""),
 ("L10","L","KK structural form via stabilized LNNs","tabula","",4,3,TABULA_P[3],"tabula#12","open",""),
 ("L11","L","Larger symmetry-respecting generalist + legibility regularizer (GPU)","tabula","",3,4,TABULA_P[3],"tabula#13","open",""),
 ("L12","L","Public discoverability benchmark (all repos' certified nulls/positives)","tabula","all supply cases",4,3,TABULA_P[4],"tabula#14, B-12","open",""),
 ("L13","L","Hashimoto depth-as-bulk, identifiability angle","OPEN-SEAT","",2,3,TABULA_P[4],"tabula#15","open",""),
 ("L14","L","Stress-test NGCL with the certificate standard","tabula","",3,2,TABULA_P[4],"tabula#18","open",""),
 ("L15","L","C-anomaly follow-ups + scored-direction readout","tabula","",3,2,TABULA_P[4],"tabula#19","open",""),
 ("L16","L","Synthesis write-up (three months)","tabula","",4,2,TABULA_P[5],"tabula#21","open",""),
 # ---------------- F: fleet epistemics ----------------
 ("F1","F","How errors propagate in an AI research fleet -- measured case study","bridge","all supply dated entries",4,2,.60,"B-14","open",""),
 ("F2","F","Fleet-wide settled-results index (plans checked against it before shipping)","bridge","each repo keeps a settled table",3,2,.90,"FLEET_ANALYSIS s5","open",""),
 ("F3","F","One outside specialist reads EXP-002","USER","",5,1,.50,"H-5","decision","only the user can do this"),
]

def M(r): return r[5]*r[6]*(1-r[7])
def EV(r): return r[5]*r[7]
def pct(p): return f"{p*100:.1f}%" if p < .1 else f"{p*100:.0f}%"

if __name__ == "__main__":
    import json, pathlib
    out = pathlib.Path(__file__).with_name("merged_register.json")
    out.write_text(json.dumps([dict(zip(["id","thread","item","owner","support","I","D","P","sources","status","note"], r)) | {"M": round(M(r),2), "EV": round(EV(r),2)} for r in R], indent=1))
    print(f"{len(R)} merged items -> {out.name}")
    active = [r for r in R if "PARKED" not in r[9]]
    print("\nMOONSHOT VIEW (M = I*D*(1-P)), top 12, excluding parked:")
    for r in sorted(active, key=M, reverse=True)[:12]:
        print(f"  {r[0]:4} M={M(r):5.2f}  I{r[5]:<3} D{r[6]:<3} P{pct(r[7]):>5}  {r[3]:10}  {r[2][:70]}")
    print("\nPORTFOLIO VIEW (EV = I*P), top 14:")
    for r in sorted(active, key=EV, reverse=True)[:14]:
        print(f"  {r[0]:4} EV={EV(r):4.2f}  I{r[5]:<3} D{r[6]:<3} P{pct(r[7]):>5}  {r[3]:10}  {r[2][:70]}")
    from collections import Counter
    print("\nITEMS BY OWNER:", dict(Counter(r[3] for r in R)))

def write_register(path="REGISTER.md"):
    import pathlib
    names = {"K": "K — hidden symmetry & integrability", "Q": "Q — real data & QNMs",
             "C": "C — corner entanglement", "L": "L — representation learning", "F": "F — fleet epistemics"}
    lines = ["# Fleet register — all 86 merged items (GENERATED by `merge_plans.py`; do not edit by hand)", "",
             "*I = impact, D = difficulty (1–5, owner's scores). P = chance the stated success criterion is met.",
             "M = I×D×(1−P), the moonshot index. EV = I×P, portfolio value. tabula's P values use a PROVISIONAL",
             "1–5 → probability mapping (1:5%, 2:15%, 3:30%, 4:50%, 5:75%), pending tabula's confirmation.*", ""]
    for t, title in names.items():
        lines += [f"## {title}", "", "| ID | Item | Owner | Support | I | D | P | M | EV | Status | Sources |",
                  "|---|---|---|---|:-:|:-:|:-:|:-:|:-:|---|---|"]
        for r in sorted([r for r in R if r[1] == t], key=M, reverse=True):
            lines.append(f"| {r[0]} | {r[2]}{(' — *' + r[10] + '*') if r[10] else ''} | {r[3]} | {r[4] or '—'} | "
                         f"{r[5]} | {r[6]} | {pct(r[7])} | {M(r):.1f} | {EV(r):.2f} | {r[9]} | {r[8]} |")
        lines.append("")
    pathlib.Path(__file__).with_name(path).write_text("\n".join(lines) + "\n")
    print(f"wrote {path}")

write_register()

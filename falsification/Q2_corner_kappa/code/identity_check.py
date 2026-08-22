"""ansatz's identity question, applied to my own checkpoint.

Recoverability and auditability are not the same as IDENTITY: a resume that draws
a different valid computation gives an EQUIVALENT result, not THE result that was
interrupted. They verified theirs differentially (bit-identical sha256 across a
kill/resume) rather than reasoning about it.

grep says there is no randomness in the s=5 path, so identity should hold by
construction. That is an inference. This is the measurement.
"""
import numpy as np, hashlib, sys
sys.path.insert(0,'.')
from entropy import correlators
from s5_run import entropy_big

L, m, ls = 800, 0.002, list(range(20,101,10))
z = np.load('../s5_spectra.npz', allow_pickle=True)
h = lambda spec: hashlib.sha256(b''.join(np.asarray(a,dtype=np.float64).tobytes()
                                         for a in spec)).hexdigest()[:16]
print("recomputing 'nn' from scratch and comparing to the banked spectrum...", flush=True)
X, P = correlators(L, m, 'nn')
fresh = [entropy_big(X, P, l, L) for l in ls]
hb, hf = h(z['nn']), h(fresh)
print(f"  banked nn sha256[:16] = {hb}")
print(f"  fresh  nn sha256[:16] = {hf}")
print(f"  BIT-IDENTICAL: {hb == hf}")
print(f"  => checkpoint has IDENTITY, not merely equivalence" if hb==hf
      else "  => EQUIVALENT ONLY — recovered spectrum is not the one interrupted")

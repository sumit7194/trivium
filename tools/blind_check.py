#!/usr/bin/env python3
"""Pre-send blinding guard. Usage: blind_check.py <recipient> <file-with-message-text>  (or '-' for stdin).
Exit 1 and print every match if the text hits an active embargo for that recipient ('*' embargoes apply to all).
Rule (bridge, 2026-10-18, after two C0 slips): every cross-session message is drafted to a file and must pass this
check before SendMessage. Embargoes live in tools/EMBARGOES.json; remove one only when its seal arrives."""
import sys, re, json, os
rec, path = sys.argv[1], sys.argv[2]
text = sys.stdin.read() if path == '-' else open(path).read()
E = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'EMBARGOES.json')))['embargoes']
# Recipient matching FAILS CLOSED (fix 2026-11-18): a short name ('ansatz') or a bare uds socket address
# ('uds:/tmp/cc-socks/66386.sock') used to match no embargo, so the check passed vacuously.
# Now: a name applies an embargo if either is a prefix of the other; a recipient that matches no known
# sister name gets EVERY embargo applied.
KNOWN = ['ansatz-machine', 'tabula-geometrica', 'cuspis', 'quantum', 'deepstrain', 'vestigium', 'spherex']
def norm(x): return x.strip().lower().split(' [')[0]
def same(a, b): a, b = norm(a), norm(b); return len(a) >= 4 and len(b) >= 4 and (a.startswith(b) or b.startswith(a))
known = any(same(rec, k) for k in KNOWN + [e['recipient'] for e in E if e['recipient'] != '*'])
if not known: print('NOTE: recipient', repr(rec), 'not recognised -> applying ALL embargoes (fail closed)')
hits = []
for e in E:
    r = e['recipient']
    if r != '*' and known and not same(rec, r): continue
    for p in e['patterns']:
        for m in re.finditer(p, text, re.I):
            hits.append((e['id'], m.group(0)[:120]))
if hits:
    print('BLOCKED: message hits active embargo(es):')
    for i, h in hits: print(f'  [{i}] ...{h}...')
    sys.exit(1)
print('OK: no embargo hits for', rec)

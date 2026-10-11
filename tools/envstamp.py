"""Environment stamp for reproducibility: interpreter, platform, key package versions, BLAS/LAPACK backend, git commit.
Usage: python tools/envstamp.py [out.json]   (or import envstamp; envstamp.stamp() -> dict to embed in results JSON)"""
import sys, json, platform, subprocess, importlib, io, contextlib, os

PKGS = ['numpy', 'scipy', 'sympy', 'mpmath', 'numba', 'llvmlite', 'flint', 'torch']

def _blas():
    out = {}
    for mod in ('numpy', 'scipy'):
        try:
            m = importlib.import_module(mod); cfg = m.show_config(mode='dicts')
            dep = cfg.get('Build Dependencies', {})
            out[mod] = {k: dep.get(k, {}).get('name') for k in ('blas', 'lapack')}
        except Exception as e:
            out[mod] = {'error': repr(e)}
    return out

def _git(path='.'):
    try:
        c = subprocess.run(['git', '-C', path, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
        d = subprocess.run(['git', '-C', path, 'status', '--porcelain'], capture_output=True, text=True).stdout.strip()
        return {'commit': c, 'dirty': bool(d)}
    except Exception as e:
        return {'error': repr(e)}

def stamp(repo='.'):
    v = {}
    for p in PKGS:
        try: v[p] = importlib.import_module(p).__version__
        except Exception: v[p] = None
    return dict(python=sys.version.split()[0], executable=sys.executable, implementation=platform.python_implementation(),
                platform=platform.platform(), machine=platform.machine(), packages=v, blas_lapack=_blas(), git=_git(repo))

if __name__ == '__main__':
    s = stamp(); out = json.dumps(s, indent=1); print(out)
    if len(sys.argv) > 1: open(sys.argv[1], 'w').write(out + '\n')

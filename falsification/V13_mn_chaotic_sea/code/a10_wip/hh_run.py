import sys, time
sys.path.insert(0, '/Users/sumit/Github/TheBridge/falsification/V13_mn_chaotic_sea/code')
import v13_a10_multishoot as M
T0=time.time(); out=M.hh_control(lambda *a: print(f'[{time.time()-T0:7.1f}]', *a, flush=True))
print('pos', out['positive_control_passes'], 'neg', out['negative_control_passes'], out['n_confirmed_self_loops'])

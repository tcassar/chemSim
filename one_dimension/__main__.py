from atom import Atom
from potential import Potential
from decimal import Decimal as d
import time

ar1, ar2 = Atom(d('0.5'), 0), Atom(d('-0.5'), 0)
intr = Potential(ar1, ar2)

log_frames = 7

if __name__ == '__main__':
    start = time.time()
    for i in range(10**log_frames):
        if not i % 10**(log_frames - 1):
            print(intr.split_force(report=True))
    print(f'Completed 1x10^{log_frames} in {time.time() - start}')


import src.atom as atom
from one_dimension.atom import Atom as onedAtom
from one_dimension.potential import Potential
import src.interaction as interaction
from src.utils import mylog
import time


# TODO: Debug force gen
# TODO: Proper RU Mode vs real mode
# TODO: Make sure two particles never overlap position


def atom_init(i=None, j=None):
    if not i:
        i = [2 * [0, 0]]
    if not j:
        j = [[1, 1], [0, 0]]

    ar_i = atom.Atom(*i)
    ar_j = atom.Atom(*j)

    return ar_i, ar_j


def cycle_to_file(frames, ops_per_frame):
    # 100 frames, 1000 ops per frame
    ar1, ar2 = atom.Atom([4, 5]), atom.Atom([6, 8])

    print(f'Ar1: {ar1}')
    print(f'Ar2: {ar2}')

    intr = interaction.Interaction(ar1, ar2)
    with open('../logs/interaction_cycle.log', 'w') as f:
        for i in range(frames * ops_per_frame):
            if not i % ops_per_frame:
                mylog(f'===FRAME {i}===\n', f)
                mylog(f'Distance: {intr.distance():.4f}\n', f)
                mylog(f'LJ Energy (J): {intr.lj_energy():.4f}\n', f)
                mylog(f'LJ Force (N): {intr.lj_force(): .4f}\n', f)
                intr.delegate_force()

                mylog('\n', f)
                mylog(f'Ar1 Vitals: {ar1}\n', f)
                mylog(f'Ar2 Vitals: {ar2}\n', f)
                mylog(f'Time since last out: {time.time() - frames}', f)
                mylog('\n', f)


def cycle(n) -> time:
    ar1, ar2 = atom.Atom([4, 5]), atom.Atom([-4, -5])
    intr = interaction.Interaction(ar1, ar2)

    start = time.time()
    for i in range(n):
        intr.delegate_force()

    print(ar1)
    print(ar2)

    return time.time() - start


def oned_run(frames):
    atm1 = onedAtom(1, 0)
    atm2 = onedAtom(-1, 0)
    potential = Potential(atm1, atm2)

    for i in range(frames):
        print(potential.split_force(report=True))


if __name__ == '__main__':
    oned_run(10)

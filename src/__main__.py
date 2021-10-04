import src.atom as atom
import src.interaction as interaction
from src.utils import mylog


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
    intr = interaction.Interaction(ar_i, ar_j)

    return ar_i, ar_j


def cycle_to_file():
    ar1, ar2 = atom.Atom([4, 5]), atom.Atom([6, 8])

    print(f'Ar1: {ar1}')
    print(f'Ar2: {ar2}')

    intr = interaction.Interaction(ar1, ar2)

    with open('../logs/interaction_cycle.log', 'w') as f:
        for i in range(100000):
            if not i % 1000:
                mylog(f'===FRAME {i}===\n', f)
                mylog(f'Distance: {intr.distance():.4f}\n', f)
                mylog(f'LJ Energy (J): {intr.lj_energy():.4f}\n', f)
                mylog(f'LJ Force (N): {intr.lj_force(): .4f}\n', f)
                intr.delegate_force()

                mylog('\n', f)
                mylog(f'Ar1 Vitals: {ar1}\n', f)
                mylog(f'Ar2 Vitals: {ar2}\n', f)
                mylog('\n', f)


def cycle():
    ar1, ar2 = atom.Atom([4, 5]), atom.Atom([-4, -5])
    intr = interaction.Interaction(ar1, ar2)

    def update():
        intr.delegate_force()

    for i in range(100):
        update()


if __name__ == '__main__':
    ar_i, ar_j = atom_init()
    print(ar_i, ar_j)
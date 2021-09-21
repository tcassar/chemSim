import atom
import interaction
from utils import mylog
import timeit

# TODO: Make sure two particles never overlap position
# TODO: Proper RU Mode vs real mode


def main():
    ar1, ar2 = atom.Atom([4, 5]), atom.Atom([6, 8])

    print(f'Ar1: {ar1}')
    print(f'Ar2: {ar2}')

    intr = interaction.Interaction(ar1, ar2)

    with open('interaction_cycle.log', 'w') as f:
        for i in range(100):
            mylog(f'===FRAME {i}===\n', f)
            mylog(f'Distance: {intr.distance():.4f}\n', f)
            mylog(f'LJ Energy (J): {intr.lj_energy():.4f}\n', f)
            mylog(f'LJ Force (N): {intr.lj_force(): .4f}\n', f)
            intr.delegate_force(v=True)

            mylog('\n', f)
            mylog(f'Ar1 Vitals: {ar1}\n', f)
            mylog(f'Ar2 Vitals: {ar2}\n', f)
            mylog('\n', f)


if __name__ == '__main__':
    main()
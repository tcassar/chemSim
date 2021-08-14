import atom
import interaction

if __name__ == '__main__':
    ar1, ar2 = atom.Atom(), atom.Atom()
    ar1.update_s(3, 4)
    ar2.update_s(6, 8)

    # print(f'Ar1 Vitals: {ar1.vitals()}')
    # print(f'Ar2 Vitals: {ar2.vitals()}')

    intr = interaction.Interaction(ar1, ar2)
    print(f'Distance: {intr.distance()}')
    print(f'LJ Energy (K): {intr.lj_energy()}')

    ar1.update_s(3, 4)
    ar2.update_s(6, 8)

    print(f'Distance: {intr.distance()}')
    print(f'LJ Energy (K): {intr.lj_energy()}')

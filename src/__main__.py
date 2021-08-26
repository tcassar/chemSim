import atom
import interaction

# TODO: Everything needs tests written: research how one tests
# TODO: Make sure two particles never overlap position

if __name__ == '__main__':
    ar1, ar2 = atom.Atom([4, 5]), atom.Atom([6, 8])

    print(f'Ar1: {ar1}')
    print(f'Ar2: {ar2}')

    intr = interaction.Interaction(ar1, ar2)
    print(f'Distance: {intr.distance():.4f}')
    print(f'LJ Energy (J): {intr.lj_energy():.4f}')
    print(f'LJ Force (N): {intr.lj_force(): .4f}')
    intr.delegate_force(v=True)

    print(f'Ar1 Vitals: {ar1}')
    print(f'Ar2 Vitals: {ar2}')
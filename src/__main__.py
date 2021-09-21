import atom
import interaction
from utils import mylog

# TODO: Make sure two particles never overlap position
# TODO: Proper RU Mode vs real mode

if __name__ == '__main__':
    ar1, ar2 = atom.Atom([4, 5]), atom.Atom([6, 8])

    print(f'Ar1: {ar1}')
    print(f'Ar2: {ar2}')

    intr = interaction.Interaction(ar1, ar2)
    
    with open('interaction_cycle.txt', 'w') as f:     
        for i in range(100):
            mylog(f'Distance: {intr.distance():.4f}', f)
            mylog(f'LJ Energy (J): {intr.lj_energy():.4f}', f)
            mylog(f'LJ Force (N): {intr.lj_force(): .4f}', f)
            intr.delegate_force(v=True)
        
            mylog(f'Ar1 Vitals: {ar1}', f)
            mylog(f'Ar2 Vitals: {ar2}', f)

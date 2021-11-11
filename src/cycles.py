from environment import Container
from potential import Potential
from decimal import Decimal
from datetime import datetime
import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from atom import Atom


def pairwise_cycle(container: Container) -> str:
    """
    Pairwise cycle runs as follows:
    SETUP:
        Assert len of atom list is 2
        Initialise static potential between atoms
    CYCLE:
        Potential.split_force()
        atoms.move() for atom in atoms
        log to file

    Important to track average distance between atoms every 1000 cycles
    """

    # Check length
    atoms: list[Atom] = container.contained_atoms
    print(atoms)
    assert len(atoms) == 2
    potential = Potential(*atoms)
    res: Decimal = 1 / (Decimal('10') ** 7)
    avg_r = Decimal('0')

    frames = 10000

    with open(f'../logs/runs/{datetime.now()}.log', 'w') as f:
        for i in range(1, 101):
            for j in range(frames):
                # delegate forces, save distance (r) for logging
                r: Decimal = potential.split_force()
                avg_r += r
                # res = np.sqrt(r) / 10 ** 6
                for atom in atoms:
                    atom.move(res)
            out = potential.report()
            f.write(out)
            print(out)

        avg = avg_r / (frames * 100)
        error_avg = avg / ( np.power(Decimal(2), Decimal(1) / 6) * potential.sigma)
        f.write(f'\nAverage distance: {avg:.7f}')
        f.write(f'% Error: {abs(1-error_avg)*100}')
        return f'{abs(1-error_avg)*100}'


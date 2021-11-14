from src.atom import Atom
import src.cycles
from src.environment import Container
from src.potential import Potential
from decimal import Decimal
import datetime
import logging


def compute_frame(atoms: list[Atom], resolution: Decimal):
    for atom in atoms:
        atom.move(resolution)


def two_atm_init():
    ar1, ar2 = Atom(Decimal('0.25'), 0, ID=1), Atom(Decimal('-0.25'), 0, ID=2)
    intr = Potential(ar1, ar2)

    walls = [Decimal(-1.1), Decimal(1.1)]
    ctr = Container(walls)
    ar1.inject_to(ctr)
    ar2.inject_to(ctr)

    print(ar1, ar2)
    return intr, ar1, ar2

def two_atom_uncontained():
    intr, *atoms = two_atm_init()
    log_frames = 8

    while True:
        for i in range(10 ** log_frames):
            if not i % 10 ** (log_frames - 2):
                intr.split_force()
                compute_frame(atoms, Decimal('0.001'))
                print(intr)


def three_atom():

    walls = [Decimal(-1.1), Decimal(1.1)]
    ctr = Container(walls)

    # Create atoms
    atoms = []
    for i in range(3):
        atm = Atom(Decimal(f'0.{4*i}'), 0, ID=i + 1)
        atoms.append(atm)
        atm.inject_to(ctr)

    # Setup potentials
    atm1, atm2, atm3 = atoms
    intr12 = Potential(atm1, atm2)
    intr23 = Potential(atm2, atm3)
    intr13 = Potential(atm1, atm3)

    intrs = [intr12, intr13, intr23]

    log_frames = 8

    while True:
        for i in range(10 ** log_frames):
            if not i % 10 ** (log_frames - 2):
                for intr in intrs:
                    intr.split_force()

                for atom in atoms:
                    atom.move(Decimal(0.001))

                print(*intrs)


def pairwise_cycle_test():

    # Initialise atoms, assign to a container

    atoms = [Atom(Decimal('0.38'), Decimal('-0.0005'), ID=1), Atom(Decimal('0'), Decimal('0.0005'))]

    walls = [Decimal(-10.1), Decimal(10.1)]
    ctr = Container(walls)
    for atom in atoms:
        atom.inject_to(ctr)

    return src.cycles.pairwise_cycle(ctr, time=Decimal('0.1'), datapoints=100)



if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')
    logging.info(f'File to write to configured: STDOUT')

    start = datetime.datetime.now()
    pairwise_cycle_test()
    logging.info(f'Completed in {datetime.datetime.now() - start}')

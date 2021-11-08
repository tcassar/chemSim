# Sets up objects that affect physical env of sim, such as container boundaries, temperature control, etc.

from atom import Atom
from potential import Potential
from decimal import Decimal
from dataclasses import dataclass
import numpy as np
from typing import Union


@dataclass
class Wall:
    pos: Decimal


class Container:
    # Scale
    # Constructs container via walls, for now 1d thus max 2 walls

    def __init__(self, walls: list[Decimal]):
        made_walls = []
        walls.sort()
        for wall in walls:
            # Scale: Needs to work with multiple dimensions, by accepting [[x, x], [y, y], [z, z]]
            made_walls.append(Wall(wall))

        self.walls = made_walls
        # Walls are sorted in [left, right] per dimension

        self.contained_atoms: list = []

    def __repr__(self):
        return f'Container(walls={self.walls}'

    def add_atom(self, atom: Union[Atom, list[Atom]]):
        """Adds atom to running container list"""
        self.contained_atoms.append(atom)

    def out_of_bounds(self, atom_pos: Decimal, res=Decimal('0.0001')) -> Decimal:
        """If molecule is out of bounds, return a correction.
        If missed lower bound, returns 1. If upper, returns -1. If neither, returns new position for atom"""
        lower, *_, upper = self.walls  # *_ is redundant as will always be len(2), just makes clear

        if atom_pos < lower.pos:
            adjustment = lower.pos + res
            # print("Lower wall hit")
        elif atom_pos > upper.pos:
            adjustment = upper.pos - res
            # print("Upper wall hit")
        else:
            return Decimal(0)

        return adjustment

    def pairwise_cycle(self):
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
        atoms = self.contained_atoms
        print(atoms)
        assert len(atoms) == 2
        potential = Potential(*atoms)
        res: Decimal = Decimal('0.00001')
        avg_r = 0

        frames = 10000

        with open('../logs/precalibrated.log', 'w') as f:
            for i in range(1, 101):
                for j in range(frames):
                    # delegate forces, save distance (r) for logging
                    r = potential.split_force()
                    avg_r += r
                    res = np.sqrt(r)/10**7
                    for atom in atoms:
                        atom.move(res)
                out = f'====FRAME {frames*i}====\nAvg Distance: {avg_r / frames :.4f}; res {res}\n'
                print(out)
                f.write(out)

            f.write(f'{avg_r / frames*100}')



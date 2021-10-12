from atom import Atom
from decimal import Decimal
import numpy as np


class Potential:

    def __init__(self, mol1: Atom, mol2: Atom):
        self.mol1 = mol1
        self.mol2 = mol2

    def distance(self):
        mol1, mol2 = self.mol1, self.mol2
        distance = Decimal(mol1.vitals()[0]) - Decimal(mol2.vitals()[0])
        if not distance:
            distance = Decimal(10 ** -4)
        else:
            distance = distance

        return distance

    def _lj_energy(self) -> Decimal:
        """
        Calculate energy from Lennard Jones Potential
        """
        epsilon = 1
        sigma = 1
        r: Decimal = self.distance()
        x: Decimal = sigma / r

        repulsive = np.power(x, 12)
        attractive = np.power(x, 6)

        return 4 * epsilon * (repulsive - attractive)

    def _lj_force(self) -> Decimal:
        """Calculate force by differentiating LJ Potential"""
        r: Decimal = self.distance()
        e: Decimal = Decimal(1)
        s: Decimal = Decimal(1)

        a = Decimal((24 * e * np.power(s, 6)) * np.power(r, -7))
        b = Decimal((2 * np.power(s, 6)) * np.power(r, -6) - 1)

        return a * b

    def split_force(self, *, report=False) -> str:
        """ Delegates equal and opposite force to two atoms. Also detects collisions"""
        # TODO: Decouple this from Atom .move()
        force = self._lj_force()
        self.mol1.move(force)
        self.mol2.move(force * -1)

        return self._report(self.distance, force, self._lj_energy()) if report else ''

    def _report(self, distance, force, energy):

        # TODO: Allow reporting from outside function i.e. turn into method

        """Debug output"""

        out = f'\n======\nDistance: {distance()}\nEnergy: {energy}\nForce: {force}\n'
        out += f'Particle A: {self.mol1}\n'
        out += f'Particle B: {self.mol2}'
        out += '\n======'

        return out

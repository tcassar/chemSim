from atom import Atom
from decimal import Decimal
import numpy as np
import xxhash


class Potential:

    def __init__(self, mol1: Atom, mol2: Atom):
        # TODO: log on creation
        self.mol1 = mol1
        self.mol2 = mol2

        self.distance = self.eval_distance()

    def __hash__(self) -> int:
        """Potential's hash is built from concatenating mol IDs"""
        x = xxhash.xxh32()
        x.update(bytes(f'{self.mol1.ID}{self.mol2.ID}'))
        return x.intdigest()

    def __str__(self):
        mol1 = self.mol1
        mol2 = self.mol2
        if mol1.get_pos() > mol2.get_pos():
            mol1, mol2 = mol2, mol1
        return f'Atom{mol1.get_ID()} {mol1.get_pos():.4f}...[{self.distance:.4f}]' \
               f'...Atom{mol2.get_ID()} {mol2.get_pos():.4f}'

    def __del__(self):
        # TODO: Log on destruction
        pass

    # ==== TIME ====

    @staticmethod
    def _eval_time(t: Decimal) -> Decimal:
        """ For the moment keep this constant"""
        return t if t else Decimal('0.01')

    def set_time(self, t: Decimal):
        """sets time to t"""
        self._eval_time(t)

    # ==== DISTANCE ====

    def eval_distance(self) -> Decimal:
        # Scale through defining type for v and s, allowing arithmetic between types
        """
        Updates self.distance variable - done to mean that distance only calculated once per frame
        """
        mol1, mol2 = self.mol1, self.mol2
        distance = abs(Decimal(mol1.get_pos()) - Decimal(mol2.get_pos()))
        if not distance:
            distance = Decimal('10') ** -4
        else:
            distance = distance

        self.distance = distance
        return distance

    # ==== MOTION ====

    def _lj_energy(self) -> Decimal:
        """
        Calculate energy from Lennard Jones Potential
        """
        # TODO: Log when calculated
        epsilon = 1
        sigma = 1
        r: Decimal = self.distance
        x: Decimal = sigma / r

        repulsive = np.power(x, 12)
        attractive = np.power(x, 6)

        return 4 * epsilon * (repulsive - attractive)

    def _lj_force(self) -> Decimal:
        """Calculate force by differentiating LJ Potential"""
        # TODO: Log when calculated
        r: Decimal = self.distance
        e: Decimal = Decimal('1.1')
        s: Decimal = Decimal('1')

        a = Decimal((24 * e * np.power(s, 6)) * np.power(r, -7))
        b = Decimal((2 * np.power(s, 6)) * np.power(r, -6) - 1)

        return a * b

    # ==== COLLISION HANDLING ====
    # i.e. how to deal with a collision AFTER detection BETWEEN PARTICLES
    # Potential is not concerned with collisions with sides of containers, that is handled by Atom class

    def _mols_collision(self) -> str:
        """
        Corrects particles in case of collision. This is a collision, will not theoretically happen but may here due to
        approx of var acceleration.

        Swap positions, elastic collision, particles of same mass => velocity *= -1.
        """

        # Scale: check maths

        # unpack molecules to local scope
        mol1, mol2 = self.mol1, self.mol2

        # Invert Velocities, elastic collisions
        v1, v2 = mol1.get_v(), mol2.get_v()
        mol1.set_v(v1 * -1)
        mol2.set_v(v2 * -1)

        # Swap positions
        s1, s2 = mol2.get_pos(), mol1.get_pos()
        mol1.set_pos(s1)
        mol2.set_pos(s2)

        # Note: order irrelevant as calculated in next frame, not real time

        # TODO: Log this output
        return f'Moved Ar1 from {s2:.4f} to {s1:.4f}, and Ar2 from {s1:.4f} to {s2:.4f}'

    def split_force(self, *, report=False) -> Decimal:
        """ Delegates equal and opposite force to two atoms. Also detects collisions"""

        unit = Decimal(1)
        t = self._eval_time(unit / 10 ** 2)

        # Update distance, adjust in case of collision
        r = self.eval_distance()
        self.distance = r

        if r <= 0:
            self._mols_collision()

        force = self._lj_force()
        self.mol1.accumulate_force(force)
        self.mol2.accumulate_force(force*-1)

        return r

    def _report(self, force, energy):
        """Debug output""" 

        out = f'\n======\nDistance: {self.distance:.4f}\nEnergy: {energy:.4f}\nForce: {force:.4f}\n'
        out += f'Particle A: {self.mol1}\n'
        out += f'Particle B: {self.mol2}'
        out += '\n======'

        return out

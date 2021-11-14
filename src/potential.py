from src.atom import Atom
from decimal import Decimal
import numpy as np


class Potential:

    def __init__(self, atom1: Atom, atom2: Atom):
        # TODO: log on creation
        self.atom1 = atom1
        self.atom2 = atom2

        self.epsilon: Decimal = Decimal('125.7')  # K
        self.sigma: Decimal = Decimal('0.3345')  # nm

        self.distance = self.eval_distance()

    def __repr__(self):
        return f'Potential({self.atom1}, {self.atom2})'

    # def __hash__(self) -> int:
    #     """Potential's hash is built from concatenating mol IDs"""
    #     x = xxhash.xxh32()
    #     x.update(bytes(f'{self.atom1.ID}{self.atom2.ID}'))
    #     return x.intdigest()

    def __str__(self):
        mol1 = self.atom1
        mol2 = self.atom2
        if mol1.get_pos() > mol2.get_pos():
            mol1, mol2 = mol2, mol1
        return f'Atom{mol1.ID()} {mol1.get_pos():.4f}...[{self.distance:.4f}]' \
               f'...Atom{mol2.ID()} {mol2.get_pos():.4f}'

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
        mol1, mol2 = self.atom1, self.atom2
        distance = abs(Decimal(mol1.get_pos()) - Decimal(mol2.get_pos()))
        if not distance:
            distance = Decimal('10') ** -4
        else:
            distance = distance

        self.distance = distance
        return distance

    # ==== MOTION ====

    def lj_energy(self) -> Decimal:
        """
        Calculate energy from Lennard Jones Potential
        """
        # TODO: Log when calculated
        epsilon = self.epsilon
        sigma = self.sigma
        r: Decimal = self.distance
        x: Decimal = sigma / r

        repulsive = np.power(x, 12)
        attractive = np.power(x, 6)

        return 4 * epsilon * (repulsive - attractive)

    def lj_force(self) -> Decimal:
        """Calculate force by differentiating LJ Potential, units of nN"""
        # TODO: Log when calculated
        r: Decimal = self.distance

        s_r = self.sigma / r
        a = (4 * self.epsilon * self.sigma) / (r * r)

        return a * (6 * np.power(s_r, 5) - 12 * np.power(s_r, 11))


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
        mol1, mol2 = self.atom1, self.atom2

        # Invert Velocities, elastic collisions
        v1, v2 = mol1.velocity, mol2.velocity
        mol1.set_v(v1 * -1)
        mol2.set_v(v2 * -1)

        # Swap positions
        s1, s2 = mol2.get_pos(), mol1.get_pos()
        mol1.set_pos(s1)
        mol2.set_pos(s2)

        # Note: order irrelevant as calculated in next frame, not real time

        # TODO: Log this output
        return f'Moved Ar1 from {s2:.4f} to {s1:.4f}, and Ar2 from {s1:.4f} to {s2:.4f}'

    def split_force(self):
        """ Delegates equal and opposite force to two atoms. Also detects collisions"""

        # Update distance, adjust in case of collision
        r = self.eval_distance()
        self.distance = r

        if r <= 0:
            self._mols_collision()

        force = self.lj_force()
        self.atom1.accumulate_force(force)
        self.atom2.accumulate_force(force * -1)

        return r

    def report(self) -> str:
        """Typical log output for potential. Should be called after running a splitforce"""

        energy = self.lj_energy()
        force = self.lj_force()
        out = f'\n======\nDistance: {self.distance:.4f}nm\nEnergy: {energy:.4f}K\nForce: {force/100:.4f}pN\n'
        out += f'Particle A: {self.atom1.get_pos():.7f}\n'
        out += f'Particle B: {self.atom2.get_pos():.7f}'
        out += '\n======'

        return out

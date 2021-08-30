import utils
from atom import Atom
import numpy as np
from decimal import Decimal


class Interaction:

    def __init__(self, i: Atom, j: Atom) -> None:
        # Unpack both atoms involved in interaction, set distance to be class level (separate func needed as distance)
        # updated every MDS cycle
        self.i: Atom = i
        self.j: Atom = j
        self.r: Decimal = self.distance()  # Angstroms

        print("\nUSING REDUCED UNITS\n")

        # Only Ar-Ar needed to be simulated, hard code epsilon and sigma as constants
        # ATTENT: Currently using reduced units
        self.SIGMA: Decimal = Decimal('1')
        self.EPSILON = Decimal('1')  # TODO: Find the right values

    def lin_diffs(self) -> list:
        s_i = self.i.vitals(v=False)
        s_j = self.j.vitals(v=False)

        lin_diffs = []
        for i in range(2):
            x1, x2 = s_i[i], s_j[i]  # unpack each coord dimension by dimension

            difference = x2 - x1
            lin_diffs.append(difference)

        return lin_diffs

    def distance(self) -> Decimal:
        square_diffs = np.power(self.lin_diffs(), 2)
        r = Decimal(np.sqrt(sum(square_diffs)))

        return r

    def angle(self) -> Decimal:
        delta_x, delta_y = self.lin_diffs()
        return np.arctan(np.divide(delta_y, delta_x))

    def lj_energy(self) -> Decimal:
        # TODO: DECIMAL!

        r = self.r
        x = np.divide(self.SIGMA, r)
        e = self.EPSILON

        repulsive = np.power(x, 12)
        attractive = np.power(x, 6)

        return 4 * e * (repulsive - attractive)

    def lj_force(self) -> Decimal:
        # TODO: Decimal everything

        r: Decimal = self.r
        e: Decimal = self.EPSILON
        s: Decimal = self.SIGMA

        a = Decimal((24 * e * np.power(s, 6)) * np.power(r, -7))
        b = Decimal((2 * np.power(s, 6)) * np.power(r, -6) - 1)

        return a * b

    def delegate_force(self, *, v=False) -> None:

        theta: Decimal = self.angle()
        magnitude: Decimal = self.lj_force()

        i_component = Decimal(np.multiply(magnitude, Decimal(np.cos(theta))))
        j_component = Decimal(np.multiply(magnitude, Decimal(np.sin(theta))))

        force = np.divide([i_component, j_component], 2)
        self.i.evaluate_next_state(force)
        self.j.evaluate_next_state(np.multiply(force, -1))

        if v:
            force_printable = f'{utils.dec_to_str(force[0])}, {utils.dec_to_str(force[1])}'
            print(f'both receives force({force_printable})N\n')

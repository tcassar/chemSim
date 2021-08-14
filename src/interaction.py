from atom import Atom
import numpy as np


class Interaction:

    def __init__(self, i: Atom, j: Atom):

        # Unpack both atoms involved in interaction, set distance to be class level (seperate func needed as distance
        # updated every MDS cycle
        self.i = i
        self.j = j
        self.r = self.distance()

        # Only Ar-Ar needed to be simulated, hard code epsilon and sigma as constants
        self.SIGMA = 3.405
        self.EPSILON = 0.238

    def distance(self):
        s_i = self.i.vitals(v=False)
        s_j = self.j.vitals(v=False)

        square_diffs = []
        for i in range(2):
            x1, x2 = s_i[i], s_j[i]  # unpack each coord dimension by dimension

            difference = x2 - x1
            square_diffs.append(np.power(difference, 2))

        self.r = np.sqrt(sum(square_diffs))

        return self.r

    def lj_energy(self):

        r = self.r
        x = np.divide(self.SIGMA, r)
        e = self.EPSILON

        repulsive = np.power(x, 12)
        attractive = np.power(x, 6)

        return 4 * e * (repulsive - attractive)

    def lj_force(self):
        pass
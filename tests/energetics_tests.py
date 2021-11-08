# Test class to verify that potential looks as it should
from decimal import Decimal
from random import random

import numpy as np
import src.atom
import src.potential
from unittest import TestCase


class EnergeticsTests(TestCase):

    def setUpModule(self):
        """
        Initialise atoms and constants needed for energetics testing. Atoms initialised with random displacements
        as to serve as a control in each tests, so can tests erroneous data
        """
        # Randomly initialised values, reset control each test
        self.a1default = random()
        self.a2default = random() * -1

        # Atoms to be used
        self.atom1 = src.atom.Atom(Decimal(self.a1default), 0, ID=1)
        self.atom2 = src.atom.Atom(Decimal(self.a2default), 0, ID=2)

        # Constants
        self.sigma = Decimal('0.3345')
        self.epsilon = Decimal('125.7')

        # TODO: Logger

    def test_energy(self):
        """
        Test case verifying **energy** at eqm distance
        1) Calculate value of r where force equals 0
        2) Compare to control atoms
        3) Initialise atoms
        """
        self.setUpModule()

        # SP of LJ at 2^(1/6)*sigma
        r_sp: Decimal = np.multiply(Decimal(np.power(2, 1 / 6)), self.sigma)

        # Get control energy (K)
        lj = src.potential.Potential(self.atom1, self.atom2)
        control_energy = lj._lj_energy()

        # Set distance to equal turning point distance, calculate epsilon
        self.atom1.set_pos(Decimal('0'))
        self.atom2.set_pos(r_sp)
        lj.eval_distance()
        calc_epsilon = lj._lj_energy()

        self.assertNotEqual(self.epsilon, control_energy)
        self.assertEqual(self.epsilon, abs(calc_epsilon))

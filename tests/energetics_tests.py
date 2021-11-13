# Test class to verify that potential looks as it should

import numpy as np
import src.atom
import src.potential
from decimal import Decimal
from unittest import TestCase
from random import random


def setUpModule():
    # TODO: Logger for outputs
    pass


class EnergeticsTests(TestCase):

    def setUp(self):

        # Constants
        self.sigma = Decimal('0.3345')
        self.epsilon = Decimal('125.7')

        # Randomly initialised values for a test
        self.a1default = Decimal(random())
        self.a2default = Decimal(random()) * -1

        # Atoms to be used
        self.atom1 = src.atom.Atom(Decimal(self.a1default), 0, ID=1)
        self.atom2 = src.atom.Atom(Decimal(self.a2default), 0, ID=2)

        self.atom1.set_pos(self.a1default)
        self.atom2.set_pos(self.a2default)

        # Initialise Potential
        self.lj = src.potential.Potential(self.atom1, self.atom2)

        self.lj.eval_distance()

    def test_e0(self):
        """
        Test case verifying **energy** at eqm distance
        1) Calculate value of r where force equals 0
        2) Compare to control atoms
        3) Initialise atoms
        """

        # SP of LJ at 2^(1/6)*sigma
        r_sp: Decimal = np.multiply(Decimal(np.power(2, 1 / 6)), self.sigma)

        # Get control energy (K)
        control_energy = self.lj.lj_energy()

        # Set distance to equal turning point distance, calculate epsilon
        self.atom1.set_pos(Decimal('0'))
        self.atom2.set_pos(r_sp)
        self.lj.eval_distance()
        calc_epsilon = self.lj.lj_energy()

        self.assertNotEqual(self.epsilon, control_energy)
        self.assertEqual(self.epsilon, abs(calc_epsilon))

    def test_e_sigma(self):
        """Verify that distance of sigma has net energy of 0, and that control distance does not"""
        # Get control energy (K)
        control_energy = self.lj.lj_energy()

        # Set atoms a distance of \sigma apart
        self.atom1.set_pos(Decimal('0'))
        self.atom2.set_pos(self.sigma)
        self.lj.eval_distance()

        # Find energy at distance of sigma
        e_sig = self.lj.lj_energy()
        
        self.assertNotEqual(control_energy, Decimal('0'))
        self.assertEqual(e_sig, Decimal('0'))

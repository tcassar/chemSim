import random

from atom import Atom
from utils import *
from decimal import Decimal
from unittest import TestCase
from random import randrange
from typing import List, Iterable
import numpy as np
import numpy.typing as npt


# noinspection PyMethodMayBeStatic
class AtomTestCase(TestCase):
    def setUp(self) -> None:
        random.seed(100)

    def test_position_update_0_velocity(self):
        """Tests that a force leads to the right movement with 0 velocity"""

        # Initialise Atom object (p) at (0,0) with |V| of 0, with reduced units
        p: Atom = Atom()

        # [Force, Resulting Displacement]: All done over t=1 ATTENT: Reduced units again

        valid_values = [
            [0, 0],
            [3, 5],
            [-2, 0],
            [-5, -2],
        ]

        valid_values = [list(map(Decimal, x)) for x in valid_values]

        for value in valid_values:
            p.set_attrs(s=[0, 0], v=[0, 0])
            print(f'Testing with Force of {list(map(dec_to_str, value))}')
            correct_disp = np.divide(value, 2)
            # print(correct_disp)
            p.evaluate_next_state(value)
            self.assertListEqual(list(correct_disp), p.vitals(v=False))

    def test_staged_motion(self):
        """Checks final displacement and velocity from set discreet forces"""

        # Initialise Atom object (p) at (0,0) with |V| of 0, with reduced units
        p: Atom = Atom()

        forces = [
            [4, 6],
            [-4, -6],
            [8, 4],
            [-3, 7]
        ]

        result = [[Decimal('6.5'), Decimal('7.5')],  # displacement
                  [Decimal('5'), Decimal('11')]]  # velocity

        for force in forces:
            p.evaluate_next_state((intlist_to_dec(force)))

        atom_results = p.vitals()
        for i, _ in enumerate(result):
            with self.subTest(i + 1):
                self.assertListEqual(list(atom_results[i]), result[i])

    def test_reversible(self, subtest=None):
        """
        Test which creates a list of forces from an RNG, then applies same force *= -1 to atom. Atom should end at (0,0)
        with 0 velocity
        """

        def random_force():
            return [Decimal(randrange(-10, 11)), Decimal(randrange(-10, 11))]

        p = Atom()
        n = 25

        forces = [random_force() for i in range(n)]
        neg_forces = np.multiply(forces, -1)

        for force in forces:
            p.evaluate_next_state(force)

        for neg_force in neg_forces:
            p.evaluate_next_state(neg_force)

        calculated = p.vitals()
        for i, result in enumerate(calculated):
            with self.subTest(i):
                self.assertListEqual(list(result), [Decimal('0'), Decimal('0')])


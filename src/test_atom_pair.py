from atom import Atom
from utils import *
from decimal import Decimal
from unittest import TestCase
from random import randrange
import numpy as np


# noinspection PyMethodMayBeStatic
class AtomTestCase(TestCase):

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
            # print(f'Testing with Force of {list(map(dec_to_str, value))}')
            correct_disp = np.divide(value, 2)
            # print(correct_disp)
            p.evaluate_next_state(value)
            self.assertListEqual(list(correct_disp), list(p.vitals()[0]))

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

        result = [[Decimal('14.5'), Decimal('15.5')],  # displacement
                  [Decimal('5'), Decimal('11')]]  # velocity

        for force in forces:
            p.evaluate_next_state((intlist_to_dec(force)))

        atom_results = p.vitals()
        for i, _ in enumerate(result):
            with self.subTest(i):
                self.assertListEqual(list(atom_results[i]), result[i])

    def test_reversible(self):
        """
        Test which creates a list of forces from an RNG, then applies same force *= -1 to atom. Atom should end at (0,0)
        with 0 velocity
        """

        def random_force():
            return [Decimal(randrange(-10, 11)), Decimal(randrange(-10, 11))]

        p = Atom()
        n = 100

        forces = [random_force() for _ in range(n)]
        neg_forces = np.multiply(forces, -1)

        for force in forces:
            p.evaluate_next_state(force)

        for neg_force in neg_forces:
            p.evaluate_next_state(neg_force)

        calculated = p.vitals()[1]
        self.assertListEqual(list(calculated), [Decimal('0'), Decimal('0')])

    def test_constant_acc(self):
        """Test calculated position and velocity from integration of constant acceleration"""

        # Write how this fixed changing origin problem:
        # I had thought that once new position was found old one would be overwritten. However, had not thought about
        # fact that origin resets with circular approach

        a = [Decimal(4), Decimal(0)]
        v: Callable = lambda t: [4 * t, 0]
        s: Callable = lambda t: [2 * (t ** 2), 0]
        time = 10

        p = Atom()

        for i in range(time):
            expected = [s(i), v(i)]
            atom_results = p.vitals()
            with self.subTest(f'3.{i}'):
                self.assertListEqual(atom_results, expected)
            p.evaluate_next_state(a)


class UtilsTestCase(TestCase):

    def test_atan(self):
        pi = np.pi
        rt3 = np.sqrt(Decimal(3))
        exact_vals = [0, rt3 / 3, 1, rt3]
        results = [0, pi / 6, pi / 4, pi / 3]

        for val, result in zip(exact_vals, results):
            with self.subTest(exact_vals.index(val)):
                self.assertEqual(inaccurate_atan(val), result)

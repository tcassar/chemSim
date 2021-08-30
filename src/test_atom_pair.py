from atom import Atom
from utils import dec_to_str
from decimal import Decimal
from unittest import TestCase
from typing import List
import numpy as np


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
            print(f'Testing with Force of {list(map(dec_to_str, value))}')
            correct_disp = np.divide(value, 2)
            # print(correct_disp)
            p.evaluate_next_state(value)
            self.assertListEqual(list(correct_disp), p.vitals(v=False))

        print('\n')

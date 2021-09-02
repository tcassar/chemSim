from atom import Atom
from utils import *
from decimal import Decimal
from unittest import TestCase
from typing import List, Iterable
import numpy as np


class AtomTestCase(TestCase):

    def test_position_update_0_velocity(self) -> None:
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

    def test_motion_via_cycle(self) -> None:
        y_axis: List[Decimal] = []
        x_axis: Iterable

        f = open('motiontest.txt', 'w')
        f.write('NEW TEST\n')
        """Verifies that stepwise approach to changing s and v equates with SUVAT approach where t!=1"""

        p: Atom = Atom()
        q: Atom = Atom()
        u: List[Decimal]
        s0: List[Decimal]
        u, s0 = p.vitals()
        t: int = 100

        # set up test equations which have been calculated & verified by hand;
        # encoded in coefficient form. a = (4t + 6)i - (t^2 - 3t)j is encoded as shown in a_eq
        a_eq: List[List[Decimal]] = [[Decimal(6), Decimal(4)],
                                     [Decimal(0), Decimal(3), Decimal(-1)]]

        v_eq: List[List[Decimal]] = [[u[0], Decimal(6), Decimal(2)],
                                     [u[1], Decimal(0), precise_frac(-3, 2), precise_frac(-1, 3)]]

        s_eq: List[List[Decimal]] = [[s0[0], u[0], Decimal(3), precise_frac(2, 3)],
                                     [s0[1], u[1], Decimal(0), precise_frac(-1, 2), precise_frac(-1, 12)]]

        for i in range(t):
            i += 1
            # find expected outcomes from equations above, from t = 1 to t=t
            force: List[Decimal] = [coef_to_dec(eq, i) for eq in a_eq]  # at = Ft as F=ma, M = 1
            test_v: List = [coef_to_dec(eq, i) for eq in v_eq]  # manual integration
            test_s: List = [coef_to_dec(eq, i) for eq in s_eq]  # manual integration
            p.evaluate_next_state(force)
            s1, v = p.vitals()
            s1, v = list(s1), list(v)
            f.write(f'Force Applied: {declist_to_str(force)}\n')
            f.write(f'Atom @ {declist_to_str(list(s1))}, should be {declist_to_str(list(test_s))}\n\n')

            with self.subTest(i):
                self.assertListEqual(s1, test_s)

        f.close()
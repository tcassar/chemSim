import src.atom
from decimal import Decimal
from unittest import TestCase


def suvat(*, u: Decimal, a: Decimal, t: Decimal) -> tuple[Decimal, Decimal]:
    """s = ut + 1/2 at^2 and v  u+at"""
    s: Decimal = u * t + (a * t**2) / Decimal(2)
    v: Decimal = u + a * t

    return s, v


class MotionTests(TestCase):
    """Tests that the atom moves as it should. All done by setting mass to 1, so that F=a"""

    def setUp(self) -> None:
        self.atom = src.atom.Atom(Decimal('0'), Decimal('0'))
        self.atom.mass = 1
        # self.atom.set_pos(Decimal('0'))
        self.atom.set_v(Decimal('0'))

    def test_constant_acceleration(self):
        """check that applying constant force leads to expected resulting displacement
        1) Apply force (= acceleration)
        2) SUVAT Equation -> vel and SUVAT Equation -> disp.
        3) Assert atom vitals = suvats
        """

        a = Decimal('4')
        u = Decimal(0)
        t = Decimal('1')

        suvat_s, suvat_v = suvat(u=u, a=a, t=t)

        res = 1000
        time = t/res
        force = a

        for i in range(res):
            self.atom.accumulate_force(force)
            self.atom.move(time)

        sim_s, sim_v = self.atom.get_pos(), self.atom.velocity

        with self.subTest("Testing Displacement"):
            self.assertEqual(sim_s, suvat_s)

        with self.subTest("Testing Velocity"):
            self.assertEqual(sim_v, suvat_v)

    def test_variable(self):
        """Check that we have correct behaviour for variable force"""
        pass

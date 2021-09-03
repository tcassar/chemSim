from utils import *
from decimal import Decimal
import numpy as np
from typing import Callable, ClassVar


class Atom:

    def __init__(self, s=None, v=None, ru=True):
        if s is None:
            s = [0, 0]
        if v is None:
            v = [0, 0]

        self.velocity = v
        self.position = s
        self.force = np.array([0, 0])

        # Default to reduced units

        if not ru:
            self.MASS: Decimal = Decimal('36')  # Daltons
        else:
            self.MASS: Decimal = Decimal('1')

    def __repr__(self):
        decs = [*self.position, *self.velocity]
        floats = list(map(dec_to_str, decs))
        floats = list(map(float, floats))
        return f'Atom(s={floats[:2]}, v={floats[2:]})'

    def set_attrs(self, *, s: List[int], v: List[int]) -> None:
        """For testing, directly sets displacement and velocity"""

        s, v = intlist_to_dec(s), intlist_to_dec(v)

        self.velocity = v
        self.position = s

    def vitals(self, *, s=True, v=True, read=False) -> List[List[Decimal]]:
        """returns s and/or v in list form (only returns what is asked)"""
        out = [self.position, self.velocity]
        if not v:
            out = self.position
        if not s:
            out = self.velocity

        return out if s or v else []

    def evaluate_next_state(self, force: List[Decimal]) -> None:
        """Evaluates next state based off previous state using SUVAT"""
        a = np.divide(force, self.MASS)

        sn: List[Decimal]
        vn: List[Decimal]
        sn, vn = self.vitals()
        t = Decimal(1)

        # v = u + at, t = 1
        self.velocity = np.add(vn, np.multiply(a, t))

        # s = ut + 1/2 a * t**2, t = 1
        self.position = np.add(np.multiply(vn, t), np.divide(np.multiply(a, t ** 2), 2))

    def limit(self, force_eq: List, subpoints: int, point: int):

        for subpoint in range(subpoints):
            subpoint = Decimal(subpoint)
            t = np.add(point,
                       np.divide(subpoint, subpoints))
            print(f't: {t!r}')
            force = coef_to_dec(force_eq, t)
            self.evaluate_next_state([force, 0])

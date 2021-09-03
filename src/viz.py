from atom import Atom
from utils import *
from decimal import Decimal
from typing import List, Tuple
import matplotlib.pyplot as plt


def line_from_integration(eq: List[Decimal], points: int) -> Tuple[range, List[Decimal]]:
    x = range(points)
    y = []
    for i in x:
        i = Decimal(i)
        y.append(coef_to_dec(eq, i))

    return x, y


def line_from_atom(eq: List, points: int, atom: Atom) -> Tuple[range, List[Decimal]]:
    x = range(points)
    y = []
    for i in x:
        # atom.evaluate_next_state([force_at_t, 0])
        atom.limit(eq, 100, i)
        _, v = atom.vitals()
        y.append(v[0])

    return x, y


i_acceleration = [Decimal(6), Decimal(4), Decimal(3)]
i_velocity = [0, Decimal(6), Decimal(2), Decimal(1)]

ar1 = Atom()
n = 10

integral_points = line_from_integration(i_velocity, n) 
atom_points = line_from_atom(i_velocity, n, ar1)

plt.plot(*integral_points, 'r', label='Integral')
plt.plot(*line_from_atom(i_velocity, n, ar1), label='Atom')
plt.xlabel('t')
plt.ylabel('velocity')
plt.show()

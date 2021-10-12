# Defines Atom class
# Initialised with displacement and velocity
# Moves given a force vector: TODO: vector class


from decimal import Decimal
import numpy as np


class Atom:

    def __init__(self, s, v):
        self.displacement: Decimal = s
        self.velocity: Decimal = v

        # Set boundary at 50 - later implemented as two bounds at +- 50
        # Wall assumed to have infinite mass
        self.wall = 50

        for i in [s, v]:
            if type(i) != Decimal:
                print(f'WARNING: Approximating {i} to Decimal')

    def __repr__(self):
        return f'Atom(s={self.displacement}, v={self.velocity})'

    def vitals(self):
        return self.displacement, self.velocity

    def move(self, force: Decimal):
        """Moves atom using current state, and force"""

        # Define suvat equations
        def new_s(a: Decimal, u: Decimal, t: Decimal) -> Decimal:
            """s = ut + (1 / 2) *  a * t**2"""
            A = u * t
            B = (Decimal('0.5')) * a * t ** 2

            return np.add(A, B)

        def new_v(a: Decimal, u: Decimal, t: Decimal):
            return np.add(u, np.multiply(a, t))

        # Retrieve current state
        u = self.velocity
        s0 = self.displacement

        # Calculate acceleration from F=ma
        # RU => mass = 1 => F=a
        a = force / 1

        # Evaluate new state
        time = Decimal('0.01')
        self.velocity = new_v(a, u, time)
        self.displacement = new_s(a, u, time) + s0

        # Make particles bounce off walls - collisions elastic hence just invert velocity
        if self.displacement > self.wall:
            self.displacement = self.wall
            self.velocity *= -1
        elif self.displacement < -self.wall:
            self.displacement = -self.wall
            self.velocity *= -1

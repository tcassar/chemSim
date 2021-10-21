# Defines Atom class
# Initialised with displacement and velocity
# Moves given a force vector: Scale: vector class

from environment import Container, Wall
from decimal import Decimal
import numpy as np


class Atom:
    displacement: Decimal
    velocity: Decimal
    walls: list[Wall]

    def __init__(self, s, v):
        # Scale displacement and velocity classes
        self.displacement: Decimal = s
        self.velocity: Decimal = v

        self.contained = False

        for i in [s, v]:
            if type(i) != Decimal:
                print(f'WARNING: Approximating {i} to Decimal')

    def __repr__(self):
        return f'Atom(s={self.displacement}, v={self.velocity})'

    def __str__(self):
        return f'Atom(s={self.displacement:.4f}, v={self.velocity:.4f})'

    def __bytes__(self):
        """Creates a bytes representation of an object"""
        st = repr(self)
        return bytes(st, 'utf-8')

    # Helper functions
    def set_pos(self, s: Decimal) -> None:
        """Set displacement from outside class"""
        self.displacement = s

    def get_pos(self) -> Decimal:
        """Get displacement from outside class"""
        return self.displacement

    def set_v(self, v: Decimal) -> None:
        """Set velocity from outside class"""
        self.velocity = v

    def get_v(self) -> Decimal:
        """Get velocity from outside class"""
        return self.velocity

    def inject_to(self, container: Container):
        """Associates atom with container"""
        self.container = container
        self.contained = True

    # Kinematics
    def move(self, force: Decimal, time: Decimal):
        """Moves atom using current state, and force
        Args:
            force: Decimal, force atom is experiencing
            time: Decimal, time period till next frame
        """

        # Define suvat equations
        # noinspection PyPep8Naming
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

        # Evaluate new state, don't update displacement until after checking for wall collision
        self.velocity = new_v(a, u, time)
        self.displacement = new_s(a, u, time) + s0

        # Detect and handle collisions with walls
        if self.contained:
            if collided := self.container.out_of_bounds(self.displacement):
                self.velocity = Decimal(0)
                self.displacement = collided
                print("Collided")




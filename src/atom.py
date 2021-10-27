# Defines Atom class
# Initialised with displacement and velocity
# Moves given a force vector: Scale: vector class
import xxhash

from environment import Container, Wall
from decimal import Decimal
import numpy as np

from src.environment import Container


class Atom:
    container: Container
    displacement: Decimal
    velocity: Decimal
    walls: list[Wall]

    # noinspection PyPep8Naming
    def __init__(self, s, v, *, ID=0):
        # Scale displacement and velocity classes

        self.container: Container
        self.ID = ID

        self.displacement: Decimal = s
        self.velocity: Decimal = v

        self.contained = False
        self.experiencing_force: Decimal = Decimal(0)

        for i in [s, v]:
            if type(i) != Decimal:
                print(f'WARNING: Approximating {i} to Decimal')

    def __repr__(self):
        return f'Atom(s={self.displacement}, v={self.velocity})'

    def __str__(self):
        return f'Atom{self.ID}'

    def __bytes__(self):
        """Creates a bytes representation of atom. Gives hash of ID for labelled atoms, ow hash of pos and vel
        Assigned atoms are preferred"""
        if self.ID:
            byte_repr = bytes(self.ID)
        else:
            byte_repr = bytes(f'{self!r}')

        return byte_repr

    def __hash__(self):
        """Outputs hash based off our ID / pos and vel"""
        x = xxhash.xxh32()
        x.update(bytes(self))

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

    def get_ID(self) -> str:
        return f'{self.ID}'

    def inject_to(self, container: Container):
        """Associates atom with container"""
        self.container = container
        self.contained = True

    # Kinematics

    def accumulate_force(self, force: Decimal):
        """"""
        self.experiencing_force += force

    def move(self, time: Decimal):
        """Moves atom using current state, and force
        Args:
            time: Decimal, time period till next frame
        """

        # Pull force that atom is experiencing
        force: Decimal = self.experiencing_force
        self.experiencing_force = 0

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
                self.velocity *= Decimal('-0.0001')  # FIXME: coef is absolute bollocks
                self.displacement = collided
                print(f'{self} collided with wall')

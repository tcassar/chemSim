# Defines Atom class
# Initialised with displacement and velocity
# Moves given a force vector: Scale: vector class

from decimal import Decimal
import logging
import numpy as np


class Atom:
    displacement: Decimal
    velocity: Decimal
    walls: list

    # noinspection PyPep8Naming
    def __init__(self, s, v, *, ID=0):
        # Scale displacement and velocity classes

        assert ID < 1000 and type(ID) == int
        self.ID = str(ID).zfill(3)

        self.displacement: Decimal = s
        self.velocity: Decimal = v

        self.contained = False
        self.experiencing_force: Decimal = Decimal(0)

        self.mass = Decimal('39.948')  # u (i.e. 1.6605 * 10**-27)

        for i in [s, v]:
            if type(i) != Decimal:
                logging.warning(f'Approximating {i} to Decimal')

    def __repr__(self):
        return f'Atom(s={self.displacement}, v={self.velocity})'

    def __str__(self):
        return f'Atom{self.ID}'
    #
    # def __bytes__(self):
    #     """Creates a bytes representation of atom. Gives hash of ID for labelled atoms, ow hash of pos and vel
    #     Assigned atoms are preferred"""
    #     if self.ID:
    #         byte_repr = bytes(self.ID)
    #     else:
    #         byte_repr = bytes(f'{self!r}')
    #
    #     return byte_repr
    #
    # def __hash__(self):
    #     """Outputs hash based off our ID / pos and vel"""
    #     x = xxhash.xxh32()
    #     x.update(bytes(self))

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

    def inject_to(self, container):
        """Associates atom with container"""
        self.container = container
        self.contained = True
        container.contained_atoms.append(self)

    # Kinematics

    def accumulate_force(self, force: Decimal):
        """"""
        self.experiencing_force += force

    def move(self, time: Decimal) -> Decimal:
        """Moves atom using current state, and acceleration
        Args:
            time: Decimal, time period till next frame
        return: New displacement
        """

        # Pull acceleration that atom is experiencing
        a: Decimal = self.experiencing_force / self.mass  #
        self.experiencing_force = 0

        # Define suvat equations
        # noinspection PyPep8Naming
        def new_s(a: Decimal, u: Decimal, t: Decimal) -> Decimal:
            """s = ut + (1 / 2) *  a * t**2"""
            A: Decimal = u * t
            B: Decimal = (Decimal('0.5')) * a * t ** 2

            return np.add(A, B)

        def new_v(a: Decimal, u: Decimal, t: Decimal):
            return np.add(u, np.multiply(Decimal(a), Decimal(t)))

        # Retrieve current state
        u = self.velocity
        s0 = self.displacement

        # Evaluate new state, don't update displacement until after checking for wall collision
        self.velocity = new_v(a, u, time)
        self.displacement = new_s(a, u, time) + s0

        # Detect and handle collisions with walls
        if self.contained:
            if collided := self.container.out_of_bounds(self.displacement):
                self.velocity *= Decimal('-0.1')  # FIXME: coef is absolute bollocks
                self.displacement = collided
                logging.info(f'{self} collided with wall')

        return self.displacement

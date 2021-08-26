import utils
from decimal import Decimal
import numpy as np


class Atom:

    def __init__(self, s=None, v=None):
        if s is None:
            s = [0, 0]
        if v is None:
            v = [0, 0]

        self.MASS: Decimal = Decimal('36')  # Daltons
        self.velocity = v
        self.position = s
        self.force = np.array([0, 0])

    def __repr__(self):
        decs = [*self.position, *self.velocity]
        floats = list(map(utils.dec_to_str, decs))
        floats = list(map(float, floats))
        return f'Atom(s={floats[:2]}, v={floats[2:]})'

    def vitals(self, *, s=True, v=True) -> list:
        """returns s and/or v in list form (only returns what is asked)"""
        out = [self.position, self.velocity]
        if not v:
            out = self.position
        if not s:
            out = self.velocity

        return out if s or v else []

    def evaluate_next_state(self, vector: list, v=False) -> str:
        """
        Updates velocity and position of particle for cycle n+1, based only off cycle n.
        Receives force vector (split into *i* and *j* components), returns a string (with updated info
        if set to verbose mode)
        """
        # TODO: needs better name

        DALTON_TO_KG = np.power(Decimal('1.66054'), -27)
        MASS = np.multiply(self.MASS, DALTON_TO_KG)

        # Generate DELTA FOR 1 CYCLE i.e. needs to be added to previous

        # remember current state
        u = self.velocity
        st = self.position

        acceleration = np.divide(vector, MASS)  # all units SI
        velocity = acceleration + u  # as integral of acceleration between limits of t and t+1 = a :. same val
        st_1 = st + velocity  # same integration note as above

        # Update atom state
        self.velocity += velocity
        self.position += st_1

        return '' if not v else f'Velocity: {velocity}\nPos:{st_1}'

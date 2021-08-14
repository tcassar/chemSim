class Atom:

    def __init__(self, v=0, x=0, y=0):
        self.MASS = 36  # Daltons
        self.velocity = v
        self.position = [x, y]

    def update_s(self, x: int, y: int):
        self.position[0] += x
        self.position[1] += y

    def update_v(self, new_velocity):
        self.velocity += new_velocity

    def vitals(self, *, s=True, v=True):
        out = [self.position, self.velocity]
        if not v:
            out = self.position
        if not s:
            out = self.velocity

        return out if s or v else []

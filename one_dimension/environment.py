# Sets up objects that affect physical env of sim, such as container boundaries, temperature control, etc.
from atom import Atom
from decimal import Decimal
from typing import List


class Wall:
    # Walls modelled with infinite mass, and collisions assumed to be elastic

    def __init__(self, pos: Decimal):
        self.position = pos

    def __repr__(self):
        return f'Wall({self.position})'

    # ==== COMPARISONS ===

    def __eq__(self, other: Decimal) -> bool:
        return self.position == other

    def __le__(self, other: Decimal) -> bool:
        """See if point has a more -ve position than wall"""
        return self.position <= other

    def __ge__(self, other: Decimal) -> bool:
        """See if point has more +ve position than wall"""
        return self.position >= other


class Container:
    # Scale
    # Constructs container via walls, for now 1d thus max 2 walls

    def __init__(self, walls: List[Decimal]):
        made_walls = []
        walls.sort()
        for wall in walls:
            # Scale: Needs to work with multiple dimensions, by accepting [[x, x], [y, y], [z, z]]
            made_walls.append(Wall(wall))

        self.walls = made_walls
        # Walls are sorted in [left, right] per dimension

    def __repr__(self):
        return f'Container(walls={self.walls}'

    def out_of_bounds(self, atom_pos: Decimal) -> int:
        """If molecule is out of bounds, return a correction.
        If missed lower bound, returns 1. If upper, returns -1. If neither, returns 0"""
        pass


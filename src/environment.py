# Sets up objects that affect physical env of sim, such as container boundaries, temperature control, etc.

from decimal import Decimal
from typing import List
from dataclasses import dataclass


@dataclass
class Wall:
    pos: Decimal


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

    def out_of_bounds(self, atom_pos: Decimal, res=Decimal('0.0001')) -> Decimal:
        """If molecule is out of bounds, return a correction.
        If missed lower bound, returns 1. If upper, returns -1. If neither, returns new position for atom"""
        lower, *_, upper = self.walls  # *_ is redundant as will always be len(2), just makes clear

        if atom_pos < lower.pos:
            adjustment = lower.pos + res
            # print("Lower wall hit")
        elif atom_pos > upper.pos:
            adjustment = upper.pos - res
            # print("Upper wall hit")
        else:
            return Decimal(0)

        return adjustment

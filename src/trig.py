from decimal import Decimal
from typing import Callable
import numpy as np


def _constructor(x, func):
    x = float(f'{x}')
    return Decimal(func(x))


class ImpTrig:

    def __init__(self):
        pass

    @staticmethod
    def atan(x: Decimal) -> Decimal:
        """Dev only, too inaccurate and imprecise for final build"""
        return _constructor(x, np.arctan)

    @staticmethod
    def cos(x: Decimal) -> Decimal:
        return _constructor(x, np.cos)

from decimal import Decimal
from typing import List, Callable
import numpy as np



def dec_to_str(n: Decimal) -> str:
    """Turns a decimal.Decimal type into a float to 4dp for readable printing"""
    return f'{float(n):.4f}'


def declist_to_str(n: List[Decimal], conv: Callable = dec_to_str) -> str:
    """Converts list consisting of Decimal into List[Str] of printable values"""
    return f'{list(map(conv, n))}'


def intlist_to_dec(n: List[int]) -> List[Decimal]:
    """Converts list of ints to list of Decimals"""
    return [Decimal(str(x)) for x in n]


def precise_frac(n: int, d: int) -> Decimal:
    """precisely calculates fractions from ints"""
    return np.divide(Decimal(n), Decimal(d))


def coef_to_dec(coefficients: List[Decimal], x: Decimal) -> Decimal:
    """Converts a polynomial in coefficient form to a Decimal"""
    y: Decimal = Decimal('0')
    for i, coefficient in enumerate(coefficients):
        y += coefficient * (x**i)

    return y

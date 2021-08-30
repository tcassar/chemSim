from decimal import Decimal
from typing import List


def dec_to_str(n: Decimal) -> str:
    """Turns a decimal.Decimal type into a float to 4dp for readable printing"""
    return f'{float(n):.4f}'


def int_to_dec(n: list) -> List[Decimal]:
    """Converts list of ints to list of Decimals"""
    return [Decimal(x) for x in n]

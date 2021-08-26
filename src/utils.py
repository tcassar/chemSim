from decimal import Decimal


def dec_to_str(n: Decimal) -> str:
    """Turns a decimal.Decimal type into a float to 4dp for readable printing"""
    return f'{float(n):.4f}'
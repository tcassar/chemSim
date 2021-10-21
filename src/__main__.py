import decimal

from atom import Atom
from environment import Container
from potential import Potential
from decimal import Decimal


def main():
    ar1, ar2 = Atom(Decimal('0.75'), 30), Atom(Decimal('-0.75'), -30)
    intr = Potential(ar1, ar2)

    walls = [Decimal(-1.1), Decimal(1.1)]
    ctr = Container(walls)
    ar1.inject_to(ctr)
    ar2.inject_to(ctr)

    log_frames = 9

    for i in range(10 ** log_frames):
        if not i % 10 ** (log_frames - 2):
            print(intr.split_force())


if __name__ == '__main__':
    main()

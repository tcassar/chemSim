from atom import Atom
from potential import Potential
from decimal import Decimal

def main():
    ar1, ar2 = Atom(Decimal('0.5'), -3), Atom(Decimal('-0.5'), 3)
    intr = Potential(ar1, ar2)

    log_frames = 9

    for i in range(10 ** log_frames):
        if not i % 10 ** (log_frames - 2):
            print(intr.split_force())


if __name__ == '__main__':
    main()

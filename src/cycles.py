from src.environment import Container
from src.potential import Potential
from decimal import Decimal
import logging
import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.atom import Atom


def write_to_csv(*, ljp: Potential, res: Decimal, file=False) -> str:
    """Will write to file in format
    distance, energy, force, time\n
    """
    # Gather Values

    sf = lambda i: f'{i:.12f}'

    distance = sf(ljp.eval_distance())
    energy = sf(ljp.lj_energy())
    force = sf(ljp.lj_force())

    out = f'{distance}, {energy}, {force}, {res}'
    if file:
        with open(file, 'a+') as f:
            f.write(out)
    else:
        print(out)
    return 'Wrote values to disk'


def pairwise_cycle(container: Container, time: Decimal(), datapoints: int) -> None:
    """
    Pairwise cycle runs as follows:
    SETUP:
        Assert len of atom list is 2
        Initialise static potential between atoms
    CYCLE:
        Potential.split_force()
        atoms.move() for atom in atoms
        log to file

    Important to track average distance between atoms every 1000 cycles
    """

    def conditions() -> str:
        out = f'Time frame: {time}\n'
        out += f'Base Resolution: {res}\n'
        out += f'Dynamic Resolution: {dyn_res}\n'
        return out

    def log_when_exit() -> str:
        avg_r = cumul_r / frames
        percent_error = 100 * ((avg_r - expected_r) / expected_r)
        sign = lambda i: ('+' if i > 0 else '-')

        logging.info(f'{}s of motion simulated over {frames} frames')
        logging.info(f'Average Distance: {avg_r}; Expected {expected_r}')
        logging.info(f'% Error: {sign(percent_error)}{percent_error:.3f}%')

        return 'Cycle has ended'

    # Check length, set counters, initialise objects
    atoms: list[Atom] = container.contained_atoms
    print(atoms)
    assert len(atoms) == 2

    potential = Potential(*atoms)
    dyn_res = False
    res: Decimal = 1 / (Decimal('10') ** 7)
    cumul_r = Decimal('0')
    frames = 0

    # calculate expected values for distance
    expected_r = (np.power(Decimal(2), Decimal(1) / 6) * potential.sigma)

    # Make sure time is a Decimal, crash if not
    if type(time) != Decimal:
        try:
            time = Decimal(time)
            logging.warning(f"Approximating time {time} to Decimal")
        except TypeError:
            logging.critical("Time is not a Decimal and cannot be approximated to one; exiting")
            quit()

    # Log initial conditions
    logging.info(f'Initial Conditions: {conditions()}')
    logging.info(f'Objects: {atoms[0]!r}\n{atoms[1]!r}\n{potential!r}')

    # Loop for total time, with desired number of outputs
    time_per_point: Decimal = time / datapoints

    try:
        for point in range(datapoints):
            t = Decimal('0')
            logging.info(write_to_csv(ljp=potential, res=(point * time_per_point) + t))
            while t < time_per_point:
                r: Decimal = potential.split_force()
                frames += 1
                cumul_r += r
                for atom in atoms:
                    if dyn_res and r < expected_r:
                        # TODO: fine tune dyn res function
                        pass
                    atom.move(res)
                t += res
    except KeyboardInterrupt:
        logging.warning("Keyboard Interrupt")
        logging.info(log_when_exit())
        quit()

    logging.info(log_when_exit())


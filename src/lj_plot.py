import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import k


def ev_per_k_to_ev(n):
    return k * n


def lj_potential(r: np.linspace, epsilon: float, sigma: float) -> float:
    """
    Calculates Lennard Jones potential in Joules

    Args:
        sigma: van de Waals radius; how close the two particles can get (Å)

        epsilon: Negative of depth of potential well; i.e. Strength of attraction at equilibrium bond length (eV)

        r: Distance between centre of both particles (Å)

    :return: Lennard-Jones potential (eV/Å)
    """
    s_over_r = sigma / r
    attractive_plus_repulsive = np.power(s_over_r, 12) - np.power(s_over_r, 6)
    return 4 * epsilon * attractive_plus_repulsive


rng = np.linspace(3, 5, 100)
plt.plot(rng, lj_potential(rng, ev_per_k_to_ev(142.095), 3.3605), label='Lennard Jones')
plt.xlabel("Distance (Å)")
plt.ylabel("Energy (eV)")
plt.show()

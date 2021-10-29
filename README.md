---
author: tcassar
---
---
# Simulating the motion of Argon atoms based off their initial velocity, and their inter-atomic forces. 

## Outline

#### Description
+ This project calculates the energy between argon atoms, $E_{PE}$, using a Lennard-Jones pairwise potential. Interatomic force (IAF) is then calculated using the derivative of the Lennard-Jones potential with respect to distance ($F=-\frac{dE_{pe}}{dr})$.
+ Using the calculated forces, a new position and velocity of each atom is calculated across a period of time. This cycle is then repeated, resulting in atomic motion.

#### Applications of Molecular Dynamics Simulations
+ In the real world, MDSs are used throughout science. In Biochemistry, they are used to simulate protein folding. In Physics, they are used to approximate solutions to n-body problems, such as the _Millenium Simulation_. They are used in material sciences to test how stress affects systems, and to predict things like temperature and pressure in virtual systems.


#### Features
+ This simulation works verifiably for two argon atoms in one dimension, logging metrics such as positions, distance, $E_{PE}$, IAF and collisions with walls of container. This simulation also can approximate the interatomic energies and forces of many $\ce{Ar}$ atoms. Many-body behaviour for this simulation is unverifiable (see below), and in all likelihood not accurate enough for commerical use. It should, however, be accurate enough to still be interesting, and to show expected behaviour. 

#### Non-Features
+ This project, like the professional LAMMPS, does not include visualisation. While a basic Python wrapper can be put round the library, the focus of this project was about the data rather than the graphical output.
+  Temperature is constant throughout, and, as configured, only $\ce{Ar}$ atoms can be used. While this is theoretically easily changeable, it was added complexity that, for me, was not necessary in understanding and simulating interatomic energies, and the motion that arises from IAFs.

---
## Models

### LJ Potential
+ In order to calculate $E_{PE}$ and IAF, I elected to implement the Lennard-Jones Potential (_LJP_). The potential was introduced in 1924 by Sir John Edward Lennard-Jones to describe the interaction of liquid argon.
+ The potential is comprised of the sum of 2 distinct interactions - attrative interactions, and repulsive interactions. 
	+ 3 possible sources for attractive interaction: permanent dipole-dipole, permanent dipole-induced dipole, induced dipole-dipole interactions. 
	+ $\therefore E_{pe{(total~attractive)}} = -\frac{1}{(4\pi\epsilon)^2}\cdot(\frac{0.66\mu^4}{k_BT} + \mu^2\alpha + 0.75\alpha^2I)\cdot(\frac{1}{r^6})~J$ where $\epsilon$ is permittivity of  medium, $\mu$ is a dipole moment, $\alpha$ is polarisibility of electron cloud, $I$ is first ionisation energy, and $r$ is interatomic distance.
	+ At constant temperatures for one species, this simplifies to $-\frac{A}{r^6}~J$
	+ Repulsive interactions (at constant temperature) given by $\frac{1}{r^{12}}~J$
	+ $E_{PE(total)} = \frac{1}{r^{12}} -\frac{A}{r^6} J$

+ Since the _LJP_ was introduced for liquid Argon, I decided Argon would be the most sensible element to start off with. Gaseous Argon also adheres incredibly well to the LJP, and can be more easily simulated, due to the increased number of simplifications and assumptions that can be made - namely, that gas has no fixed volume. 

+ I also chose the _LJP_ as it is a common choice for commerical MDSs. It is featured in  LAMMPS - the _Large-scale Atomic/Molecular Massively Parallel Simulator_, from Sandia National Laboratories. LAMMPS is a standard open source library for proper molecular dynamics simulation. However, as an article in the Royal Society of Chemistry pointed out, the _LJP_ may not be the best choice for this simulation, as when simulating many atoms, the simulation reduces range instead of considering every possible atomic potential. As below, I did this in a less naive way than it is normally done to attempt to counteract this problem.


### Two Body
+ LJ Pairwise potential yields most accurate results with two $\ce{Ar}$ Atoms
+ Two atoms are initialised with a position and velocity, and a potential is initialised between them. The potential uses the interatomic distance to yield an energy and a force. The force is applied to each atom, and the atoms are then moved across a time period. 


### Multi-body
+ EAM determines $E_i$, by considering the pairwise potential of atom $i$ to all other atoms, as well as energy needed to embed $i$ in the electron cloud of every other atom present
+ EAM typical use case: inter-ionic energies in metal alloy lattices. EAM does not work where bonds are directional, hence use in metals. Works poorly for covalent substances. For Ar-Ar sim, no directional bonding so still seemingly appropriate despite unconventional use case.
+ EAM vs MEAM: MEAM takes shape of molecule into account when calculating charge density, increasing accuracy for real-world applications. Where molecules are symmetric spheres, $\rho_{EAM} = \rho_{MEAM}$.
+ EAMs are typically used in metals due to their dependance on no directional bonds for accuracy, making them inappropriate for  substances with significant covalent character. Again, Argon being monatomic means that there are no directional bonds present. This, I believe, qualifies the use of the EAM in this simulation despite it being unconventional. 

<br>

### Physical Assumptions
+ Collisions with wall inelastic. Due to fact that with elastic collisions, $\Sigma E$ increased. Somewhat reasonable as simulation runnning at constant 88K
+ Calculating exact coef of restitution beyond my ability; pV=nRT cannot be used as sim violates key ideal gas assumption (no forces between particles)
+ Simulated in 1D
+ Assume Ar atoms point masses
+ All force derived from potential goes into motion; i.e. no energy lost due to rotation of particle

---

## Implementation

### MDS Cycle
+ Stateful; give initial state $n$, calculates state $n+1$; explain how
+ State is made up of:
	- Container: in what box are the atoms held (if any)
	- Atoms: Position and Velocity
	- Potentials: Pairwise potential between atoms
+ States seperated by time (resolution), lower resolution => greater accuracy, but more computationally expensive per unit time.
+ Means corrections needed - possible for next state to be computed outside of wall / other side of other atom, so atom appears tp 'phase through' objects. 

<br>

##  Optimisations
### Two Body
+ Dynamic Resolution - resolution $\propto$ speed<sup>-1</sup> 
+ Circumvents problem where atoms phase through each other / container walls
+ Time complexity of a frame is $O(1)$
+ Time complexity of program is $O(n)$, where $n$ corresponds to number of frames

### Multibody Optimisations
+ **Simplification of EAM approach**. EAM was picked over MEAM as Ar atoms are spherical and symmetrical, thus there would be no difference in approach. Approach taken was to ignore proportion of energy that comes from embedding atom $i$ in the electron cloud of other atoms in the system. This was done for two reasons
	+ Complexity. While this would not change the time complexity of the multibody systen, it adds a significant proportion more computation. 
	+ Accuracy. I believe that ommiting this term, whilst probably making the multibody sim too inaccurate for professional use, does not affect the general result too significantly. EAMs and MEAMs are typically used when calculating intermolecular energies in metal alloys. In metal alloys, molecules (in this case ions) are incredibly close, and the delocalised electrons in the metals make the placement of an ion in the electron cloud very energeticlly significant. However, Argon is monatomic, meaning that there is not much of a total electron cloud to account for - certainly much less significant than in metals. Hence, while there is definitely a significant discrepancy in results, results are theoretically close enough to still be interesting.
+ **Range cutoff**. Standard cutoff $r_c = 2\sigma$ in lots of LJ sims _(RSC Misuse of LJ)_. Opted for different approach
	+ Imagine case where $r_{ij} \ge 2\sigma$. In reality, these atoms experience attractive forces, but if standard $r_c$ used, sim would report no motion. 
	+ Instead, use relative cut off based on the $\Sigma|F|$ that the atom experiences. 
	+ $E_{ref}~\colon=\phi_{ij}$, where $i$ is a selected atom, and $j$ is its closest neighbour.  $\phi_{ij}$ is the potential energy as calculated by the Lennard-Jones potential between atoms $i$ and $j$.  $E_n ~\colon= \phi_{in}$, where $n$ is another atom in the sim. Potentials are only considered where $\frac{E_n}{E_{ref}} > 0.01$
	+ Effect on time complexity. Worst case is still $O(n^2)$, as in rare edge cases it could still be the case that every atom pair needs to be considered. In reality, this approach is similar to a cutoff, vastly limiting the number of pairs that need considering to only a few per atom. 

+ **Parallelisation** - Once all potentials have been assigned, the computation of forces on the atom can be parallelised, as well as the operations where atoms are moved. This has not been done in this simulation, but is the obvious next step. This is included as it was something I had planned to do, but ended up being quite complex.
	+ To do this, each atom $i$ would be picked up by a thread $I$. The thread would then handle the computations for every potential between $i$ and $k: k>i$. 
	+ The atom's force accumulator would have to be modified to become of the form of a queue, to ensure that different threads are not trying to write to the same resource.
	+ Once all of the potential calculations, atom $i$ will be moved by thread $I$

---

## Verification
### Two Body
+ Verification can be achieved by seeing that the atoms maintain an average distance within some tolerance $\epsilon$ of their equilibrium position. The accuracy of the simulation can then be calculated by $\frac{\epsilon}{r_0}$.

### Many Body
+ Due to the simplifications made, I do not expect the many body simulation to be entirely accurate. 
+ I also run into a problem here, in that, while each of the parts of the many body simulation are themselves verifiable, I do not have a good way to verify that the system as a whole works. This is perhaps the largest shortfall of this project. 
+ I had considered that it may be possible to compare the distribution of the $E_k$ of the atoms in my simulation to a Maxwell-Boltzmann distribution, and use the average difference as a test for accuracy. However, I don't think that I would have a large enough sample size for the calculated difference to be meaningful enough. Moreover, Maxwell-Boltzmann is a result of kinetic theory of gases. Thus, it is derived using ideal gas assumptions - significantly, they assume no forces between gas particles. This assumption does not hold true in my simulation, and begins to break down in reality at 90K. 

	 
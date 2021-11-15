# Simulating the motion of argon atoms from initial interatomic distance, and interatomic energy
---
## Project Outline
### Description
+ Project aimed at calculating energy between argon atoms , $E_{PE}$, using a Lennard-Jones pairwise potential. Inter-atomic force, $F$, is then calculated using the derivative of the Lennard-Jones potential with respect to distance ($F=-\frac{dE_{pe}}{dr})$ _(Burrows et. al (2013))_[^1]

+ Using the force calculated, a new position and velocity of each atom is calculated across a period of time. This cycle is then repeated, resulting in atomic motion.


#### Applications of Molecular Dynamics Simulations (MDS)
+ In the real world, MDSs are used throughout science. In Biochemistry, they are used to simulate protein folding. In Physics, they are used to approximate solutions to n-body problems, such as the _Millennium Simulation_. They are used in material sciences to test how stress affects systems, and to predict things like temperature and pressure in virtual systems. _(Zammataro, L 2020)_[^2]

#### Features
+ The behaviour of the simulation is verifiable for two argon atoms in one dimension, logging metrics such as positions, distance, $E_{PE}$, $F$ and collisions with walls of container. 

+ This simulation also can approximate the interatomic energies and forces of many $\ce{Ar}$ atoms. Many-body behaviour for this simulation is unverifiable (see below), and in all likelihood not accurate enough for commercial use. It should, however, be accurate enough to be of interest.

+ Graphing of results is included in this project. Each simulation results in a file of changes in interatomic distance, energy, and force against time. This is then plotted using `matplotlib`

#### Non-Features
+ This project, like the professional LAMMPS (Large-scale Atomic/Molecular Massively Parallel Simulator)_(Thompson et. al (2022)_[^3], does not include visualisation. While a basic Python wrapper can be put round the library, the focus of this project was about the data rather than the graphical output.

+  Temperature is constant throughout, and, as configured, only $\ce{Ar}$ atoms can be used. While this is theoretically easily changeable, variable temperature was added complexity that, for me, was not necessary in understanding and simulating interatomic energies. 

---
## Models

### LJ Potential
+ The Lennard Jones Potential is used to calculate interatomic potential energy, and can be described as follows, where $\ce{K}$ represents Kelvin
$$E_{PE} = 4\epsilon\Big[(\frac{\sigma}{r})^{12} - (\frac{\sigma}{r})^6\Big] ~~K ~~~~~~~~ (1)$$
$$E_{PE} = \frac{A}{r^{12}} - \frac{B}{r^{6}} ~~K ~~~~~~~~~~~~ (2)$$ _(Burrows et. al (2013))_[^1]

+ In order to calculate $E_{PE}$ and $F$, I elected to implement the Lennard-Jones Potential (_LJP_). The potential was introduced in 1924 by Sir John Edward Lennard-Jones to describe the interaction of liquid argon.

+ The potential is comprised of the sum of 2 distinct interactions - attractive interactions, and repulsive interactions (all indented cited as _(Burrows et. al (2013))_[^1])
	+ 3 possible sources for attractive interaction: permanent dipole-dipole, permanent dipole-induced dipole, induced dipole-dipole interactions. 
	 $$\therefore E_{pe{(total~attractive)}} = -\frac{1}{(4\pi\epsilon)^2}\cdot(\frac{0.66\mu^4}{k_BT} + \mu^2\alpha + 0.75\alpha^2I)\cdot(\frac{1}{r^6})~K$$ 
	 where $\epsilon$ is permittivity of  medium, $\mu$ is a dipole moment, $\alpha$ is polarisibility of electron cloud, $I$ is first ionisation energy, and $r$ is interatomic distance.
	+ At constant temperatures for one species, this simplifies to $-\frac{A}{r^6}~K$
	+ Repulsive interactions (at constant temperature) given by $\frac{B}{r^{12}}~K$
	+ $\implies E_{PE(total)} = \frac{B}{r^{12}} -\frac{A}{r^6} J$

+ Since the _LJP_ was introduced for liquid argon _(Zammataro, L 2020)_[^2], I decided argon would be the most sensible element to start off with. Gaseous argon also adheres incredibly well to the LJP, and can be more easily simulated, due to the increased number of simplifications and assumptions that can be made - namely, that gas has no fixed volume. 

+ I also chose the _LJP_ as it is a common choice for commercial MDSs. It is featured in  LAMMPS - the _Large-scale Atomic/Molecular Massively Parallel Simulator_, from Sandia National Laboratories _(Thompson et. al (2022)_[^3].

+ LAMMPS is a standard open source library for proper molecular dynamics simulation. However, as an article in the Royal Society of Chemistry pointed out, the _LJP_ may not be the best choice for this simulation. When simulating many atoms, the simulation reduces range instead of considering every possible atomic potential _(Wang et. al)_[^4] . As below, I strayed from the normal approach in order to try to counteract this problem.

### Two Body
+ LJ Pairwise potential yields most accurate results with two $\ce{Ar}$ Atoms, as it was created to model liquid argon _(Zammataro, L 2020)_[^2]
+ Two atoms are initialised with a position and velocity, and a potential is initialised between them. The potential uses the interatomic distance to yield an energy and a force. The force is applied to each atom, and the atoms are then moved across a time period. 
+ In testing, the Two Body Simulation yielded accuracy of +0.005% accuracy when a frame was computed at a resolution $1\times10^{-7}$ seconds, across 0.3 seconds.


### Multi-body
+ Multi-body Simulations generally conducted using the **Embedded Atom Model**(EAM), or more commonly,  the **Modified Embedded Atom Model**(MEAM)

+ EAM determines $E_i$, by considering the pairwise potential of atom $i$ to all other atoms, as well as energy needed to embed $i$ in the electron cloud of every other atom present _(Zhou, X, Bartlet, N, Sills, R)_[^5]

$$E_i = F_\alpha \left(\sum_{j \neq i}\ \rho_\beta (r_{ij})\right) +
      \frac{1}{2} \sum_{j \neq i} \phi_{\alpha\beta} (r_{ij})$$
	  
+ EAM typical use case: inter-ionic energies in metal alloy lattices. EAM does not work where bonds are directional _(Ackland, G, Bonny, G 2020)_[^6], hence use in metals. Works poorly for covalent substances. For Ar-Ar sim, no directional bonding so still seemingly somewhat appropriate despite unconventional use case.

+ EAM vs MEAM: MEAM takes shape of molecule into account when calculating charge density, increasing accuracy for real-world applications. Where molecules are symmetric spheres, $\rho_{EAM} = \rho_{MEAM}$ _(Ackland, G, Bonny, G 2020)_[^6]

+ This is very much the case with $\ce{Ar}$ molecules, hence, an EAM approach is equivalent to an MEAM approach.

+ EAMs are typically used in metals due to their dependence on no directional bonds for accuracy, making them inappropriate for  substances with significant covalent character. Again, argon being monatomic means that there are no directional bonds present. This, I believe, qualifies the use of the EAM in this simulation despite it being unconventional. 

<br>

### Physical Assumptions
+ Collisions with container walls are **inelastic**. This is a modeling assumption that is incorrect, and had to be implemented due to the fact that with elastic collisions, $\sum E$ of the system increased.

+ What I did to try to mitigate this problem is calculate a coefficient of restitution, $e$, using my simulation. Here, $e$ refers to collisions between the walls of the container and the $\ce{Ar}$ atoms. 

+ I was able to simulate a value which resulted in a reasonable error margin. This was done by assuming perfectly elastic collisions to begin with, and looking at resultant error. Error was, and is, calculated by looking at average interatomic distance, and seeing how this varies from predicted equilibrium bond distance (see **Verification**)

+ This method, however, was scrapped.
	+ **Too specific**. Calculated values for $e$ required re-calibrating when various factors were changed, such as size of container, initial energy of atoms, and initial displacement of atoms. 
	+ **Circular verification**. Calibrated using deviation in interatomic distance. Tested by making sure that deviation in interatomic distance was small. Arguably therefore not a proof of validity

+ In the end, particles stay oscillating together when walls a far enough away from the area of action.

+ Analytically solving for a general expression for a coefficient of restitution is beyond my ability, as this simulation does not happen under ideal gas laws by definition, hence $pV=nRT$ cannot be used to find $e$

<div style="page-break-after: always;"></div>

---

## Implementation
![](chemSim/cycle.svg)

+ Based on a cycle through states. Each state is calculated solely from the previous state.

+ States hold information such as
	+ Atoms: Position, velocity, mass
	+ _LJP_ between atoms: pair of atoms, $E_{PE}$, $F$, interatomic distance, $\ce{Ar}$-$\ce{Ar}$ values for $\sigma$ and $\epsilon$

+ Each state is separated by a period of time. It was found that $1\times10^{-7}$ seconds yielded an accuracy of $+0.005\%$, for 0.3 seconds of motion. 

+ Simulated in **one dimension**. Due to design of software, the jump to three dimensions should not be too difficult and will likely be done in the future. However here it was not done as it adds complexity, and having one dimension does not detract from atomic motion, when the metric used for verification is interatomic distance.

+ Having mentioned ease of implementation, it is not as straight forward as introducing a vector class with a distance method. Steric factors of the $\ce{Ar}$ atoms would need to be considered, and this is currently beyond my ability. 

+ Also, the simulation assumes that all the force calculated from the potential contributes to the motion of each particle (i.e. no loss of energy due to rotation).

+ Particles are modeled as point masses.

---

## Optimisation

### Two Body

+ Dynamic Resolution for very small distances relative to equilibrium distance
	+ As force of repulsion increases with $r^12$,  particles experience large forces as they approach each other.
	+ Hence, as particles get closer, sampling rate should increase to avoid a situation where particles phase through each other.
	+ As mentioned, sampling at a frequency of 100$\ce{ns}$ yields a deviation from equilibrium distance of $0.005\%$, across 0.3s of time. Hence, at equilibrium distance and above, resolution of  100$\ce{ns}$ is used. At shorter distances, resolution decreases $\propto\sqrt r$. This was a fairly arbitrary decision. The square root function was used due to its exponential decrease in the range $1 \le x \le 0$, and the fact that its range is defined as $\sqrt r \ge 0$.
	+ Time complexity of a frame is constant (**only in two body**)
	+ Time complexity of a full simulation is $\mathcal {O(n)}$, where n represents the number of cycles per frame, ignoring writing to file


### Multi-body Optimisations
+ **Simplification of EAM approach**. EAM was picked over MEAM as Ar atoms are spherical and symmetrical, thus there would be no difference in approach (see above). Approach taken was to ignore proportion of energy that comes from embedding atom $i$ in the electron cloud of other atoms in the system. This was done for two reasons
	+ Complexity. While this would not change the time complexity of the multi-body system, it adds significantly more computation. 
	+ Accuracy. I believe that omitting this term, whilst probably making the multi-body sim too inaccurate for professional use, does not affect the general result too significantly. EAMs and MEAMs are typically used when calculating intermolecular energies in metal alloys. 
	+ In metal alloys, molecules (in this case ions) are incredibly close, and the delocalised electrons in the metals make the placement of an ion in the electron cloud very energetically significant. However, argon is monatomic, meaning that there is not much of a total electron cloud to account for - certainly much less significant than in metals. Hence, while there is definitely a significant discrepancy in results, results are theoretically close enough to still be interesting.

+ **Range cutoff**. Standard cutoff $r_c = 2\sigma$ in lots of LJ simulations _(Zammataro, L 2020) [^2]_. Opted for different approach
	+ Imagine case where $r_{ij} \ge 2\sigma$. In reality, these atoms experience attractive forces, but if standard $r_c$ used, simulation would report no motion. 
	+ Instead, use relative cut off based on the $\sum|F|$ that the atom experiences. 
	+ $E_{ref}~\colon=\phi_{ij}$, where $i$ is a selected atom, and $j$ is its closest neighbour.  $\phi_{ij}$ is the potential energy as calculated by the Lennard-Jones potential between atoms $i$ and $j$.  $E_n ~\colon= \phi_{in}$, where $n$ is another atom in the sim. Potentials are only considered where $\frac{E_n}{E_{ref}} > 0.01$
	+ Effect on time complexity. Worst case is still $\mathcal{O(n^2)}$, as in rare edge cases it could still be the case that every atom pair needs to be considered. In reality, this approach is similar to a cutoff, vastly limiting the number of pairs that need considering to only a few per atom. 

+ **Parallelisation** - Once all potentials have been assigned, the computation of forces on the atom can be parallelised, as well as the operations where atoms are moved. **This has not been done in this simulation**, but seemed like the obvious next step. This has been included in the write up as it was something I had planned to do, but ended up being quite complex.
	+ To do this, each atom $i$ would be picked up by a thread $I$. The thread would then handle the computations for every potential between $i$ and $k: k>i$. 
	+ The atom's force accumulator would have to be modified to become of the form of a queue, to ensure that different threads are not trying to write to the same resource.
	+ Once all of the potential calculations, atom $i$ will be moved by thread $I$.
---
	
**N.B.** Due to Amdahl's Law, parallelisation may not have been a particularly fruitful route to take. Amdahl's Law is something I learned about very recently, and is used to predict maximum theoretical performance gains when parallelising a process. It is calculated 

$$\frac{1}{1-p}$$
(_Bryant, R, O'Hallaron, D 2015)_[^7] 
where $p$ is the proportion of total (single-threaded) running time of a program that **cannot be parallelised**. The resulting number after the calculation is a theoretical max speed increase. For instance, if the formula yielded $2$, then your program would have a maximum $2\times$ speed increase. 

Deciding which atoms are interacting is an operation that cannot be parallelised. Neither is calculating the force on atoms once the potentials have been spawned, due to the fact that attributes in an atoms (namely force) will have to be updated by multiple threads in the same cycle. This step is the most significant one that requires synchronisation.

---

## Verification

### Two Body
+ Accuracy achieved by comparing average intermolecular distance to expected value

+ Finding expected equilibrium distance
	+ _LJP_ constant $\epsilon$ is depth of potential well, in Kelvin
	+ Thus, equilibrium distance is distance where energy is minimum
$$E_{PE} = 4\epsilon \Big[(\frac{\sigma}{r})^{12} - (\frac{\sigma}{r})^6\Big] K$$
$$\implies \frac{dE_{PE}}{dr} = \frac{4\epsilon\sigma}{r^2}\Big[6(\frac{\sigma}{r})^5 - 12(\frac{\sigma}{r})^{11}\Big] Knm^{-1}$$ (where distances are in nm)

$$\ce{SP where} ~~ \frac{dE_{PE}}{dr} = 0$$
$$\implies r = 2^{\frac{1}{6}}\cdot\sigma ~nm ~~ \ce{at equilibrium distance}$$

+ For argon, this yields an equilibrium distance of $0.3755$ nm (data for simulation gathered from (White, J, 1999) [^8]

+ Hence percentage error is calculated as
$$\% ~\ce{Error}  = 100\times\frac{r_{avg} - 2^{\frac{1}{6}}\cdot\sigma}{2^{\frac{1}{6}}\cdot\sigma}$$

+ With a constant sample of 100ns, a +0.005% error is calculated


### Many Body
+ Due to the simplifications made, I do not expect the many body simulation to be entirely accurate. 

+ I also run into a problem here, in that, while each of the parts of the many body simulation are themselves verifiable, I do not have a good way to verify that the system as a whole works.

+ I had considered that it may be possible to compare the distribution of the $E_k$ of the atoms in my simulation to a Maxwell-Boltzmann distribution, and use the average difference as a test for accuracy. However, I don't think that I would have a large enough sample size for the calculated difference to be meaningful enough. Moreover, Maxwell-Boltzmann is a result of kinetic theory of gases. Thus, it is derived using ideal gas assumptions - significantly, they assume no forces between gas particles. This assumption does not hold true in my simulation, and begins to break down in reality at 90K. 

<div style="page-break-after: always;"></div>
---
## Bibliography
[^1]: Burrows, A, Holman, J, Parsons, A, Pilling, G, Price, G 2013, _Chemistry^3 introducing inorganic, organic and physical chemistry_, Oxford University Press, Oxford

[^2]: Zammataro, L 2020, _The Lennard-Jones potential. Why the art of molecular dynamics is so fascinating, and why I got so emotionally overwhelmed_ viewed on 11 August 2021 <https://towardsdatascience.com/the-lennard-jones-potential-35b2bae9446c>

[^3]: Thompson, A, Aktulga, H, Berger, R,. Bolintineanu, D , Brown, W,  Crozier, P in 't Veld, P, Kohlmeyer, A,  Moore, S,  Nguyen, T,  Shan, R,  Stevens, M. Tranchida, J, Trott, C,  Plimpton, S, 2022.  _LAMMPS - a flexible simulation tool for particle-based materials modeling at the atomic, meso, and continuum scales_, Comp Phys Comm
		
[^4]: Wang, X, Ramírez-Hinestrosa, S, Dobnikar, J, Frenkel, D, 2020,  _The Lennard-Jones potential: when (not) to use it_ viewed on 11 August 2021 <https://pubs.rsc.org/en/content/articlelanding/2020/CP/C9CP05445F>
		
[^5]: Zhou, X, Bartelt, N, Sills, R, 2021, _Enabling simulations of helium bubble nucleation and growth: A strategy for interatomic potentials_,  Physical Review B 
		
[^6]: Ackland, G, Bonny, G 2020 _Comprehensive Nuclear Materials_ viewed on 11 August <https://doi.org/10.1016/B978-0-12-803581-8.11687-X>
		
[^7]: Bryant, R, O'Hallaron, D (2016) _Computer Systems: A Programmer's Perspective (3 ed.)_, Pearson Education, p. 58, ISBN 978-1-488-67207-1 

[^8]: White, J 1999, _Lennard-Jones as a model for argon and test of extended renormalisation of group calculations_, Journal of Chemical Physics 111
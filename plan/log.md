---
# Initial Project Plan

## Working Title
Simulating inter-atomic forces and energies in a noble gas, and hence accurately modelling the predicted motion of atoms
with respect to time.

## Initial Thoughts and Plans
My idea for this project came about as I wanted to better understand how atoms interacted with each other, and I wanted
to be able to experiment with this concept myself in a computer simulation. I started doing research on both the
chemistry of interatomic interactions, as well as the kind of computer system that I would have to design to be able
to carry out my idea successfully. 

While researching the computational side, I began to read about a type of simulation called a Molecular Dynamics
Simulation, which was focussed entirely on being able to track the behaviour of particles with varying time. Broadly,
an MDS follows 4 main steps, which cycle every time that time is updated. In step one, the system obtains the spacial
configuration of the particles in the simulation. This includes physical properties like position, velocity, and
acceleration. Once these elements are determined, they are used to determine the inter-molecular energy between each
pair of molecules; from the energy, inter-molecular force is derived. Using classical mechanics, it becomes possible to 
calculate the new acceleration of the molecules. Through numerical integration, updated velocity and position are then
found. The cycle restarts, progressing, typically, at the rate of an update every femtosecond.

#### Initially Expected Problems 

I anticipate this project to include many hurdles that require overcoming, in both the chemical and computational
aspects. Chemically speaking, the model used to derive intermolecular energies from the distance between particles is
crucial in ending up with an accurate simulation. 

Computationally speaking, I foresee more problems than in the chemical side. The first problem to overcome lies in the
size of the quantities being dealt with. Due to the way numbers are represented in binary, computers have trouble with 
non-integer values, losing huge amounts of precision, especially with small numbers. In a system dealing with such small
forces, times, and distances, overcoming the floating point problem will be important in ensuring an accurate 
simulation.

Another far more difficult problem to solve will be that of scale. An MDS requires knowledge of interactions between
every particle. Having to know every interaction is combinatorically explosive, and, with even a modest number of 
particles, risks running out of memory, and long computation times. With 2 molecules, there is only 1 interaction to 
consider. With 4, there are 6. with 100, there are almost 5000 interactions, and with 1000 molecules, there are almost
500,000 interactions to consider. This becomes impossible for any regular computer to handle, thus, heavy optimisation
will be required, while keeping the system accurate.

Another problem to consider will be a more practical one - how can the simulation produced be tested? How will I know
how accurate my particle motion is?

#### Potential Solutions

In terms of my first outlined problem, dealing with turning a configuration of the system at a point in time into
intermolecular energies, I am currently considering restricting my simulation to using atoms of only Noble gases, and
modelling the relationship between inter-atomic distance and inter-atomic energy using a Lennard Jones potential.
This does however have limitations [FIND]

The small number problem will have to be overcome through implementation. Depending on what is most appropriate for
different sections of the program, I will try to use Python libraries such as `decimal.Decimal`, which store floating
point numbers as integer ratios. [LOOK AT HOW DECIMAL WORKS]

Scaling the project will be, I think, the most difficult problem to solve. As I outlined, using any sort of meaningful
number of particles will lead to far too much computation to viably be able to do it all. Hence, optimisation will be
needed. My instinct is to begin to look at graphical optimisation techniques such as collision detection in computer
graphics for a starting point, as it deals with many problems similar to this (i.e. moving from 1000s of collision 
checks per second to as few as possible).

In terms of testing the accuracy of my simulation, I have a few ideas about what to do, though these most definitely
need further research. As MDSs are widely used in certain communities, it turns out that there are various Python
libraries maintained by professionals that do MDS. I could start my MDS with the same initial conditions as theirs, and
track properties derived from both, such as temperature. However, deriving temperature from the simulations may be
difficult, and it may not necessarily show that all aspects of my simulation are successful. While I should be able to 
unit test various aspects of my code easily using predefined results, I need to find some more robust integration tests.

## Supervisor's thoughts and advice

My Supervisor's initial thoughts were that this project was doable. He offered me valuable advice in looking at the kind
of things that I would need to consider, as well as ways in which I can extend my project past what I have initially
proposed. He pointed me towards researching the Lennard-Jones potential, as well as encouraged me to limit my project
to only the Noble gases.

## Plan going forward
My plan going forward is relatively straightforward. The first thing that I need to do is research. I already have a 
good idea of what an MDS involves in the broad, general sense, but now I need to research more of the specifics about
how I am going to implement my own. This will involve comparing different intermolecular energy potentials to ensure
that Lennard Jones is the best choice moving forward. I also intend to work through some fixed simulation cycles by hand
on paper before I begin to implement them in Python. In terms of finding an integration test that will allow me to set
success criteria, I will research the feasibility of comparing my simulation with other open source simulations of the
same nature. 

Once I have concluded my research, and have found a way to validate my simulation, I will begin the implementation phase
of the project. I anticipate this to be the most intensive stage by far. To do so, I will break the implementation down
into a number of distinct stages. Firstly, I will just focus on reporting a static interaction between to Ar-Ar atoms
accurately. This should be easy to validate with pre-calculated results which I can do by hand. One I am satisfied with
this, I will implement a cycle, which will update different physical properties of the molecules, such as position and
acceleration vectors, in the hope of being able to accurately model the movement of two argon atoms on a femtosecond by
femtosecond basis. I anticipate these stages to be fairly involved, but hopefully, not too complex. The complexity of
this project will come from scale. Once I can model and report the interaction between two molecules, I will try to
scale the simulation up to cope with more and more molecules. As aforementioned, designing an optimisation algorithm
which is fast enough to run while keeping the simulation accurate will be challenging. I intend to start trying to
tackle this problem with ideas from collision detection. 

If I manage to scale the project to work with a meaningful
number of particles, I can start to implement more than just argon atoms, and see how the simulation handles heavier
noble gases, or even noble gases in more interesting states, such as supercritical helium. I can also look at varying
certain physical factors, such as changing temperature or pressure of the system. I could even try to derive temperature
from the kinetic energy of each atom. 

That is, however, far later down the line in the project, and not included in my immediate plans for the future. Before
my Mid-Project Review, I would like to accurately map the relationship between two atoms over time. From there, I will
see how I think the project should progress.

---
# Mid Project Review

## Final Title of Project
Modelling the motion of a group of atoms due to the inter-atomic forces experienced between each pair of atoms, in Python.

## Outline your progress since your initial meeting with your supervisor, including any obstacles you have overcome. 

### Progress since initial review


Over the summer, I did not progress as much as I would have liked. If I were to repeat the HELP Project, I would have
tried to do more during the break. The main reason for this, I believe, is that I have never attempted a project as 
large as this in a formal setting before. All other large projects that I have worked on have been done at my own pace 
in my free time, and were nowhere near as rigorously documented as the HELP. Hence, I vastly underestimated how much 
time I would require doing things such as build, each component of my system. This was especially true when writing 
tests - something that I had not had much of a need to do before now. 

Good tests, however, proved incredibly useful, and were the reason I was able to solve unexpected problems that arose
with the simulation relatively quickly. The most obvious example of this happened soon into development. 

## Problems

To simulate continuous motion, from fixed force at an instant, I use SUVAT equations (i.e. assume constant acceleration).
This assumption is good enough for small values (>1 femtosecond) **TEST**. To test the motion, I took a function

---
# DO THIS BIT
start at v, s = 0
a = t + 2
=> v = 1/t^2 + t2 + 0
=> s = 1/6t^3 + t^2

and modelled it against
calculating acceleration at a time T, and then using v = u+at to derive new velocity, s=ut+1/2at^2 for displacement

I tested values at t=2^n, n = {0 < n < 10, n is integer}
intended to do 100 frames of motion per increment of t as to be accurate enough,
accidentally did same interval, but over much greater time -> a very large divergence, caught through testing

---

Another problem that I encountered was in keeping the simulation accurate. Doing so many calculations, very high
precision is necessary, as rounding early will cause the calculated result to diverge from the true result quickly.
Computers store floats, by default, using floating point binary - where a bit is defined to have a decimal point
behind it, and everything to the left of the decimal point has the value of 2^-n. This means that floats are inherently
imprecise, as it would require infinite bits to be able to accurately store a given value. 
  The solution to this was to use a Python built-in module called `decimal`. `decimal.Decimal` objects encode
floats accurately to n decimal places, and is the standard solution for programs that require a high level of precision.
This did mean that the program is slower, and that I had to implement my own accurate trigonometric functions
(arctan, cos, sin). This was due to an unexpected incompatibility with `numpy` and `decimal`.

Having addressed this issue, I was able to run an integration test on my two atom, two dimension molecular dynamics sim.
The motion of the atom was fully tested and working, and the program seemed precise enough to yield accurate results.
Having run the first integration test, I encountered a very strange problem. The log file yielded the two atoms moving
in the same direction. Upon further inspection, it seemed that the distance between the particles was staying constant,
and hence the acceleration between particles was the same in every frame. This was quite obviously incorrect. The first
thing that I thought was that I was missing a multiplier of -1 somewhere, and hence each atom was receiving an equal and
identical force, as opposed to an equal and opposite force. I adjusted for this, and no change happened.
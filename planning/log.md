# LJ Project Log

---

## First Plot of Potential 
_09/05/2021_

![Lennard Jones potential of an Ar-Ar interaction](Ar-Ar_lj_1.png)

File hard coded to only deal with Ar-Ar interaction.  
Used [this site](http://www.sklogwiki.org/SklogWiki/index.php/Argon#Lennard-Jones_parameters) for reference data 

---

## Forward Planning
_10/05/2021_

### Requirements
+ Simulate attractive force of two monatomic species
+ Create a Molecular Dynamics Simulation with the aim of simulating the force in real time, and plotting results against 
  theoretical (LJ Potential), as well as `pylj md_simulation` (standard library) (better idea of accuracy needed to be 
  successful will come with more research)
  
+ Use PubChem or ChemSpider to pull relevant info about requested atoms; recognise where an LJ Potential is not 
  appropriate approx. and report (yield output anyway)
  

### Brief Dev Outline
1. ~~Function that returns LJ energy when given distance, epsilon, sigma~~
2. Ability to change inputs, look at differences (i.e. add plotting theoretical functionality)
3. __Parameterisation__
   + API integration; pull requested atoms from PubChem, test theoretical plot for different interactions 
   + can run with experimental data, and quantum mechanical calculations
4. Start on mol dyn sim (before now have played around with `pylj`, be comfortable with maths & chem)
5. UI and tidying

Testing should be written as project goes on
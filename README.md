# Monte-Carlo-Simulation_Wharf
A python code developed to interact with the ABAQUS API in order to generate and store numerical data regarding the collapse load of a wharf structure under a Monte Carlo Simulation.

The simulation scheme is motivated and described below.

1. A wharf structure is supported on 280 piles which exhibit varying degrees of corrosion.
2. Measurements of the corroded piles are known for half of the structure (140 piles).
3. These piles were characterized by individual load-displacement (L-D) curves.
3. A finite-element model was developed in ABAQUS to predict the behavior of that half of the structure.
4. The extent of corrosion, and thus the capacity of the piles is stochastic.
5. Consequently, the behavior of the half of the structure with unknown pile measurements need not be the same.
6. A Monte Carlo simulation approach was taken in order to predict the collapse load of the structure for randomized pile orderings.
7. One-thousand simulations were performed (1000 positional distributions of the 140 piles), and the collapse load variable was statistically characterized in order to better understand the collapse potential of the wharf as a whole.

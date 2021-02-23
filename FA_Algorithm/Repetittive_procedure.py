from FA_Algorithm.search_space import searchSpace
from FA_Algorithm.firefly_info import firefly

import numpy as np

#MINE_BLAST_EXPLOIT = False
FRACTAL_DIFF = False
PSO_MOVEMENT = False

PLOTTING = False

class repProcedure:
    def __init__(self, max_iterations, fireflies_pop, dimensions):

        self.max_iterations = max_iterations
        self.fireflies_pop = fireflies_pop
        self.dimensions = dimensions

        self.s_space = searchSpace()
        self.lower_bound = searchSpace().lower_bound
        self.upper_bound = searchSpace().upper_bound

        # Simple FA initialization
        self.fireflies_vector = [firefly(self.dimensions,
                                         self.lower_bound, self.upper_bound) for _ in range(self.fireflies_pop)]
        self.s_space.fireflies = self.fireflies_vector

        # Initialization of MBA
        self.shrapnel_pieces = np.random.randint(3, 10)

        # Initialization of fractals
        self.new_fractals_per = np.random.randint(3, 10)

    def results(self, plot_iter, independent_runs):

        exploration = []
        for iteration in range(self.max_iterations):

            self.s_space.fireflyEvaluation()
            self.s_space.diversification(self.dimensions, self.fireflies_pop)  # Finding the % of Exploration

            self.s_space.moveFireflies()  # Move the Particles in space with the PSO velocity mechanism

            # if MINE_BLAST_EXPLOIT:
            #     self.s_space.mineBlastExploitation(self.shrapnel_pieces, self.max_iterations, iteration)

            if FRACTAL_DIFF:
                self.s_space.fractalDiffusion(self.max_iterations, self.new_fractals_per)

            if PSO_MOVEMENT:
                self.s_space.psoMovement()

            self.s_space.relocation(self.dimensions)  # Relocate the position if it goes out of bound

            exploration.append(self.s_space.diver_per)
        exploitation = [1 - exploration[_] for _ in range(len(exploration))]

        if plot_iter == independent_runs - 1:

            if PLOTTING:
                from matplotlib import pyplot as plt
                plt.plot(exploration, label='Xpl %')
                plt.plot(exploitation, label='Xpt %')

                plt.ylabel("Exploration - Exploitation %")
                plt.xlabel("Iterations")
                plt.title("CEC10 F17 - SFS")
                plt.legend()
                plt.show()

        return self.s_space.global_best_eval, self.s_space.global_best_position,\
               np.average(exploration), np.average(exploitation)
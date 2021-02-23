# from Xin_She_Yang_Bench_Fun.xin_she_yang_N4_fun import xinSheYangN4 as fitness
# from Xin_She_Yang_Bench_Fun.xin_she_yang_N4_fun import lower_bound, upper_bound

# from CEC10.CEC10 import benchFunctions
# fitness = benchFunctions().function17
# lower_bound = benchFunctions().f17_lower_bound
# upper_bound = benchFunctions().f17_upper_bound

from CEC10_Con.CEC10_Con import benchFunctions
fitness = benchFunctions().function7
lower_bound = benchFunctions().f7_lower_bound
upper_bound = benchFunctions().f7_upper_bound

# from CEC17.CEC17 import benchFunctions
# fitness = benchFunctions().function13
# lower_bound = benchFunctions().lower_bound
# upper_bound = benchFunctions().upper_bound

# from CEC05.CEC05 import benchFunctions
# fitness = benchFunctions().function6
# lower_bound = benchFunctions().f6_lower_bound
# upper_bound = benchFunctions().f6_upper_bound

import numpy as np
from copy import deepcopy

class searchSpace:
    def __init__(self):

        self.lower_bound = lower_bound
        self.upper_bound = upper_bound  # import these from the obj_fun

        self.fireflies = []
        self.alpha = 0.2

        self.global_best_eval = float('inf')
        self.global_best_position = np.array([0.])

        # Diversification
        self.diver_array = np.array([])  # Maybe there is no need to save this, did it for later use
        self.diver_per = None

        # Find out if trapped in local optima
        self.local_optima_counter = 0  # Will be set to zero each time it find a new global best

    def fireflyEvaluation(self):

        # Now I Save the best position and the global best
        for firefly in self.fireflies:

            firefly.position_eval = fitness(firefly.position)  # import fitness

            # # Saving the best position of each particle
            if firefly.position_eval <= firefly.best_position_eval:  # abs if for max and min
                firefly.best_position_eval = firefly.position_eval
                firefly.best_position = firefly.position


            # Saving global best position
            if firefly.position_eval <= self.global_best_eval:
                self.global_best_eval = firefly.position_eval
                self.global_best_position = firefly.position

                self.local_optima_counter = 0
            else:
                self.local_optima_counter += 1

    def moveFireflies(self):

        # Parameters
        self.alpha *= 0.98  # delta
        gamma = 1.  # <--- Change them to your desire or use parameter adaptation
        beta0 = 1

        self.prev_fireflies = deepcopy(self.fireflies)  # copy::deepcopy is from copying the array

        for i in range(len(self.fireflies) - 1):

            dimensions = self.fireflies[i].position.shape[1]

            if self.fireflies[i].position_eval < self.fireflies[i + 1].position_eval:

                r_dist = self.fireflies[i + 1].position - self.fireflies[i].position
                # new_light = β beta
                new_light_attract = beta0 * np.exp(
                    -gamma * r_dist ** 2) * r_dist + self.alpha * np.random.uniform(0, 1, [1, dimensions])

                self.fireflies[i].light_attract = new_light_attract
                self.fireflies[i].movement()

    def fractalDiffusion(self, max_iterations, new_fractals_per):

        for firefly in self.fireflies:
            # std of the gaussian log(gens)/gens  * (BP - GB)
            sigma = abs(np.log(max_iterations) / max_iterations * (firefly.position - self.global_best_position))

            for j in range(new_fractals_per):  # Here j fractals are produced per particle

                if np.random.uniform() <= 0.5:
                    # Gaussian Walk 1 is: G(mu = BestParticle,σ = sigma) +
                    # (rand * BestParticle  - rand * currentParticlePosition)
                    new_position = firefly.position + np.random.normal(
                        loc=abs(self.global_best_position),
                        scale=sigma
                    ) + (np.random.uniform() * self.global_best_position - np.random.uniform() * firefly.position
                         )

                else:
                    # Gaussian Walk 2 is: G(mu = currentParticlePosition, σ = sigma)
                    new_position = firefly.position + np.random.normal(
                        loc=firefly.position,
                        scale=sigma
                    )
                if fitness(firefly.position) < fitness(new_position):
                    firefly.position = new_position

    def psoMovement(self):
        W, c1, c2 = 0.5, 0.5, 0.5  # Parameters, change them to your desire

        for firefly in self.fireflies:  # (W * particle.velocity) + , if Weighted
            new_velocity = (
                    c1 * np.random.uniform()) * (firefly.best_position - firefly.position) + (
                                   c2 * np.random.uniform()) * (self.global_best_position - firefly.position)

            firefly.light_attract = new_velocity
            firefly.movement()

    def diversification(self, dimensions, fireflies_pop):
        # Finding the % of exploration
        i = 0  # This loop can be done easier, fix it later
        for firefly in self.fireflies:

            if i == 0: fireflies_matrix = firefly.position

            else: fireflies_matrix = np.concatenate((fireflies_matrix, firefly.position))

            i = 1

        dim_median = np.median(fireflies_matrix, axis=0)  # The median of each column(dimension) of the particle matrix

        # Average of Diversity of all dimensions
        div_in_iter = np.sum(dim_median - fireflies_matrix) / (fireflies_pop * dimensions)

        self.diver_array = np.append(self.diver_array, div_in_iter)

        max_diver = np.max((abs(self.diver_array)))
        self.diver_per = abs(div_in_iter) / max_diver

    def relocation(self, dimensions):

        # Relocate the position if it goes out of bounds
        for firefly in self.fireflies:

            for i in range(dimensions):

                # Relocation in space
                if firefly.position[0][i] > self.upper_bound or firefly.position[0][i] < self.lower_bound:

                    firefly.position[0][i] = self.lower_bound + (
                            self.upper_bound - self.lower_bound) * np.cos(firefly.position[0][i]) ** 2

                # Relocation at bounds
                # if firefly.position[0][i] > self.upper_bound: firefly.position[0][i] = self.upper_bound
                #
                # elif firefly.position[0][i] < self.lower_bound:  firefly.position[0][i] = self.lower_bound

    ####################################################################################################################
    # def mineBlastExploitation(self, shrapnel_pieces, max_iterations, iteration):
    #
    #     if self.local_optima_counter < max_iterations * 0.1: #iteration <= np.floor(
    #     max_iterations/2) and self.diver_per < 0.5:
    #
    #         i = 0  # Population Counter
    #         for firefly in self.fireflies:
    #
    #             for _ in range(shrapnel_pieces):
    #                 # Calculation of the distance of the shrapnel pieces
    #                 mine_distance = np.sqrt((firefly.position - self.prev_fireflies[i].position) ** 2 + (
    #                         fitness(firefly.position) - fitness(self.prev_fireflies[i].position)) ** 2)
    #
    #                 # Calculation of the direction of the shrapnel pieces
    #                 mine_direction = (fitness(firefly.position) - fitness(self.prev_fireflies[i].position)) / (
    #                         firefly.position - (self.prev_fireflies[i].position + 10**(-8))) # division by zero fix it
    #                                                                                       # added 10**(-8) temporarily
    #                 # Location of the exploding Mine Bomb Particles
    #                 explode_particle = np.multiply(mine_distance,
    #                                                np.random.uniform() * np.cos(2 * np.pi / shrapnel_pieces))
    #
    #                 # New Mine Particles affected by shrapnels (The new positions)
    #                 new_position = explode_particle + np.exp(
    #                     -np.sqrt(abs(mine_direction), abs(mine_distance))) * self.prev_fireflies[i].position
    #
    #                 if fitness(firefly.position) > fitness(new_position):
    #                     firefly.position = new_position
    #
    #             i += 1  # counting the population
    #         else:
    #             pass
    ####################################################################################################################
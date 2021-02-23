
import numpy as np

class firefly:
    def __init__(self, dimensions, lower_bound, upper_bound):

        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.dimensions = dimensions

        self.position = np.array(
            [[(lower_bound + (upper_bound - lower_bound) * np.random.uniform()) for _ in range(self.dimensions)]])

        self.best_position = self.position

        self.position_eval = np.array([float('inf')])
        self.best_position_eval = float('inf')

        self.light_attract = np.array([0 for _ in range(self.dimensions)])


    def movement(self):

        self.position = self.position + self.light_attract
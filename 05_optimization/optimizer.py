from random import randint
from city import BuildingType
import math
from itertools import product
import numpy as np

    
def pythagoras(x, y):
    return math.sqrt(math.pow(x, 2) + math.pow(y, 2))

class Optimizer:
    def __init__(self, city):
        """An optimizer that iteratively optimizes a given city grid."""
        self._city = city

    def step(self, print_info=False):
        """Performs a single optimization step.
        Args:
            print_info (bool):
                Whether to print information about the optimization step.
        """
        return self.parallelized_random(print_info)

    def optimize(self, n_steps=100, print_info=False):
        """
        Runs the optimizer for a fixed number of steps.
        Args:
            n_steps (int):
                The number of optimization steps.
            print_info (bool):
                Whether to print information about the optimization step.
        """
        # TODO: Change this method to add a stopping criterion, e.g. stop when
        #  the score does not improve anymore.
        self._city.reset_grid()
        print("Initial scores: ", self._city.compute_sunlight_scores())
        print("Initial scores sum: ", sum(self._city.compute_sunlight_scores()))
        print("Initial city layout: ")
        self._city.print_plots()
        print("Optimizing...")
        for i in range(n_steps):
            print(f"Step: {i}", end="\r")
            score = self.step(print_info)
            # TODO: Add a stopping criterion here.
        print(f"\nDone! Final score: {score}")

    # this function creates k versions of the grid and applies n-m swaps to each
    # the best version (can be original) is selected and will be the result of this step
    def parallelized_random(self, print_info, k=6, n=2, m=6):
        # create random new version of input
        
        modification_list = [[]] # empty array is to carry over the input as a possible output
        for i in range(k):
            swap_count = randint(n, m)
            swaps = []
            for j in range(swap_count):
                swap = self.random_swap_coords()
                swaps.append(swap)
            modification_list.append(swaps)

        # evaluate random versions
        scores = []    
        for swap_arr in modification_list:
            self.apply_swaps(swap_arr)
            scores.append(self.score())
            self.apply_swaps(reversed(swap_arr))

        # select best
        best = scores.index(max(scores))
        self.apply_swaps(modification_list[best])

        if print_info:
            print("Version sums: ", scores)
            print("New scores sum: ", scores[best])
            print("New city layout: ")
            self._city.print_plots()
        print(scores[best])
        return scores[best]



    def random_swap_coords(self):
        row_size = self._city._plots_per_row
        col_size = self._city._plots_per_col
        row1, col1 = randint(0, row_size - 1), randint(0, col_size - 1)
        row2, col2 = randint(0, row_size - 1), randint(0, col_size - 1)
        return ((row1, col1), (row2, col2))

    def apply_swaps(self, swap_arr):
        for i, current in enumerate(swap_arr):
            ((row1, col1), (row2, col2)) = current
            self._city.swap_buildings(row1, col1, row2, col2)
    
    # rules:
    # 1. skyscrapers/highrises should be near the center
    # 2. houses should be near atleast 3 other houses in the nearby 8 tiles,
    #    to make the neighbourhoods more fun
    # 3. the parks should be spread evenly
    #    (every non-empty tile should be as close as possible to the nearest park)
    # 4. To encourage competitiveness each office should be directly neighboured by another office
    # 5. To make a compact city, empty tiles should be away from the center and near the border
    def score(self):
        score = 0

        num_rows = self._city.rows
        num_cols = self._city.cols
        for i in range(num_rows):
            for j in range(num_cols):
                type = self._city.get_building_type(i, j)
                if type == BuildingType.EMPTY: # rule 5
                    offset_row = i - num_rows/2
                    offset_col = j - num_cols/2
                    score += np.clip(pythagoras(offset_row, offset_col) / 20, 0, 1)
                elif type == BuildingType.HIGHRISE or type == BuildingType.SKYSCRAPER: # rule 1
                    offset_row = i - num_rows/2
                    offset_col = j - num_cols/2
                    distance = pythagoras(offset_row, offset_col)
                     
                    score += (1 - np.clip(distance-5 / 15, 0, 1)) * 0.8
                elif type == BuildingType.HOUSE: # rule 2
                    neighbours = []
                    neighbours.append((i-1,j-1))
                    neighbours.append((i-1,j+1))
                    neighbours.append((i+1,j-1))
                    neighbours.append((i+1,j+1))
                    neighbours.append((i,j-1))
                    neighbours.append((i,j+1))
                    neighbours.append((i+1,j))
                    neighbours.append((i+1,j))
                    types = [self._city.get_building_type(row, col) for (row, col) in neighbours if 0 <= row < num_rows and 0 <= col < num_cols]
                    if types.count(BuildingType.HOUSE) >= 3:
                        score += 0.8
                elif type == BuildingType.OFFICE: # rule 4
                    neighbours = []
                    neighbours.append((i,j-1))
                    neighbours.append((i,j+1))
                    neighbours.append((i+1,j))
                    neighbours.append((i+1,j))
                    types = [self._city.get_building_type(row, col) for (row, col) in neighbours if 0 <= row < num_rows and 0 <= col < num_cols]
                    if BuildingType.OFFICE in types:
                        score += 0.8
                if type != BuildingType.PARK and type != BuildingType.EMPTY: # rule 3
                    row_list = range(i-3, i+4)
                    col_list = range(j-3, j+4)
                    neighbours = product(row_list, col_list)
                    types = [(row, col, self._city.get_building_type(row, col)) for (row, col) in neighbours if 0 <= row < num_rows and 0 <= col < num_cols]
                    park_distances = [pythagoras(row-i, col-j) for (row, col, bt) in types if bt is BuildingType.PARK]
                    closest = min(park_distances, default=5)
                    if closest <= 1.5:
                        score += 0.2
                    elif closest <= 3.5:
                        score += (closest - 1.5) * 0.1
                if type == BuildingType.PARK:
                    score += 1
        return score
    

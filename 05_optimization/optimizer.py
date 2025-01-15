from random import randint


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
        # TODO: Implement your optimization algorithm here.
        #  Hint: You can use the following code to swap two buildings:
        row1, col1 = randint(0, self._city._plots_per_row - 1), randint(0, self._city._plots_per_col - 1)
        row2, col2 = randint(0, self._city._plots_per_row - 1), randint(0, self._city._plots_per_col - 1)
        self._city.swap_buildings(row1, col1, row2, col2)
        #  Hint: You can use the function `compute_sunlight_scores` of the City class
        #  to compute the sunlight scores
        new_scores = self._city.compute_sunlight_scores()
        if print_info:
            print("New scores: ", new_scores)
            print("New scores sum: ", sum(new_scores))
            print("New city layout: ")
            self._city.print_plots()
        return sum(new_scores)

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
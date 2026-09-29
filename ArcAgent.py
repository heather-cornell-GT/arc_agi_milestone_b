import numpy as np

from ArcProblem import ArcProblem
from ArcData import ArcData
from ArcSet import ArcSet

class ArcAgent:
    def __init__(self):
        """
        You may add additional variables to this init method. Be aware that it gets called only once
        and then the make_predictions method will get called several times.
        """
        """
                making rule sets so that i can apply them easier later. 
                this is giving the agent a 'helping hand'
                """
        self.rules = [
            "rotate_90",
            "rotate_180",
            "rotate_270",
            "flip_up_down",
            "flip_left_right",
            "transpose",
            "crop_nonzero",
            "left_right_and",
            "left_right_or",
            "left_right_nor",
            "top_bottom_and",
            "top_bottom_or",
            "top_bottom_nor",
            "no_change",  # used when only the colors change
        ]


    def make_predictions(self, arc_problem: ArcProblem) -> list[np.ndarray]:
        """
        Write the code in this method to solve the incoming ArcProblem.
        Your agent will receive 1 problem at a time.

        You can add up to THREE (3) the predictions to the
        predictions list provided below that you need to
        return at the end of this method.

        In the Autograder, the test data output in the arc problem will be set to None
        so your agent cannot peek at the answer (even on the public problems).

        Also, if you return more than 3 predictions in the list it
        is considered an ERROR and the test will be automatically
        marked as INCORRECT.

        A maximum of three distinct predictions is returned.

        agent tries 3 general rules:
        1. rotate the grid 180 degrees.
        2. crop empty space around the non-black object.
        3. learn a color replacement rule.

        then, a rule is only used if it works for every training example.
        """

        predictions, training  = [], []

        #grab the training examples the same way we did in Milestone A
        for pair in arc_problem.training_set():
            train_input = pair.get_input_data().data()
            train_output = pair.get_output_data().data()
            training.append((train_input, train_output))

        test_input = arc_problem.test_set().get_input_data().data()

        #testing out each of the rules defined earlier one by one
        for rule_name in self.rules:

    def apply_rule(self, rule_name, grid):
        """
        apply each rule to the grid and if it works, return it
        """
        if rule_name == "no_change":
            return grid.copy()
        if rule_name == "rotate_90":
            return np.rot90(grid, 1)
        if rule_name == "rotate_180":
            return np.rot90(grid, 2)
        if rule_name == "rotate_270":
            return np.rot90(grid, 3)
        if rule_name == "flip_up_down":
            return np.flipud(grid)
        if rule_name == "flip_left_right":
            return np.fliplr(grid)
        if rule_name == "transpose":
            return grid.T
        if rule_name == "crop_nonzero":
            return self.crop_nonzero(grid)


        if rule_name.startswith("left_right_"):
            operation = rule_name.replace("left_right_", "")
            return self.compare_halves(grid, "left_right", operation)
        if rule_name.startswith("top_bottom_"):
            operation = rule_name.replace("top_bottom_", "")
            return self.compare_halves(grid, "top_bottom", operation)
        return None



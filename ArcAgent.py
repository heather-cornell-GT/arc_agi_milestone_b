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
        pass

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
        predictions = []

        training = []
        for pair in arc_problem.training_set():
            train_input = pair.get_input_data().data()
            train_output = pair.get_output_data().data()
            training.append((train_input, train_output))

        test_input = arc_problem.test_set().get_input_data().data()


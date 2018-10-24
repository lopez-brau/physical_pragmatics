import itertools as it
import numpy as np
import sys

# Define hyperparameters.
COST_RATIO = 1.0
COST_TABLE = {0: 0, 1: 2, 2: 4, 3: 6}
GRIDWORLD = True
GRIDWORLD_MAX_ACTION = 4
GRIDWORLD_MAX_SAMPLES = 25
MAX_SAMPLES = 100
MAX_VALUE = 10
NUM_ACTIONS = 2
SAMPLING = False
NATURAL_COST = np.array([int(sys.argv[1]), int(sys.argv[2])])
ENFORCER_ACTIONS = np.array([[1, 0], [2, 0], [3, 0]])
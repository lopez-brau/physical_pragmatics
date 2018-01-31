import numpy as np
import sys

# Define hyperparameters.
COST_RATIO = 1.0
COST_TABLE = {0: 0, 1: 6, 2: 8}
GRIDWORLD = True
MAX_SAMPLES = 100
MAX_VALUE = 10
METHOD = "flat"
NATURAL_COST = np.array([int(sys.argv[1]), int(sys.argv[2])])
NUM_ACTIONS = 2
SAMPLING = False

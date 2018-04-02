import numpy as np
import sys

# 
NATURAL_COST = np.array([int(sys.argv[1]), int(sys.argv[2])])
# COOPERATION = float(sys.argv[6])

# Define hyperparameters.
COST_RATIO = 1.0
COST_TABLE = {0: 0, 1: 6, 2: 8, 3: 10}
GRIDWORLD = True
GRIDWORLD_MAX_ACTION = 4
GRIDWORLD_MAX_SAMPLES = 16
MAX_SAMPLES = 100
MAX_VALUE = 10
NUM_ACTIONS = 2
SAMPLING = False

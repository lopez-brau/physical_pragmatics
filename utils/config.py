import numpy as np
import sys

# Define hyperparameters.
# COOPERATION = float(sys.argv[6])
COST_RATIO = 1.0
COST_TABLE = {0: 0, 1: 6, 2: 8, 3: 10}
# ENFORCER_ACTION = np.array([int(sys.argv[3]), int(sys.argv[4])])
# ENFORCER_REWARD = np.array([0, int(sys.argv[5])])
GRIDWORLD = True
GRIDWORLD_MAX_ACTION = 4
GRIDWORLD_MAX_SAMPLES = 16
MAX_SAMPLES = 100
MAX_VALUE = 10
METHOD = "proportional"
NATURAL_COST = np.array([int(sys.argv[1]), int(sys.argv[2])])
NUM_ACTIONS = 2
SAMPLING = False

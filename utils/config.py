import numpy as np
import sys

# Define hyperparameters.
# COOPERATION = float(sys.argv[6])
COST_RATIO = 1.0
COST_TABLE = {0: 0, 1: 6, 2: 8, 3: 10}
# ENFORCER_ACTION = np.array([int(sys.argv[3]), int(sys.argv[4])])
# ENFORCER_REWARD = np.array([0, int(sys.argv[5])])
GRIDWORLD = False
MAX_SAMPLES = 100
MAX_VALUE = 10
METHOD = "confidence"
# NATURAL_COST = np.array([int(sys.argv[1]), int(sys.argv[2])])
NATURAL_COST = np.array([0, 0])
NUM_ACTIONS = 2
SAMPLING = False

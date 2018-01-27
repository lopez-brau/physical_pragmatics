import numpy as np
import sys

# Define hyperparameters.
COST_RATIO = 1.0
MAX_SAMPLES = 100
MAX_VALUE = 10
METHOD = "flat"
NATURAL_COST = np.array([int(sys.argv[1]), int(sys.argv[2])])
NUM_ACTIONS = 2
SAMPLING = False

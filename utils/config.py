import itertools as it
import numpy as np
import sys

PATH = "D:/Research/social_pragmatics/"
# Define the ratio between the cost the enforcer pays to act versus the cost
# the enforcer incurs on the actor.
COST_RATIO = 1.0
COST_TABLE = {0: 0, 1: 2, 2: 4, 3: 6}

# Set whether we're evaluating this on a specific gridworld or in the standard case.
GRIDWORLD = False

# If in a gridworld, set the max value for an action/reward.
GRIDWORLD_MAX_SAMPLES = 25
GRIDWORLD_MAX_VALUE = 4
MAX_SAMPLES = 100
MAX_VALUE = 10
NUM_ACTIONS = 2
SAMPLING = False
NATURAL_COST = np.array([int(sys.argv[1]), int(sys.argv[2])])

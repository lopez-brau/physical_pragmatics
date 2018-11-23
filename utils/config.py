import itertools as it
import numpy as np
import sys

# Set the path.
PATH = "D:/Research/social_pragmatics/"

# Define the ratio between the cost the enforcer pays to act versus the cost
# the enforcer incurs on the actor.
COST_RATIO = 1.0
COST_TABLE = {0: 0, 1: 2, 2: 4, 3: 6}

# Set the max number of actions agents can consider.
NUM_ACTIONS = 2

# Set whether we're evaluating this on a specific gridworld or in the standard 
# case.
GRIDWORLD = False

# Set the max value for actions (but not rewards) in a gridworld environment.
GRIDWORLD_MAX_VALUE = 4

# Set the max value for actions and rewards in a non-gridworld environment.
MAX_VALUE = 10

# Determine if we're using an exhaustive or sampling approach. If we're using
# sampling, set the max number of samples depending on the environment.
SAMPLING = False
GRIDWORLD_MAX_SAMPLES = 25
MAX_SAMPLES = 100

# Have the user provide environmental barriers/constraints.
NATURAL_COST = np.array([int(sys.argv[1]), int(sys.argv[2])])

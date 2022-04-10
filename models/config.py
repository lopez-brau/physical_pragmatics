import os
import sys

# Set the path and check that it exists.
PATH = "C:/Data/Research/pragmatics_refactor/"
if os.path.exists(PATH) == False:
    sys.exit("Please update the project path in `utils/config.py`.")
else:
    os.chdir(PATH)

# Define the environmental barriers/constraints.
NATURAL_COST = [float(sys.argv[1]), float(sys.argv[2])]

# Define a scaling parameter for the costs the decider and enforcer incur.
DECIDER_COST_RATIO = 2.0
ENFORCER_COST_RATIO = 2.0

# Set whether or not the models use cached results.
CACHE = True

# Set whether we're evaluating over gridworlds or standard environments.
GRIDWORLD = True

# Set the environment to append to cache filenames.
ENVIRONMENT = "gridworld" if GRIDWORLD == True else "standard"

# Set the max number of actions agents can consider.
NUM_ACTIONS = 2

# Set the max value for actions and rewards.
MAX_ACTION = 4 if GRIDWORLD == True else 10
MAX_REWARD = 10

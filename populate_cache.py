import itertools as it
import numpy as np
import time

from models import *
from utils import *

if __name__ == "__main__":
	# Set up the rationality set.
	rationality_set = np.array([0.01, 0.1, 1.0])

	# Cache the actor_no_ToM model.
	if SAMPLING == True:
		actor_rewards = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS))
		enforcer_actions = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS)) if GRIDWORLD != True else \
						   np.random.choice(GRIDWORLD_MAX_VALUE, (GRIDWORLD_MAX_SAMPLES, NUM_ACTIONS))
	else:
		actor_rewards = np.array(list(it.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS)))
		enforcer_actions = np.array(list(it.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS))) if GRIDWORLD != True else \
						   np.array(list(it.product(np.arange(GRIDWORLD_MAX_VALUE), repeat=NUM_ACTIONS)))

	start_time = time.time()
	cache_actor_no_ToM(actor_no_ToM, rationality_set, actor_rewards, enforcer_actions)
	print("Cache time for actor_no_ToM: " + str(time.time()-start_time))

	# Cache the enforcer_no_ToM model.
	if SAMPLING == True:
		enforcer_rewards = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS))
	else:
		enforcer_rewards = np.array(list(it.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS)))

	start_time = time.time()
	cache_enforcer_no_ToM(enforcer, rationality_set, enforcer_rewards)
	print("Cache time for enforcer_no_ToM: " + str(time.time()-start_time))
	
	# Set up the method and cooperation sets for the actor_ToM model.
	methods = ["confidence", "flat", "proportional"]
	cooperation_set = np.array([-10.0, -5.0, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 5.0, 10.0, 20.0])

	# Cache the actor_ToM model.
	if SAMPLING == True:
		actor_rewards = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS))
		enforcer_actions = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS)) if GRIDWORLD != True else \
						   np.random.choice(GRIDWORLD_MAX_VALUE, (GRIDWORLD_MAX_SAMPLES, NUM_ACTIONS))
	else:
		actor_rewards = np.array(list(it.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS)))
		enforcer_actions = np.array(list(it.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS))) if GRIDWORLD != True else \
						   np.array(list(it.product(np.arange(GRIDWORLD_MAX_VALUE), repeat=NUM_ACTIONS)))

	start_time = time.time()
	cache_actor_ToM(actor_ToM, rationality_set, actor_rewards, enforcer_actions, methods, cooperation_set)
	print("Cache time for actor_ToM: " + str(time.time()-start_time))

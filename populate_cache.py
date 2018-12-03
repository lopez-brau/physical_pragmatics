import itertools as it
import numpy as np
import time

from models import *
from utils import *

if __name__ == "__main__":
	# Set up the rationality set.
	rationality_set = np.array([0.01, 0.1, 1.0])

	# Set up the range of ToM that actors can have (exclude the case of no ToM to avoid redundant computations).
	p_set = np.round(np.linspace(0.1, 1.0, num=10), decimals=1)

	# Set up the ways in which the actor can integrate social reward.
	social_reward = {
		"confidence": np.array([-25.0, -20.0, -15.0, -10.0, -5.0, 0.0, 5.0, 10.0, 15.0, 20.0, 25.0]),
		"preference": np.array([-25.0, -20.0, -15.0, -10.0, -5.0, 0.0, 5.0, 10.0, 15.0, 20.0, 25.0]),
		"proportional": np.array([-2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5])
	}

	# Set up the 
	if SAMPLING == True:
		actor_rewards = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS))
		enforcer_actions = np.random.choice(GRIDWORLD_MAX_VALUE, (GRIDWORLD_MAX_SAMPLES, NUM_ACTIONS)) if \
						   GRIDWORLD == True else np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS))
		enforcer_rewards = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS))
	else:
		actor_rewards = np.array(list(it.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS)))
		enforcer_actions = np.array(list(it.product(np.arange(GRIDWORLD_MAX_VALUE), repeat=NUM_ACTIONS))) if \
						   GRIDWORLD == True else np.array(list(it.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS)))
		enforcer_rewards = np.array(list(it.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS)))

	# Cache the actor_no_ToM model.
	start_time = time.time()
	cache_actor_no_ToM(actor_no_ToM, rationality_set, actor_rewards, enforcer_actions)
	print("Cache time for actor_no_ToM: " + str(time.time()-start_time))

	# Cache the enforcer_no_ToM model.
	start_time = time.time()
	cache_enforcer_no_ToM(enforcer, rationality_set, enforcer_rewards)
	print("Cache time for enforcer_no_ToM: " + str(time.time()-start_time))
	
	# Cache the actor_ToM model.
	start_time = time.time()
	cache_actor_ToM(actor_ToM, rationality_set, actor_rewards, enforcer_actions, social_reward)
	print("Cache time for actor_ToM: " + str(time.time()-start_time))

	# Cache the enforcer_ToM model.
	start_time = time.time()
	cache_enforcer_ToM(enforcer, rationality_set, enforcer_actions, p_set, social_reward)
	print("Cache time for enforcer_ToM: " + str(time.time()-start_time))

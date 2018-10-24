from models import *
from utils import *

import itertools as it
import numpy as np
import time

if __name__ == "__main__":
	# Set the rationality parameter.
	rationality = 1.0

	# Cache the agent_no_ToM model.
	enforcer_actions = ENFORCER_ACTIONS
	if SAMPLING == True:
		agent_rewards = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS))
		# enforcer_actions = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS)) if GRIDWORLD != True else \
		# 				   np.random.choice(GRIDWORLD_MAX_ACTION, (GRIDWORLD_MAX_SAMPLES, NUM_ACTIONS))
	else:
		agent_rewards = np.array(list(it.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS)))
		# enforcer_actions = np.array(list(it.product(np.arange(MAX_VALUE), repeat_NUM_ACTIONS))) if GRIDWORLD != True else \
		# 				   np.array(list(it.product(np.arange(GRIDWORLD_MAX_ACTION), repeat=NUM_ACTIONS)))
	start_time = time.time()
	cache_agent_no_ToM(agent_no_ToM, rationality, agent_rewards, enforcer_actions)
	print("Cache time for agent_no_ToM: " + str(time.time()-start_time))

	# Cache the enforcer_no_ToM model.
	if SAMPLING == True:
		enforcer_rewards = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS))
	else:
		enforcer_rewards = np.array(list(it.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS)))
	start_time = time.time()
	cache_enforcer_no_ToM(enforcer, rationality, enforcer_rewards)
	print("Cache time for enforcer_no_ToM: " + str(time.time()-start_time))
	
	# Cache the agent_ToM model.
	enforcer_actions = ENFORCER_ACTIONS
	if SAMPLING == True:
		agent_rewards = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS))
		# enforcer_actions = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS)) if GRIDWORLD != True else \
		# 				   np.random.choice(GRIDWORLD_MAX_ACTION, (GRIDWORLD_MAX_SAMPLES, NUM_ACTIONS))
	else:
		agent_rewards = np.array(list(it.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS)))
		# enforcer_actions = np.array(list(it.product(np.arange(MAX_VALUE), repeat_NUM_ACTIONS))) if GRIDWORLD != True else \
		# 				   np.array(list(it.product(np.arange(GRIDWORLD_MAX_ACTION), repeat=NUM_ACTIONS)))

	methods = ["confidence", "flat", "proportional"]
	cooperation_set = np.array([-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 5.0])
	start_time = time.time()
	cache_agent_ToM(agent_ToM, rationality, agent_rewards, enforcer_actions, methods, cooperation_set)
	print("Cache time for agent_ToM: " + str(time.time()-start_time))

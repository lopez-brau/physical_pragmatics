from models import * 
from utils import *

import csv
import itertools as it
import matplotlib.pyplot as plt
import numpy as np
import time

def main(operation):
	# Cache enforcer reasoning about an agent with no ToM.
	if operation == "cache_enforcer_no_ToM":
		if SAMPLING == True:
			enforcer_rewards = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS))
		else: 
			enforcer_rewards = np.array(list(it.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS)))
		cache_enforcer_no_ToM(enforcer, rationality, enforcer_rewards)

	# Cache agent reasoning about an enforcer reasoning about an agent with no ToM.
	elif operation == "cache_agent_ToM":
		if SAMPLING == True:
			agent_rewards = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS))
			enforcer_actions = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS))
		else:	
			agent_rewards = np.array(list(it.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS)))
			enforcer_actions = np.array(list(it.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS)))
		cooperation_set = np.array([-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 5.0])
		cache_agent_ToM(agent_ToM, rationality, agent_rewards, enforcer_actions, cooperation_set)

	# Enforcer reasoning about an agent with no ToM.
	elif operation == "enforcer_no_ToM":
		start_time = time.time()
		x1 = enforcer(rationality, enforcer_reward, plot=True)
		print(time.time()-start_time)
		return x1

	# Agent reasoning about an enforcer reasoning about an agent with no ToM.
	elif operation == "agent_ToM":
		start_time = time.time()
		x2 = agent_ToM(rationality, agent_reward, enforcer_action, cooperation, cache=True, plot=True)
		print(time.time()-start_time)

	# Enforcer reasoning about an agent with ToM.
	elif operation == "enforcer_ToM":
		start_time = time.time()
		x3 = enforcer(rationality, enforcer_reward, p=p, cooperation=cooperation, plot=True)
		print(time.time()-start_time)

if __name__ == "__main__":
	agent_reward = np.array([9, 0])
	enforcer_reward = np.array([0, 9])
	enforcer_action = np.array([1, 0])

	rationality = 0.1
	cooperation = 2.0
	p = 1.0

	main("cache_agent_ToM")


	# enforcer_reward = np.array([0, 9])
	# cooperation = 2.0
	# enforcer_actions = [[2, 0], [1, 0], [0, 0], [3, 0], [2, 0], [1, 0], [0, 0], [3, 0], [2, 0], [1, 0], [0, 0], [3, 0], \
	# 					[2, 0], [1, 0], [0, 0], [3, 0], [2, 0], [1, 0], [0, 0], [3, 0], [2, 0], [1, 0], [0, 0], [3, 0], \
	# 					[2, 0], [1, 0], [0, 0], [3, 0], [2, 0], [1, 0], [0, 0], [3, 0], [2, 0], [1, 0], [0, 0], [3, 0]]


	# predictions = observer("agent_reward_and_p", rationality, enforcer_reward=ENFORCER_REWARD, cooperation=COOPERATION, \
	# 					   enforcer_action=ENFORCER_ACTION)

	# path = "data/model_comparisons/"
	# filename = path + str(COOPERATION) + "/" + str(NATURAL_COST) + "_" + str(ENFORCER_ACTION) + ".txt"
	# with open(filename, "w", newline="") as file:
	# 	writer = csv.writer(file)
	# 	writer.writerows(predictions)
	# print("Done!")

	# Observer reasoning about the enforcer's beliefs about the agent reward and degree of ToM.
	# start_time = time.time()
	# enforcer_actions = np.array([[0, 0], [1, 0], [2, 0], [3, 0]])
	# path = "predictions/data/gridworld_nc_distance_3/"
	# for enforcer_action in enforcer_actions:
	# 	predictions = observer("agent_reward_and_p", rationality, enforcer_reward=enforcer_reward, cooperation=cooperation, \
	# 						   enforcer_action=enforcer_action)
	# 	print(time.time()-start_time)

		# filename = path + str(cooperation) + "/" + str(NATURAL_COST) + "_" + str(enforcer_action) + ".txt"
		# with open(filename, "w", newline="") as file:
		# 	writer = csv.writer(file)
		# 	writer.writerows(predictions)

from models import * 
from utils import *

import csv
import itertools as it
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import time

if __name__ == "__main__":

	# natural_costs = [[2, 2], [2, 2], [2, 2], [2, 2], [2, 3], [2, 3], [2, 3], [2, 3], [2, 4], [2, 4], [2, 4], [2, 4], \
	#  				 [3, 2], [3, 2], [3, 2], [3, 2], [3, 3], [3, 3], [3, 3], [3, 3], [3, 4], [3, 4], [3, 4], [3, 4],  \
	#  				 [4, 2], [4, 2], [4, 2], [4, 2], [4, 3], [4, 3], [4, 3], [4, 3], [4, 4], [4, 4], [4, 4], [4, 4]]
	# enforcer_actions = [[2, 0], [1, 0], [0, 0], [3, 0], [2, 0], [1, 0], [0, 0], [3, 0], [2, 0], [1, 0], [0, 0], [3, 0], \
	# 					[2, 0], [1, 0], [0, 0], [3, 0], [2, 0], [1, 0], [0, 0], [3, 0], [2, 0], [1, 0], [0, 0], [3, 0], \
	# 					[2, 0], [1, 0], [0, 0], [3, 0], [2, 0], [1, 0], [0, 0], [3, 0], [2, 0], [1, 0], [0, 0], [3, 0]]
	
	# enforcer_rewards = np.array(list(it.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS)))
	
	# cooperation_set = np.array([-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 5.0])

	# start_time = time.time()	
	# rationality = 0.1
	# agent_rewards = np.array(list(it.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS)))
	# enforcer_actions = np.array(list(it.product(np.arange(GRIDWORLD_MAX_ACTION), repeat=NUM_ACTIONS)))
	# cache_agent_no_ToM(agent_no_ToM, rationality, agent_rewards, enforcer_actions)
	# print(time.time()-start_time)

	# start_time = time.time()
	# rationality = 0.1
	# enforcer_rewards = np.array(list(it.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS)))
	# cache_enforcer_no_ToM(enforcer, rationality, enforcer_rewards)
	# print(time.time()-start_time)
	
	# start_time = time.time()
	# rationality = 0.1
	# agent_rewards = np.array(list(it.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS)))
	# enforcer_actions = np.array(list(it.product(np.arange(GRIDWORLD_MAX_ACTION), repeat=NUM_ACTIONS)))
	# cooperation_set = np.array([-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 5.0])
	# cache_agent_ToM(agent_ToM, rationality, agent_rewards, enforcer_actions, cooperation_set)
	# print(time.time()-start_time)

	
	enforcer_actions = np.array(list(it.product(np.arange(GRIDWORLD_MAX_ACTION), repeat=NUM_ACTIONS)))
	rationality = 0.1
	enforcer_reward = np.array([0, 9])
	p_set = np.linspace(0.0, 1.0, num=11)
	cooperation = 2.0
	for enforcer_action in enforcer_actions:
		start_time = time.time()
		predictions = observer("agent_reward_and_p", rationality, enforcer_reward=enforcer_reward, p_set=p_set, \
							   cooperation=cooperation, enforcer_action=enforcer_action, cache=True)
		print(time.time()-start_time)

		filename = "data/model/" + str(NATURAL_COST) + "_" + str(enforcer_action) + ".txt"
		with open(filename, "w", newline="") as file:
			writer = csv.writer(file)
			writer.writerows(predictions)
	
	sys.exit("Done with one iteration.")

	predictions = []
	path = "data/model/"
	with open("temp.txt", "r") as file:
		reader = csv.reader(file)
		for row in reader:
			predictions.append([float(num) for num in row])
	predictions = np.array(predictions)


	p1 = predictions[56]
	print(p1)
	predictions = predictions.reshape(MAX_VALUE, MAX_VALUE, p_set.size)
	p2 = predictions[5][6]
	print(p2)
	print(p1-p2)
	prob_A = np.sum(predictions, axis=(1, 2))
	prob_B = np.sum(predictions, axis=(0, 2))
	prob_p = np.sum(predictions, axis=(0, 1))
	expected_A = np.sum(np.multiply(prob_A, np.arange(10)))
	expected_B = np.sum(np.multiply(prob_B, np.arange(10)))
	expected_p = np.sum(np.multiply(prob_p, np.arange(11)/10))
	print(expected_A)
	print(expected_B)
	print(expected_p)

	with open("temp1.txt", "w", newline="") as file:
		writer = csv.writer(file)
		writer.writerow([expected_A, expected_B, expected_p])


	# enforcer_rewards = [[3, 0], [0, 3], [0, 9]]
	# cooperation_set = [1.0, 1.5, 2.0]
	# enforcer_reward = [0, 9]
	# cooperation = 2.0
	# for i in range(len(natural_costs)):
	# 	os.system("python main.py %d %d %d %d %d %f" % \
	# 		(natural_costs[i][0], natural_costs[i][1], enforcer_actions[i][0], enforcer_actions[i][1], enforcer_reward[1], cooperation))

	# predictions = observer("agent_reward_and_p", rationality, enforcer_reward=ENFORCER_REWARD, cooperation=COOPERATION, \
	# 					   enforcer_action=ENFORCER_ACTION)

	# path = "data/model_comparisons/"
	# filename = path + str(COOPERATION) + "/" + str(NATURAL_COST) + "_" + str(ENFORCER_ACTION) + ".txt"
	# with open(filename, "w", newline="") as file:
	# 	writer = csv.writer(file)
	# 	writer.writerows(predictions)
	# print("Done!")

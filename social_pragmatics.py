import numpy as np
import matplotlib.pyplot as plt
import itertools
import time
import sys
import csv

from util import softmax
from util import cooperative_reward
from util import cache_dumb_enforcer
from util import cache_smart_enforcer
from util import retrieve

MAX_VALUE = 10
NUM_ACTIONS = 2
MAX_SAMPLES = 100
COST_RATIO = 1

PATH = "D:/Home/Research/social_pragmatics/"

def dumb_agent(agent_reward, agent_cost, rationality):
	U = agent_reward - agent_cost
	action_probabilities = softmax(U, rationality)

	return action_probabilities

def smart_agent(agent_reward, agent_cost, enforcer_action, rationality, cooperation, cache=False, plot=False):
	# Set up the likelihood space.
	space = tuple([MAX_VALUE for action in np.arange(NUM_ACTIONS)])
	likelihood = np.zeros(space)
	
	# Generate possible enforcer rewards. Use random sampling if problem space
	# is bigger than MAX_SAMPLES.
	size = min(np.prod(space), MAX_SAMPLES)
	if size > MAX_SAMPLES:
		enforcer_rewards = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS))
	else:
		enforcer_rewards = list(itertools.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS))

	# Compute the likelihood.
	if cache == True:
		for enforcer_reward in enforcer_rewards:
			enforcer_action_probabilities = retrieve(PATH, enforcer_reward, "dumb")
			likelihood[enforcer_reward] = enforcer_action_probabilities[tuple(enforcer_action)]
	else:
		for enforcer_reward in enforcer_rewards:
			enforcer_action_probabilities = enforcer(enforcer_reward, rationality)
			likelihood[enforcer_reward] = enforcer_action_probabilities[tuple(enforcer_action)]

	# Normalize the likelihood to generate the posterior.
	likelihood = likelihood.flatten()
	if sum(likelihood) == 0:
		posterior = likelihood.reshape(space)
	else:
		posterior = (likelihood/sum(likelihood)).reshape(space)

	# Plot the posterior.
	if plot == True:
		plt.figure(2)
		plt.title("Rationality = " + str(rationality))
		plt.ylabel("Enforcer Rewards for Action 0")
		plt.xlabel("Enforcer Rewards for Action 1")
		plt.pcolor(posterior)

	# Compute the utilities.
	smart_agent_reward = agent_reward + cooperative_reward(enforcer_rewards, posterior, cooperation, "flat")
	smart_agent_cost = agent_cost + enforcer_action
	U = smart_agent_reward - smart_agent_cost

	# Softmax the utilities to get action probabilities.
	action_probabilities = softmax(U, rationality)

	return action_probabilities

def enforcer(enforcer_reward, rationality, cooperation=None, smart=False, cache=False, plot=False):
	# Set up the utility space.
	space = tuple([MAX_VALUE for action in np.arange(NUM_ACTIONS)])
	U = np.zeros(space)

	# Generate possible agent rewards and enforcer actions. Use random sampling
	# if the problem space is bigger than MAX_SAMPLES.
	size = min(np.prod(space), MAX_SAMPLES)
	if size > MAX_SAMPLES:
		agent_rewards = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS))
		enforcer_actions = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS))
	else:
		agent_rewards = list(itertools.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS))
		enforcer_actions = list(itertools.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS))
	agent_cost = np.zeros(NUM_ACTIONS)

	# Compute the utilities.
	temp = np.zeros(space)
	for agent_reward in agent_rewards:
		for enforcer_action in enforcer_actions:
			if smart == True:
				agent_action_probabilities = smart_agent(agent_reward, agent_cost, enforcer_action, rationality, cooperation, cache=cache)
			elif smart == False:
				updated_agent_cost = agent_cost + enforcer_action
				agent_action_probabilities = dumb_agent(agent_reward, updated_agent_cost, rationality)
			expected_enforcer_reward = np.dot(enforcer_reward, agent_action_probabilities)
			U[enforcer_action] = expected_enforcer_reward - (COST_RATIO*sum(enforcer_action))
		temp = temp + U
	U = temp / size

	# Softmax the utilities to get action probabilities.
	action_probabilities = softmax(U.flatten(), rationality).reshape(space)

	# Plot the action probabilities.
	if plot == True:
		plt.figure(1 if smart == False else 3)
		plt.title("Rationality = " + str(rationality))
		plt.ylabel("Agent Cost (Enforcer Action) for Action 0")
		plt.xlabel("Agent Cost (Enforcer Action) for Action 1")
		plt.pcolor(action_probabilities)

	return action_probabilities

def argmax(action_probabilities):
	space = action_probabilities.shape
	arg = np.argmax(action_probabilities.flatten())

	row = 0
	col = arg
	while col > 0:
		col -= space[0]
		row += 1

	return (row, col)

def main():
	agent_reward = np.array((5, 0))
	agent_cost = np.array((0, 0))
	enforcer_reward = np.array((0, 5))
	enforcer_action = np.array((8, 8))

	rationality = 1
	cooperation = 100
	
	plot = int(sys.argv[1])
	cache = int(sys.argv[2])
	batch_size = int(sys.argv[3])

	if cache == True:
		enforcer_rewards = list(itertools.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS))
		# cache_dumb_enforcer(PATH, enforcer, enforcer_rewards, rationality)
		batch_rewards = enforcer_rewards[batch_size:(batch_size+9)]
		cache_smart_enforcer(PATH, enforcer, batch_rewards, rationality, cooperation)

	start_time = time.time()
	
	# print(enforcer(enforcer_reward, rationality, plot=plot))
	# print(smart_agent(agent_reward, agent_cost, enforcer_action, rationality, cooperation, cache=True, plot=plot))
	# print(enforcer(enforcer_reward, rationality, cooperation=cooperation, smart=True, cache=True, plot=plot))

	# action_cost = []
	# cooperation_set = [0.5, 1.0, 2.0, 5.0, 10.0, 50.0]
	# with open(PATH + "temp.csv", "w", newline="") as file:
	# 	for cooperation in cooperation_set:
	# 		action_probabilities = enforcer(enforcer_reward, rationality, cooperation=cooperation, smart=True, cache=True, plot=plot)
	# 		writer = csv.writer(file)
	# 		writer.writerows(action_probabilities)
	# 		optimal_enforcer_action = argmax(action_probabilities)
	# 		action_cost.append(sum(optimal_enforcer_action))
	# 		print("Done with " + str(cooperation), sep="")

	with open(PATH + "temp.csv", "r") as file:
		reader = csv.reader(file)
		action_probabilities = []
		for row in reader:
			action_probabilities.append(row)
	
	plt.figure(4)
	plt.plot(action_cost, cooperation_set)
	plt.show()

	end_time = time.time()
	print("Run time = ", end_time-start_time, " seconds!", sep="")

	if plot == True:
		plt.show()

if __name__ == "__main__":
	main()

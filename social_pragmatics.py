import numpy as np
import matplotlib.pyplot as plt
import itertools
import time
import sys
import csv

from util import softmax
from util import cooperative_reward
from util import cache_dumb_enforcer
from util import cache_smart_agent
from util import access_dumb_enforcer
from util import access_smart_agent

MAX_VALUE = 10
NUM_ACTIONS = 2
MAX_SAMPLES = 100
COST_RATIO = 1

def dumb_agent(agent_reward, agent_cost, rationality):
	U = agent_reward - agent_cost
	action_probabilities = softmax(U, rationality)

	return action_probabilities

def smart_agent(agent_reward, agent_cost, enforcer_action, rationality, cooperation, method, cache=False, plot=False):
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
			enforcer_action_probabilities = access_dumb_enforcer(enforcer_reward)
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
	smart_agent_reward = agent_reward + cooperative_reward(enforcer_rewards, posterior, cooperation, method)
	smart_agent_cost = agent_cost + enforcer_action
	U = smart_agent_reward - smart_agent_cost

	# Softmax the utilities to get action probabilities.
	action_probabilities = softmax(U, rationality)

	return action_probabilities

def enforcer(enforcer_reward, rationality, cooperation=None, method=None, smart=False, cache=False, plot=False):
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
				if cache == True:
					agent_action_probabilities = access_smart_agent(agent_reward, enforcer_action, cooperation, method)
				else:
					agent_action_probabilities = smart_agent(agent_reward, agent_cost, enforcer_action, rationality, \
															 cooperation, method, cache=True)
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

def observer(model, observations, enforcer_reward=None, enforcer_action=None, cooperation=None, rationality=None):
	# Variables:
	# Enforcer's beliefs (distributional assumptions) about agent rewards 
	# Possibly not needed: enforcer beliefs of smart vs. dumb agent
	# Cooperation
	# Enforcer rewards
	# Enforcer action

	# Set up the likelihood space.
	space = tuple([MAX_VALUE for action in np.arange(NUM_ACTIONS)])
	likelihood = np.zeros(space)

	# Generate possible agent rewards and enforcer actions. Use random sampling
	# if the problem space is bigger than MAX_SAMPLES.
	size = min(np.prod(space), MAX_SAMPLES)
	if size > MAX_SAMPLES:
		enforcer_rewards = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS))
	else:
		enforcer_rewards = list(itertools.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS))
	cooperation_set = [-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 5.0]

	methods = ["confidence", "flat", "proportional"]
	for method in methods:
		for cooperation in cooperation_set:
			for enforcer_reward in enforcer_rewards:
				enforcer_action_probabilities = model(enforcer_reward, rationality, cooperation=cooperation, method=method, \
													  smart=True, cache=True)
				likelihood[enforcer_reward] = enforcer_action_probabilities[tuple(enforcer_action)]

	# Sample cooperation values and pick the one that maximizes the likelihood.
	cooperation = [1.0, 5.0]
	temp = np.zeros(len(cooperation))
	method = "flat"
	for c in range(len(cooperation)):
		cache_smart_enforcer(enforcer, [enforcer_reward], rationality, cooperation[c], method)
		# enforcer_action_probabilities = enforcer(enforcer_reward, rationality, cooperation=cooperation[c], method=method, smart=True, cache=True)
		# temp[c] = enforcer_action_probabilities[tuple(enforcer_action)]

	cooperation_set = [-1.5, -1.0, -0.5, 0, 0.5, 1.5, 2.0, 10.0][::-1]
	for cooperation in cooperation_set:
		cache_smart_enforcer(enforcer, enforcer_rewards, rationality, cooperation, method)
	# enforcer_rewards
	# loop through cooperation parameters
	# run cache function
	# compute maximum enforcer reward/cooperation parameter pair that maximizes likelihood of enforcer action

	return
	# assigning meaning to objects
	# "starting with Baker 2009..."
	# need 1) theory of mind 2) intuitive physics (for understanding costs) 3) cooperation (or not)


	# with open("proportional.csv", "r") as file:
	# 	reader = csv.reader(file)
	# 	cooperation_set = [-2.0, -1.0, -0.5, 0, 0.5, 1.0, 2.0, 5.0, 10.0, 50.0][::-1]
	# 	action_probabilities = []
	# 	total = []
	# 	counter = 0
	# 	for row in reader:
	# 		action_probabilities.append([float(num) for num in row])
	# 		counter += 1
	# 		if (counter % 10) == 0:
	# 			action_probabilities = np.array(action_probabilities)
	# 			# plt.figure()
	# 			# plt.title("Cooperation = " + str(cooperation_set.pop()))
	# 			# plt.pcolor(action_probabilities)

	# 			print(np.unravel_index(action_probabilities.argmax(), action_probabilities.shape))
	# 			action_probabilities = []

	return temp

def main():
	agent_reward = np.array((5, 0))
	agent_cost = np.array((0, 0))
	enforcer_reward = np.array((0, 9))
	enforcer_action = np.array((0, 3))

	rationality = 1
	cooperation = 1.0
	method = "flat"

	start_time = time.time()
	observer(enforcer, agent_reward, rationality, cooperation=cooperation, method=method, smart=True, cache=True)	
	print(time.time()-start_time)
	return

	agent_rewards = list(itertools.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS))
	enforcer_actions = list(itertools.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS))
	
	complete_parameters = [-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 5.0]
	parameters_to_test = [10.0, 50.0]
	start_time = time.time()
	cache_smart_agent(smart_agent, agent_rewards, agent_cost, enforcer_actions, rationality, [1.5])
	print(time.time()-start_time)
	return

if __name__ == "__main__":
	main()

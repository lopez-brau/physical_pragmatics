import numpy as np
import matplotlib.pyplot as plt
import itertools
import time
import sys
import csv

from util import *

def no_ToM_agent(agent_reward, agent_cost, rationality):
	U = agent_reward - agent_cost
	action_probabilities = softmax(U, rationality)

	return action_probabilities

def ToM_agent(agent_reward, agent_cost, enforcer_action, rationality, cooperation, method, cache=False, plot=False):
	# Set up the likelihood space.
	space = tuple([MAX_VALUE for action in np.arange(NUM_ACTIONS)])
	likelihood = np.zeros(space)
	
	# Generate possible enforcer rewards. Use random sampling if problem space
	# is bigger than MAX_SAMPLES.
	size = min(np.prod(space), MAX_SAMPLES)
	if size > MAX_SAMPLES or SAMPLING == True:
		enforcer_rewards = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS))
	else:
		enforcer_rewards = list(itertools.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS))

	# Compute the likelihood.
	if cache == True:
		total_enforcer_action_probabilities = access_no_ToM_enforcer(enforcer_rewards)
		likelihood = total_enforcer_action_probabilities.T[enforcer_action[1]][enforcer_action[0]:total_enforcer_action_probabilities.shape[0]:10]
		likelihood = likelihood.reshape(space)
		return
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
		plt.title("ToM Agent with Rationality = " + str(rationality))
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
	if size > MAX_SAMPLES or SAMPLING == True:
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
					agent_action_probabilities = access_ToM_agent(agent_reward, enforcer_action, cooperation, method)
				else:
					agent_action_probabilities = ToM_agent(agent_reward, agent_cost, enforcer_action, rationality, \
															 cooperation, method, cache=True)
			elif smart == False:
				updated_agent_cost = agent_cost + enforcer_action
				agent_action_probabilities = no_ToM_agent(agent_reward, updated_agent_cost, rationality)
			expected_enforcer_reward = np.dot(enforcer_reward, agent_action_probabilities)
			U[enforcer_action] = expected_enforcer_reward - (COST_RATIO*sum(enforcer_action))
		temp = temp + U
	U = temp / size

	# Softmax the utilities to get action probabilities.
	action_probabilities = softmax(U.flatten(), rationality).reshape(space)

	# Plot the action probabilities.
	if plot == True:
		plt.figure(1 if smart == False else 3)
		plt.title("Enforcing Agent with Rationality = " + str(rationality))
		plt.ylabel("Agent Cost (Enforcer Action) for Action 0")
		plt.xlabel("Agent Cost (Enforcer Action) for Action 1")
		plt.pcolor(action_probabilities)

	return action_probabilities

# Variables:
# Enforcer's beliefs (distributional assumptions) about agent rewards 
# Possibly not needed: enforcer beliefs of smart vs. dumb agent
# Cooperation
# Enforcer rewards
# Enforcer action

# assigning meaning to objects
# "starting with Baker 2009..."
# need 1) theory of mind 2) intuitive physics (for understanding costs) 3) cooperation (or not)
# develop a "one-slider" to my project; like the hat on the chair example
# loss aversion is not part of our mental models; loss aversion paper was counterintuitive!
# develop super simple plot or graphic that explains the problem to the core
def observer(unobserved, rationality, **kwargs):
	# Infer the enforcer's reward.
	if unobserved == "enforcer_reward":
		# Set up the likelihood space.
		space = tuple([MAX_VALUE for action in np.arange(NUM_ACTIONS)])
		likelihood = np.zeros(space)

		# Generate possible enforcer rewards. Use random sampling if the 
		# problem space is bigger than MAX_SAMPLES.
		size = min(np.prod(space), MAX_SAMPLES)
		if size > MAX_SAMPLES:
			enforcer_rewards = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS))
		else:
			enforcer_rewards = list(itertools.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS))
		
		# Compute the likelihood.
		for enforcer_reward in enforcer_rewards:
			enforcer_action_probabilities = enforcer(
				enforcer_reward, 
				rationality, 
				cooperation=kwargs["cooperation"], 
				method=kwargs["method"], 
				smart=True, 
				cache=True
			)
			likelihood[enforcer_reward] = enforcer_action_probabilities[tuple(kwargs["enforcer_action"])]

		# Normalize the likelihood to generate the posterior.
		likelihood = likelihood.flatten()
		if sum(likelihood) == 0:
			posterior = likelihood.reshape(space)
		else:
			posterior = (likelihood/sum(likelihood)).reshape(space)

	# Infer the enforcer's beliefs about the cooperativeness of agents.
	elif unobserved == "cooperation":
		# Set up the space of possible cooperation parameters and the
		# likelihood space.
		cooperation_set = np.array([-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 5.0])
		space = np.shape(cooperation_set)
		likelihood = np.zeros(space)

		for c in np.arange(cooperation_set.size):
			# start_time = time.time()
			print(c)
			enforcer_action_probabilities = enforcer(
				enforcer_reward=kwargs["enforcer_reward"],
				rationality=rationality,
				cooperation=cooperation_set[c],
				method=kwargs["method"],
				smart=True,
				cache=True
			)
			# print(time.time()-start_time)
			# plt.figure(c)
			# plt.title("Cooperation = " + str(cooperation_set[c]))
			# plt.pcolor(enforcer_action_probabilities)
			likelihood[c] = enforcer_action_probabilities[tuple(kwargs["enforcer_action"])]

			if sum(likelihood) == 0:
				posterior = likelihood.reshape(space)
			else:
				posterior = likelihood / sum(likelihood)
			

	return posterior

def main():
	agent_reward = np.array((5, 0))
	agent_cost = np.array((0, 0))
	enforcer_reward = np.array((4, 0))
	enforcer_action = np.array((3, 2))

	rationality = 1.0
	cooperation = 2.0
	method = "flat"
	
	start_time = time.time()
	# agent_rewards = list(itertools.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS))
	# enforcer_actions = list(itertools.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS))
	enforcer_rewards = list(itertools.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS))
	# cooperation_set = np.array([-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 5.0])
	# cache_ToM_agent(smart_agent, agent_rewards, agent_cost, enforcer_actions, rationality, cooperation_set)
	
	cache_no_ToM_enforcer(enforcer, enforcer_rewards, rationality) 

	# ToM_agent(agent_reward, agent_cost, enforcer_action, rationality, cooperation, method, cache=True)
	print(time.time()-start_time)
	return

	posterior = enforcer(enforcer_reward, rationality, plot=True)
	# smart_agent(agent_reward, agent_cost, enforcer_action, rationality, cooperation, method, cache=True, plot=True)
	# enforcer(enforcer_reward, rationality, cooperation=cooperation, method=method, smart=True, cache=True, plot=True)
	unobserved = "cooperation"
	posterior = observer(unobserved, rationality, enforcer_reward=enforcer_reward, enforcer_action=enforcer_action, 
						 cooperation=cooperation, method=method, smart=True)
	# print(posterior)
	# print(np.unravel_index(posterior.argmax(), posterior.shape))
	# print(time.time()-start_time)
	# plt.show()
	return
	# agent_rewards = list(itertools.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS))
	# enforcer_actions = list(itertools.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS))

	start_time = time.time()
	# cooperative_reward(enforcer_rewards, posterior, cooperation, "confidence")
	smart_agent(agent_reward, agent_cost, enforcer_action, rationality, cooperation, "confidence", cache=True)
	print(time.time()-start_time)

	start_time = time.time()
	# cooperative_reward(enforcer_rewards, posterior, cooperation, "flat")
	smart_agent(agent_reward, agent_cost, enforcer_action, rationality, cooperation, "flat", cache=True)
	print(time.time()-start_time)

	start_time = time.time()
	# cooperative_reward(enforcer_rewards, posterior, cooperation, "proportional")
	smart_agent(agent_reward, agent_cost, enforcer_action, rationality, cooperation, "proportional", cache=True)
	print(time.time()-start_time)

	return

if __name__ == "__main__":
	main()

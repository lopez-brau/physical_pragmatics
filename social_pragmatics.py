import csv
import itertools
import matplotlib.pyplot as plt
import numpy as np
import time

from utils import *

def agent_no_ToM(agent_reward, agent_cost, rationality):
	U = agent_reward - agent_cost
	action_probabilities = softmax(U, rationality)

	return action_probabilities

def agent_ToM(agent_reward, agent_cost, enforcer_action, rationality, cooperation, cache=False, plot=False):
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
		likelihood = retrieve_enforcer_no_ToM(enforcer_rewards, enforcer_action, likelihood)
	else:
		for enforcer_reward in enforcer_rewards:
			enforcer_action_probabilities = enforcer(enforcer_reward, rationality)
			likelihood[tuple(enforcer_reward)] = enforcer_action_probabilities[tuple(enforcer_action)]

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
	smart_agent_reward = agent_reward + cooperative_reward(enforcer_rewards, posterior, cooperation)
	smart_agent_cost = agent_cost + enforcer_action
	U = smart_agent_reward - smart_agent_cost

	# Softmax the utilities to get action probabilities.
	action_probabilities = softmax(U, rationality)

	return action_probabilities

def enforcer(enforcer_reward, rationality, p=0.0, cooperation=None, cache=False, plot=False, ar=None):
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
	
	# Compute the utilities. Cached option only supports p = 1.0.
	if cache == True:
		U = retrieve_agent_ToM(agent_rewards, enforcer_reward, enforcer_actions, cooperation, U)
	# Temporary? This runs the inference with agent reward fixed.
	elif type(ar) != type(None):
		U_no_ToM = np.zeros(space)
		U_ToM = np.zeros(space)
		agent_reward = ar
		for enforcer_action in enforcer_actions:
			# Reason about a ToM agent.
			if p != 0.0:
				agent_action_probabilities = agent_ToM(agent_reward, agent_cost, enforcer_action, rationality, \
													   cooperation, cache=True)
				expected_enforcer_reward = np.dot(enforcer_reward, agent_action_probabilities)
				U_ToM[tuple(enforcer_action)] = expected_enforcer_reward - (COST_RATIO*sum(enforcer_action))

			# Reason about a non-ToM agent.
			updated_agent_cost = agent_cost + enforcer_action
			agent_action_probabilities = agent_no_ToM(agent_reward, updated_agent_cost, rationality)
			expected_enforcer_reward = np.dot(enforcer_reward, agent_action_probabilities)
			U_no_ToM[tuple(enforcer_action)] = expected_enforcer_reward - (COST_RATIO*sum(enforcer_action))
		U = ((1.0-p)*U_no_ToM) + (p*U_ToM)
	else:
		U_no_ToM = np.zeros(space)
		U_ToM = np.zeros(space)
		temp_no_ToM = np.zeros(space)
		temp_ToM = np.zeros(space)
		for agent_reward in agent_rewards:
			for enforcer_action in enforcer_actions:
				# Reason about a ToM agent.
				if p != 0.0:
					agent_action_probabilities = agent_ToM(agent_reward, agent_cost, enforcer_action, rationality, \
														   cooperation, cache=True)
					expected_enforcer_reward = np.dot(enforcer_reward, agent_action_probabilities)
					temp_ToM[tuple(enforcer_action)] = expected_enforcer_reward - (COST_RATIO*sum(enforcer_action))

				# Reason about a non-ToM agent.
				updated_agent_cost = agent_cost + enforcer_action
				agent_action_probabilities = agent_no_ToM(agent_reward, updated_agent_cost, rationality)
				expected_enforcer_reward = np.dot(enforcer_reward, agent_action_probabilities)
				temp_no_ToM[tuple(enforcer_action)] = expected_enforcer_reward - (COST_RATIO*sum(enforcer_action))
			U_no_ToM = U_no_ToM + temp_no_ToM
			U_ToM = U_ToM + temp_ToM
		U_no_ToM = U_no_ToM / np.prod(space)
		U_ToM = U_ToM / np.prod(space)
		U = ((1.0-p)*U_no_ToM) + (p*U_ToM)

	# Softmax the utilities to get action probabilities.
	action_probabilities = softmax(U.flatten(), rationality).reshape(space)

	# Plot the action probabilities.
	if plot == True:
		# plt.figure(1 if smart == False else 3)
		plt.figure()
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
			enforcer_action_probabilities = enforcer(enforcer_reward, rationality, cooperation=kwargs["cooperation"], cache=True)
			likelihood[tuple(enforcer_reward)] = enforcer_action_probabilities[tuple(kwargs["enforcer_action"])]

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
			enforcer_action_probabilities = enforcer(enforcer_reward=kwargs["enforcer_reward"], rationality=rationality, \
													 p=kwargs["p"], cooperation=cooperation_set[c])
			likelihood[c] = enforcer_action_probabilities[tuple(kwargs["enforcer_action"])]

		if sum(likelihood) == 0:
			posterior = likelihood.reshape(space)
		else:
			posterior = likelihood / sum(likelihood)
		
	# Infer whether the enforcer was acting for an agent with or without ToM.
	elif unobserved == "p":
		# Set up the space of possible proportion parameters and the likelihood
		# space.
		p_set = np.linspace(0.0, 1.0, num=11)
		space = np.shape(p_set)
		likelihood = np.zeros(space)

		for p in np.arange(p_set.size):
			enforcer_action_probabilities = enforcer(enforcer_reward=kwargs["enforcer_reward"], rationality=rationality, \
													 p=p, cooperation=kwargs["cooperation"])
			likelihood[p] = enforcer_action_probabilities[tuple(kwargs["enforcer_action"])]

		if sum(likelihood) == 0:
			posterior = likelihood.reshape(space)
		else:
			posterior = likelihood / sum(likelihood)

	# Jointly infer what the enforcer's beliefs of the agent rewards and
	# whether the enforcer was acting for an agent with or without ToM.
	elif unobserved == "agent_rewards_and_p":
		# Set up the space of possible proportion parameters and the likelihood
		# space.
		p_set = np.linspace(0.0, 1.0, num=11)
		space = (100, p_set.size)
		likelihood = np.zeros(space)

		# Generate possible enforcer rewards. Use random sampling if the 
		# problem space is bigger than MAX_SAMPLES.
		size = min(np.prod(space), MAX_SAMPLES)
		if size > MAX_SAMPLES:
			agent_rewards = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS))
		else:
			agent_rewards = list(itertools.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS))

		# Compute the likelihood.
		for i in np.arange(len(agent_rewards)):
			for p in np.arange(p_set.size):
				enforcer_action_probabilities = enforcer(enforcer_reward=kwargs["enforcer_reward"], rationality=rationality, \
													 	 p=p, cooperation=kwargs["cooperation"], ar=agent_rewards[i])
				likelihood[i][p] = enforcer_action_probabilities[tuple(kwargs["enforcer_action"])]

		# Normalize the likelihood to generate the posterior.
		likelihood = likelihood.flatten()
		if sum(likelihood) == 0:
			posterior = likelihood.reshape(space)
		else:
			posterior = (likelihood/sum(likelihood)).reshape(space)

	elif unobserved == "enforcer_and_agent_rewards":
		# Set up the likelihood space.
		space = (100, 10, 10)
		likelihood = np.zeros(space)

		# Generate possible enforcer rewards. Use random sampling if the 
		# problem space is bigger than MAX_SAMPLES.
		size = min(np.prod(space), MAX_SAMPLES)
		if size > MAX_SAMPLES:
			agent_rewards = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS))
			enforcer_rewards = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS))
		else:
			agent_rewards = list(itertools.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS))
			enforcer_rewards = list(itertools.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS))
		
		# Compute the likelihood.
		for i in np.arange(len(agent_rewards)):
			for enforcer_reward in enforcer_rewards:
				enforcer_action_probabilities = enforcer(enforcer_reward, rationality, cooperation=kwargs["cooperation"], \
														 cache=True, ar=agent_rewards[i])
				likelihood[i][tuple(enforcer_reward)] = enforcer_action_probabilities[tuple(kwargs["enforcer_action"])]

		# Normalize the likelihood to generate the posterior.
		likelihood = likelihood.flatten()
		if sum(likelihood) == 0:
			posterior = likelihood.reshape(space)
		else:
			posterior = (likelihood/sum(likelihood)).reshape(space)

	# Plot the action probabilities.
	if kwargs["plot"] == True:
		plt.figure()
		plt.title("Observer with Rationality = " + str(rationality))
		plt.ylabel("Agent Cost (Enforcer Action) for Action 0")
		plt.xlabel("Agent Cost (Enforcer Action) for Action 1")
		plt.pcolor(posterior)

	return posterior

def main():
	agent_reward = np.array((0, 9))
	# agent_cost = np.array((0, 0))
	enforcer_reward = np.array((0, 9))
	enforcer_action = np.array((2, 0))

	rationality = 1.0
	cooperation = 2.0
	p = 1.0

	# x1 = enforcer(enforcer_reward, rationality, plot=True))
	# x2 = enforcer(enforcer_reward, rationality, cooperation=cooperation, cache=True, plot=True)
	# x3 = enforcer(enforcer_reward, rationality, p=1.0, cooperation=cooperation, cache=False, plot=True, ar=agent_reward)
	start_time = time.time()
	x4 = observer("agent_rewards_and_p", rationality, enforcer_reward=enforcer_reward, enforcer_action=enforcer_action, p=p,
				  cooperation=cooperation, plot=False)
	print(time.time()-start_time)
	print(x4)
	with open("temp.txt", "w", newline="") as file:
		writer = csv.writer(file)
		writer.writerows(x4)
	plt.show()	
	return

if __name__ == "__main__":
	main()

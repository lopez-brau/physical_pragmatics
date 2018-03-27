from utils import *

import itertools as it
import matplotlib.pyplot as plt
import numpy as np

def agent_no_ToM(rationality, agent_reward, enforcer_action):
	# Compute the utilities.
	agent_cost = convert_cost(enforcer_action) if GRIDWORLD == True else NATURAL_COST + enforcer_action
	U = agent_reward - agent_cost

	# Compute the action probabilities.
	action_probabilities = softmax(U, rationality)

	return action_probabilities

def agent_ToM(rationality, agent_reward, enforcer_action, cooperation, cache=False, plot=False):
	# Set up the likelihood space.
	space = tuple([MAX_VALUE for action in np.arange(NUM_ACTIONS)])
	likelihood = np.zeros(space)
	
	# Generate possible enforcer rewards.
	if SAMPLING == True:
		enforcer_rewards = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS))
	else:
		enforcer_rewards = np.array(list(it.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS)))

	# Compute the likelihood.
	if cache == True:
		likelihood = retrieve_enforcer_no_ToM(rationality, enforcer_rewards, enforcer_action, likelihood)
	else:
		for enforcer_reward in enforcer_rewards:
			enforcer_action_probabilities = enforcer(rationality, enforcer_reward, cache=True)
			likelihood[tuple(enforcer_reward)] = enforcer_action_probabilities[tuple(enforcer_action)]

	# Normalize the likelihood to generate the posterior.
	likelihood = likelihood.flatten()
	if sum(likelihood) == 0:
		posterior = likelihood.reshape(space)
	else:
		posterior = (likelihood/sum(likelihood)).reshape(space)

	# Plot the posterior.
	if plot == True:
		plt.figure()
		plt.title("ToM Agent with Rationality = " + str(rationality))
		plt.ylabel("Enforcer Rewards for Action 0")
		plt.xlabel("Enforcer Rewards for Action 1")
		plt.pcolor(posterior)

	# Compute the utilities.
	smart_agent_reward = agent_reward + cooperative_reward(enforcer_rewards, posterior, cooperation)
	smart_agent_cost = convert_cost(enforcer_action) if GRIDWORLD == True else NATURAL_COST + enforcer_action
	U = smart_agent_reward - smart_agent_cost

	# Compute the action probabilities.
	action_probabilities = softmax(U, rationality)

	return action_probabilities

def enforcer(rationality, enforcer_reward, p=0.0, cooperation=None, reward_assumptions=[], cache=False, plot=False):
	# Set up the utility space.
	space = tuple([MAX_VALUE for action in np.arange(NUM_ACTIONS)]) if GRIDWORLD != True else \
			tuple([GRIDWORLD_MAX_ACTION for action in np.arange(NUM_ACTIONS)])
	U = np.zeros(space)
	
	# Generate possible agent rewards and enforcer actions, taking into account
	# any potential assumptions the enforcer may have about agent rewards.
	if SAMPLING == True:
		agent_rewards = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS))
		enforcer_actions = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS)) if GRIDWORLD != True else \
						   np.random.choice(GRIDWORLD_MAX_ACTION, (GRIDWORLD_MAX_SAMPLES, NUM_ACTIONS))
	else:
		if len(reward_assumptions) == 0:
			agent_rewards = np.array(list(it.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS)))
		elif np.size(reward_assumptions) == NUM_ACTIONS:
			agent_rewards = np.array([reward_assumptions])
		else:
			agent_rewards = np.array(reward_assumptions)
		enforcer_actions = np.array(list(it.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS))) if GRIDWORLD != True else \
						   np.array(list(it.product(np.arange(GRIDWORLD_MAX_ACTION), repeat=NUM_ACTIONS)))

	# Compute the utilities.
	if cache == True:
		U = retrieve_agent(rationality, enforcer_reward, agent_rewards, enforcer_actions, p, cooperation, U)
	else:
		U_agent_no_ToM = np.zeros(space)
		U_agent_ToM = np.zeros(space)
		temp_agent_no_ToM = np.zeros(space)
		temp_agent_ToM = np.zeros(space)
		for agent_reward in agent_rewards:
			for enforcer_action in enforcer_actions:
				# Reason about a non-ToM agent.
				if p != 1.0:
					agent_action_probabilities = agent_no_ToM(rationality, agent_reward, enforcer_action)
					expected_enforcer_reward = np.dot(enforcer_reward, agent_action_probabilities)
					temp_agent_no_ToM[tuple(enforcer_action)] = expected_enforcer_reward - (COST_RATIO*sum(enforcer_action))

				# Reason about a ToM agent.
				if p != 0.0:
					agent_action_probabilities = agent_ToM(rationality, agent_reward, enforcer_action, cooperation, cache=True)
					expected_enforcer_reward = np.dot(enforcer_reward, agent_action_probabilities)
					temp_agent_ToM[tuple(enforcer_action)] = expected_enforcer_reward - (COST_RATIO*sum(enforcer_action))

			U_agent_no_ToM = U_agent_no_ToM + temp_agent_no_ToM
			U_agent_ToM = U_agent_ToM + temp_agent_ToM
		U_agent_no_ToM = U_agent_no_ToM / len(agent_rewards)
		U_agent_ToM = U_agent_ToM / len(agent_rewards)
		U = ((1.0-p)*U_agent_no_ToM) + (p*U_agent_ToM)

	# Compute the action probabilities.
	action_probabilities = softmax(U.flatten(), rationality).reshape(space)

	# Plot the action probabilities.
	if plot == True:
		plt.figure()
		plt.title("Enforcing Agent with Rationality = " + str(rationality))
		plt.ylabel("Agent Cost (Enforcer Action) for Action 0")
		plt.xlabel("Agent Cost (Enforcer Action) for Action 1")
		plt.pcolor(action_probabilities)

	return action_probabilities

def observer(infer, rationality, **kwargs):
	# Infer the enforcer's reward.
	if infer == "enforcer_reward":
		# Extract variables.
		cooperation = kwargs["cooperation"]
		p = kwargs["p"]
		enforcer_action = kwargs["enforcer_action"]
		plot = kwargs["plot"]

		# Set up the likelihood space.
		space = tuple([MAX_VALUE for action in np.arange(NUM_ACTIONS)])
		likelihood = np.zeros(space)

		# Generate possible enforcer rewards.
		if SAMPLING == True:
			enforcer_rewards = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS))
		else:
			enforcer_rewards = np.array(list(it.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS)))
		
		# Compute the likelihood.
		for enforcer_reward in enforcer_rewards:
			enforcer_action_probabilities = enforcer(rationality, enforcer_reward, p=p, cooperation=cooperation, cache=True)
			likelihood[tuple(enforcer_reward)] = enforcer_action_probabilities[tuple(enforcer_action)]

		# Normalize the likelihood to generate the posterior.
		likelihood = likelihood.flatten()
		if sum(likelihood) == 0:
			posterior = likelihood.reshape(space)
		else:
			posterior = (likelihood/sum(likelihood)).reshape(space)

		# Plot the posterior.
		if plot == True:
			plt.figure()
			plt.title("Observer with Rationality = " + str(rationality))
			plt.ylabel("Enforcer Rewards for Action 0")
			plt.xlabel("Enforcer Rewards for Action 1")
			plt.pcolor(posterior)

	# Infer the enforcer's beliefs about the cooperativeness of agents.
	elif infer == "cooperation":
		# Extract variables.
		enforcer_reward = kwargs["enforcer_reward"]
		p = kwargs["p"]
		cooperation_set = kwargs["cooperation_set"]
		enforcer_action = kwargs["enforcer_action"]
		plot = kwargs["plot"]

		# Set up the space of possible cooperation parameters and the
		# likelihood space.
		cooperation_set = np.array([-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 5.0])
		space = np.shape(cooperation_set)
		likelihood = np.zeros(space)

		# Compute the likelihood.
		for c in np.arange(cooperation_set.size):
			enforcer_action_probabilities = enforcer(rationality, enforcer_reward, p=p, cooperation=cooperation_set[c], cache=True)
			likelihood[c] = enforcer_action_probabilities[tuple(enforcer_action)]

		# Normalize the likelihood to generate the posterior.
		if sum(likelihood) == 0:
			posterior = likelihood
		else:
			posterior = likelihood / sum(likelihood)
		
		# Print the posterior.
		if plot == True:
			print(posterior)

	# Infer the degree of ToM that the enforcer was acting for.
	elif infer == "p":
		# Extract variables.
		enforcer_reward = kwargs["enforcer_reward"]
		cooperation = kwargs["cooperation"]
		enforcer_action = kwargs["enforcer_action"]
		plot = kwargs["plot"]

		# Set up the space of possible proportion parameters and the likelihood
		# space.
		p_set = np.linspace(0.0, 1.0, num=11)
		space = np.shape(p_set)
		likelihood = np.zeros(space)

		# Compute the likelihood.
		for p in np.arange(p_set.size):
			enforcer_action_probabilities = enforcer(rationality, enforcer_reward, p=p_set[p], cooperation=cooperation, cache=True)
			likelihood[p] = enforcer_action_probabilities[tuple(enforcer_action)]

		# Normalize the likelihood to generate the posterior.
		if sum(likelihood) == 0:
			posterior = likelihood
		else:
			posterior = likelihood / sum(likelihood)

		# Print the posterior.
		if plot == True:
			print(posterior)

	# Jointly infer what the enforcer's beliefs of the agent rewards and
	# the degree of ToM that the enforcer was acting for.
	elif infer == "agent_reward_and_p":
		# Extract variables.
		enforcer_reward = kwargs["enforcer_reward"]
		cooperation = kwargs["cooperation"]
		enforcer_action = kwargs["enforcer_action"]
		
		# Set up the space of possible proportion parameters and the likelihood
		# space.
		p_set = np.linspace(0.0, 1.0, num=11)
		space = (MAX_VALUE**2, p_set.size)
		likelihood = np.zeros(space)

		# Generate possible enforcer rewards.
		if SAMPLING == True:
			agent_rewards = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS))
		else:
			agent_rewards = np.array(list(it.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS)))

		# Compute the likelihood.
		for ar in np.arange(len(agent_rewards)):
			for p in np.arange(p_set.size):
				enforcer_action_probabilities = enforcer(rationality, enforcer_reward, p=p_set[p], cooperation=cooperation, \
														 reward_assumptions=agent_rewards[ar], cache=True)
				likelihood[ar][p] = enforcer_action_probabilities[tuple(enforcer_action)]

		# Normalize the likelihood to generate the posterior.
		likelihood = likelihood.flatten()
		if sum(likelihood) == 0:
			posterior = likelihood.reshape(space)
		else:
			posterior = (likelihood/sum(likelihood)).reshape(space)

	return posterior

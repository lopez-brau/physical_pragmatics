import itertools as it
import matplotlib.pyplot as plt
import numpy as np

from utils import *

def actor_no_ToM(rationality, actor_reward, enforcer_action):
	# Compute the utilities.
	actor_cost = NATURAL_COST + [COST_TABLE[action] for action in enforcer_action] if GRIDWORLD == True else \
				 NATURAL_COST + enforcer_action
	U = actor_reward - actor_cost

	# Compute the action probabilities.
	action_probabilities = softmax(U, rationality)

	return action_probabilities

def actor_ToM(rationality, actor_reward, enforcer_action, method, cooperation, cache=False, plot=False):
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
		likelihood = process_enforcer_no_ToM(rationality, enforcer_rewards, enforcer_action, likelihood)
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
		plt.title("ToM Actor with Rationality = " + str(rationality))
		plt.ylabel("Enforcer Rewards for Action 0")
		plt.xlabel("Enforcer Rewards for Action 1")
		plt.pcolor(posterior)
	
	# Compute the utilities.
	actor_ToM_reward = actor_reward + cooperative_reward(enforcer_rewards, posterior, method, cooperation)
	actor_ToM_cost = NATURAL_COST + [COST_TABLE[action] for action in enforcer_action] if GRIDWORLD == True else \
					 NATURAL_COST + enforcer_action
	U = actor_ToM_reward - actor_ToM_cost

	# Compute the action probabilities.
	action_probabilities = softmax(U, rationality)

	return action_probabilities

def enforcer(rationality, enforcer_reward, p=0.0, method=None, cooperation=None, reward_assumptions=[], cache=False, plot=False):
	# Set up the utility space.
	space = tuple([MAX_VALUE for action in np.arange(NUM_ACTIONS)]) if GRIDWORLD != True else \
			tuple([GRIDWORLD_MAX_VALUE for action in np.arange(NUM_ACTIONS)])
	U = np.zeros(space)
	
	# Generate possible actor rewards and enforcer actions, taking into account
	# any potential assumptions the enforcer may have about actor rewards.
	if SAMPLING == True:
		actor_rewards = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS))
		enforcer_actions = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS)) if GRIDWORLD != True else \
						   np.random.choice(GRIDWORLD_MAX_VALUE, (GRIDWORLD_MAX_SAMPLES, NUM_ACTIONS))
	else:
		if len(reward_assumptions) == 0:
			actor_rewards = np.array(list(it.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS)))
		elif np.size(reward_assumptions) == NUM_ACTIONS:
			actor_rewards = np.array([reward_assumptions])
		else:
			actor_rewards = np.array(reward_assumptions)
		enforcer_actions = np.array(list(it.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS))) if GRIDWORLD != True else \
						   np.array(list(it.product(np.arange(GRIDWORLD_MAX_VALUE), repeat=NUM_ACTIONS)))
	
	# Compute the utilities.
	if cache == True:
		U = process_actor(rationality, enforcer_reward, actor_rewards, enforcer_actions, p, method, cooperation, U)
	else:
		U_actor_no_ToM = np.zeros(space)
		U_actor_ToM = np.zeros(space)
		temp_actor_no_ToM = np.zeros(space)
		temp_actor_ToM = np.zeros(space)
		for actor_reward in actor_rewards:
			for enforcer_action in enforcer_actions:
				# Reason about a non-ToM actor.
				if p != 1.0:
					actor_action_probabilities = actor_no_ToM(rationality, actor_reward, enforcer_action)
					expected_enforcer_reward = np.dot(enforcer_reward, actor_action_probabilities)
					temp_actor_no_ToM[tuple(enforcer_action)] = expected_enforcer_reward - (COST_RATIO*sum(enforcer_action))

				# Reason about a ToM actor.
				if p != 0.0:
					actor_action_probabilities = actor_ToM(rationality, actor_reward, enforcer_action, method, cooperation, \
														   cache=True)
					expected_enforcer_reward = np.dot(enforcer_reward, actor_action_probabilities)
					temp_actor_ToM[tuple(enforcer_action)] = expected_enforcer_reward - (COST_RATIO*sum(enforcer_action))
			U_actor_no_ToM = U_actor_no_ToM + temp_actor_no_ToM
			U_actor_ToM = U_actor_ToM + temp_actor_ToM
		U_actor_no_ToM = U_actor_no_ToM / len(actor_rewards)
		U_actor_ToM = U_actor_ToM / len(actor_rewards)
		U = ((1.0-p)*U_actor_no_ToM) + (p*U_actor_ToM)

	# Compute the action probabilities.
	action_probabilities = softmax(U.flatten(), rationality).reshape(space)

	# Plot the action probabilities.
	if plot == True:
		plt.figure()
		plt.title("Enforcer with Rationality = " + str(rationality))
		plt.ylabel("Actor Cost (Enforcer Action) for Action 0")
		plt.xlabel("Actor Cost (Enforcer Action) for Action 1")
		plt.pcolor(action_probabilities)

	return action_probabilities

def observer(infer, rationality, **kwargs):
	# Infer the enforcer's reward.
	if infer == "enforcer_reward":
		# Extract variables.
		p = kwargs["p"]
		method = kwargs["method"]
		cooperation = kwargs["cooperation"]
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
			enforcer_action_probabilities = enforcer(rationality, enforcer_reward, p=p, method=method, cooperation=cooperation, \
													 cache=True)
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

	# Infer the enforcer's beliefs about the cooperativeness of actors.
	elif infer == "cooperation":
		# Extract variables.
		enforcer_reward = kwargs["enforcer_reward"]
		p = kwargs["p"]
		method = kwargs["method"]
		enforcer_action = kwargs["enforcer_action"]
		plot = kwargs["plot"]

		# Set up the space of possible cooperation parameters and the
		# likelihood space.
		cooperation_set = np.array([-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 5.0])
		space = np.shape(cooperation_set)
		likelihood = np.zeros(space)

		# Compute the likelihood.
		for c in np.arange(cooperation_set.size):
			enforcer_action_probabilities = enforcer(rationality, enforcer_reward, p=p, method=method, \
													 cooperation=cooperation_set[c], cache=True)
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
		method = kwargs["method"]
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
			enforcer_action_probabilities = enforcer(rationality, enforcer_reward, p=p_set[p], method=method, \
													 cooperation=cooperation, cache=True)
			likelihood[p] = enforcer_action_probabilities[tuple(enforcer_action)]

		# Normalize the likelihood to generate the posterior.
		if sum(likelihood) == 0:
			posterior = likelihood
		else:
			posterior = likelihood / sum(likelihood)

		# Print the posterior.
		if plot == True:
			print(posterior)

	# Jointly infer what the enforcer's beliefs of the actor rewards and
	# the degree of ToM that the enforcer was acting for.
	elif infer == "actor_reward_and_p":
		# Extract variables.
		enforcer_reward = kwargs["enforcer_reward"]
		method = kwargs["method"]
		cooperation = kwargs["cooperation"]
		enforcer_action = kwargs["enforcer_action"]
		
		# Set up the space of possible proportion parameters and the likelihood
		# space.
		p_set = np.linspace(0.0, 1.0, num=11)
		space = (MAX_VALUE**2, p_set.size)
		likelihood = np.zeros(space)

		# Generate possible actor rewards.
		if SAMPLING == True:
			actor_rewards = np.random.choice(MAX_VALUE, (MAX_SAMPLES, NUM_ACTIONS))
		else:
			actor_rewards = np.array(list(it.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS)))

		# Compute the likelihood.
		for ar in np.arange(len(actor_rewards)):
			for p in np.arange(p_set.size):
				enforcer_action_probabilities = enforcer(rationality, enforcer_reward, p=p_set[p], method=method, \
														 cooperation=cooperation, reward_assumptions=actor_rewards[ar], cache=True)
				likelihood[ar][p] = enforcer_action_probabilities[tuple(enforcer_action)]

		# Normalize the likelihood to generate the posterior.
		likelihood = likelihood.flatten()
		if sum(likelihood) == 0:
			posterior = likelihood.reshape(space)
		else:
			posterior = (likelihood/sum(likelihood)).reshape(space)

	return posterior

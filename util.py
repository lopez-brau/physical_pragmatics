import numpy as np
import csv

def softmax(U, rationality):
	# Subtracting away the max prevents overflow.
	U = U - np.max(U)
	exp = np.exp(U/rationality)

	return exp / sum(exp)

def cooperative_reward(enforcer_rewards, reward_probabilities, cooperation, method):
	num_actions = len(np.shape(reward_probabilities))
	inferred_enforcer_action = np.zeros(num_actions)

	# The "confidence" method computes the probabilities of each enforcer 
	# action being the optimal one.
	if method == "confidence":
		for enforcer_reward in enforcer_rewards:
			optimal_enforcer_action = (max(enforcer_reward) == np.array(enforcer_reward)) + 0.0
			inferred_enforcer_action = inferred_enforcer_action + (reward_probabilities[enforcer_reward]*optimal_enforcer_action)

	# The "flat" method computes the expected enforcer rewards and infers that
	# the max of those rewards is the optimal enforcer action.
	elif method == "flat":
		expected_enforcer_rewards = np.zeros(num_actions)
		for enforcer_reward in enforcer_rewards:
			expected_enforcer_rewards = expected_enforcer_rewards + (reward_probabilities[enforcer_reward]*np.array(enforcer_reward))
		inferred_enforcer_action = (max(expected_enforcer_rewards) == expected_enforcer_rewards) + 0.0

	# The "proportional" method computes the expected enforcer rewards.
	elif method == "proportional":
		expected_enforcer_rewards = np.zeros(num_actions)
		for enforcer_reward in enforcer_rewards:
			expected_enforcer_rewards = expected_enforcer_rewards + (reward_probabilities[enforcer_reward]*np.array(enforcer_reward))
		inferred_enforcer_action = expected_enforcer_rewards

	# Throw an error if there's a typo in the method type.
	else:
		print("Invalid method.")
		return

	return cooperation*inferred_enforcer_action

def cache_dumb_enforcer(path, enforcer, enforcer_rewards, rationality): 
	for enforcer_reward in enforcer_rewards:
		action_probabilities = enforcer(enforcer_reward, rationality)
		filename = path + "cache/dumb/" + ''.join([str(action_reward) for action_reward in enforcer_reward]) + ".csv"
		with open(filename, "w", newline="") as file:
			writer = csv.writer(file)
			writer.writerows(action_probabilities)

def cache_smart_enforcer(path, enforcer, enforcer_rewards, rationality, cooperation):
	for enforcer_reward in enforcer_rewards:
		action_probabilities = enforcer(enforcer_reward, rationality, cooperation=cooperation, smart=True, cache=True)
		filename = path + "cache/smart/" + ''.join([str(action_reward) for action_reward in enforcer_reward]) + ".csv"
		with open(filename, "w", newline="") as file:
			writer = csv.writer(file)
			writer.writerows(action_probabilities)

def retrieve(path, enforcer_reward, enforcer_model):
	enforcer_action_probabilities = []
	filename = path + "cache/" + enforcer_model + "/" + ''.join([str(action_reward) for action_reward in enforcer_reward]) + ".csv"
	with open(filename, "r") as file:
		reader = csv.reader(file)
		for row in reader:
			enforcer_action_probabilities.append([float(num) for num in row])

	return np.array(enforcer_action_probabilities)

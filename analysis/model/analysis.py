import csv
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from models import *
from utils import *

if __name__ == "__main__":
	# Set up the rationality set.
	rationality_set = np.array([0.01, 0.1, 1.0])

	# Set up the range of ToM that actors can have.
	p_set = np.round(np.linspace(0.0, 1.0, num=11), decimals=1)

	# Set up the ways in which the actor can integrate social reward.
	social_reward = {
		"confidence": np.array([-25.0, -20.0, -15.0, -10.0, -5.0, 0.0, 5.0, 10.0, 15.0, 20.0, 25.0]),
		"preference": np.array([-25.0, -20.0, -15.0, -10.0, -5.0, 0.0, 5.0, 10.0, 15.0, 20.0, 25.0]),
		"proportional": np.array([-2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5])
	}

	# Generates the model predictions for how the enforcer's action changes as a function of the actor's reward. Other
	# considerations include rationality, degree of ToM, the method the actor uses to integrate others' rewards, and 
	# cooperation.
	enforcer_reward = np.array([9, 0])
	actor_rewards = np.array([[0, 0]]+[[a, 0] for a in np.arange(1, 10)]+[[0, b] for b in np.arange(1, 10)])
	with open(PATH+"data/model/enforcer_action_vs_actor_reward.csv", "w", newline="") as file:
		writer = csv.writer(file)
		writer.writerow(["Enforcer_Action", "A", "B", "Cooperation", "Method", "ToM", "Rationality"])
		for rationality in rationality_set:
			for p in p_set:
				for method in social_reward.keys():
					for cooperation in social_reward[method]:
						for actor_reward in actor_rewards:
							enforcer_action_probabilities = enforcer(rationality, enforcer_reward, p=p, \
																	 method=method, cooperation=cooperation, \
																	 reward_assumptions=actor_reward, cache=True)
							writer.writerow([np.argmax(enforcer_action_probabilities[0, :]), \
											 actor_reward[0], actor_reward[1], cooperation, method, p, rationality])

	# Generates the model predictions for how the actor's decision changes as a function of the enforcer's action. Other
	# considerations include rationality, degree of ToM, the method the actor uses to integrate others' rewards, and
	# cooperation.
	enforcer_actions = np.array(list(it.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS)))
	actor_reward = np.array([0, 5])
	with open(PATH+"data/actor_0/model/actor_choice_vs_enforcer_action.csv", "w", newline="") as file:
		writer = csv.writer(file)
		writer.writerow(["Enforcer_Action", "A", "B", "Cooperation", "Method", "ToM", "Rationality"])
		for rationality in rationality_set:
			for p in p_set:
				for method in social_reward.keys():
					for cooperation in social_reward[method]:
						for enforcer_action in [[0, b] for b in np.arange(10)]:
							if p == 0.0:
								action_probabilities = actor_no_ToM(rationality, actor_reward, enforcer_action)
							elif p == 1.0:
								action_probabilities = actor_ToM(rationality, actor_reward, enforcer_action, method=method, \
																 cooperation=cooperation, cache=True)
							else:
								continue

							writer.writerow([enforcer_action[1], action_probabilities[0], action_probabilities[1], \
											 cooperation, method, p, rationality])
	
	sys.exit(print("Done."))

	with open("enforcer_action_vs_actor_p.csv", "w", newline="") as file:
		writer = csv.writer(file)
		for cooperation in cooperation_set:
			for actor_reward in arr4:
			# for b in np.arange(10):
				for p in np.arange(p_set.size):
					enforcer_action_probabilities = enforcer(rationality, enforcer_reward, p=p_set[p], method=method, \
															 cooperation=cooperation, reward_assumptions=actor_reward, cache=True)
					a = actor_reward[0]
					b = actor_reward[1]
					y = np.argmax(enforcer_action_probabilities[0, :])
					print(y)
					writer.writerow([a, b, y, p])
					# The enforcer will only take actions [0, x] because it has reward [9, 0]
					# Index and compute the argmax of [0, x]. Store this as the y variable and the reward assumption as the x variable. 
					# Later, I can use this to easily create a scatterplot.


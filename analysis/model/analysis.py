import csv
import numpy as np
import os
import sys

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
	actor_rewards = np.array([[0, 0]]+[[a, 0] for a in np.arange(1, 10)]+[[0, b] for b in np.arange(1, 10)])
	enforcer_rewards = np.array([[a, 0] for a in np.arange(0, 10)])
	with open(PATH+"data/model/enforcer_action_vs_actor_reward.csv", "w", newline="") as file:
		writer = csv.writer(file)
		writer.writerow(["Actor_Reward", "Enforcer_Action", "Enforcer_Reward", "Cooperation", "Method", "ToM", \
						 "Rationality"])
		for rationality in rationality_set:
			for p in p_set:
				for method in social_reward.keys():
					for cooperation in social_reward[method]:
						for actor_reward in actor_rewards:
							for enforcer_reward in enforcer_rewards:
								action_probabilities = enforcer(rationality, enforcer_reward, p=p, method=method, \
																cooperation=cooperation, \
																reward_assumptions=actor_reward, cache=True)
								writer.writerow([actor_reward[1]-actor_reward[0], \
												 np.argmax(action_probabilities[0, :]), enforcer_reward[0], \
												 cooperation, method, p, rationality])

	# Generates the model predictions for how the actor's decision changes as a function of the enforcer's action. Other
	# considerations include rationality, degree of ToM, the method the actor uses to integrate others' rewards, and
	# cooperation.
	actor_rewards = np.array([[0, b] for b in np.arange(0, 10)])
	enforcer_actions = np.array([[0, 0]]+[[a, 0] for a in np.arange(1, 10)]+[[0, b] for b in np.arange(1, 10)])
	with open(PATH+"data/model/actor_action_vs_enforcer_action.csv", "w", newline="") as file:
		writer = csv.writer(file)
		writer.writerow(["Actor_Reward", "Actor_Action_A", "Actor_Action_B", "Enforcer_Action", "Cooperation", 
						 "Method", "ToM", "Rationality"])
		for rationality in rationality_set:
			for p in p_set:
				for method in social_reward.keys():
					for cooperation in social_reward[method]:
						for actor_reward in actor_rewards:
							for enforcer_action in enforcer_actions:
								if p == 0.0:
									action_probabilities = actor_no_ToM(rationality, actor_reward, enforcer_action)
								elif p == 1.0:
									action_probabilities = actor_ToM(rationality, actor_reward, enforcer_action, 
																	 method=method, cooperation=cooperation, cache=True)
								else:
									continue

								writer.writerow([actor_reward[1], action_probabilities[0], action_probabilities[1], \
												 enforcer_action[1], cooperation, method, p, rationality])

import csv
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

print(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append("D:/Research/social_pragmatics")
from models import *
from utils import *

# Index the left-most piece of the action probabilities, run the next agent pref, stitch it in a "left-join" fashion until
# we're done with the agent prefs. Take max of each column slide (agent pref iteration) and store that value. For p=0, this is trivial.

# For p>0, we don't need to vary cooperation across all 11 variables and create many plots. We only need to use 2 cooperation 
# parameters--0 cooperation and some positive cooperation (like 2.0).

if __name__ == "__main__":
	rationality_set = np.array([0.01, 0.1, 1.0])
	rationality = 0.01
	enforcer_reward = np.array([9, 0])
	p_set = np.linspace(0.0, 1.0, num=11)
	# p_set = np.array([0.0, 1.0])
	methods = ["confidence", "flat", "proportional"]
	method = "proportional"
	cooperation_set = np.array([-5.0, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 5.0])
	cooperation = 1.0
	actor_reward = np.array([0, 4])

	arr1 = [[0, 0]]
	arr2 = [[0, b] for b in range(1, 10)]
	arr3 = [[a, 0] for a in range(1, 10)]
	arr4 = arr1 + arr2 + arr3

	with open("enforcer_action_vs_actor_reward.csv", "w", newline="") as file:
		writer = csv.writer(file)
		for cooperation in cooperation_set:
			for actor_reward in arr4:
				for p in np.arange(p_set.size):
					enforcer_action_probabilities = enforcer(rationality, enforcer_reward, p=p_set[p], method=method, \
															 cooperation=cooperation, reward_assumptions=actor_reward, cache=True)
					a = actor_reward[0]
					b = actor_reward[1]
					y = np.argmax(enforcer_action_probabilities[0, :])
					print(y)
					writer.writerow([a, b, y, p, method, cooperation])
					# The enforcer will only take actions [0, x] because it has reward [9, 0]
					# Index and compute the argmax of [0, x]. Store this as the y variable and the reward assumption as the x variable. 
					# Later, I can use this to easily create a scatterplot.

	sys.exit()

	enforcer_actions = np.array(list(it.product(np.arange(MAX_VALUE), repeat=NUM_ACTIONS)))
	actor_reward = np.array([0, 5])
	with open("actor_choice_vs_enforcer_action.csv", "w", newline="") as file:
		writer = csv.writer(file)
		for p in [0.0, 1.0]:
			for enforcer_action in [[0, b] for b in np.arange(10)]:
				if p == 0.0:
					action_probabilities = actor_no_ToM(rationality, actor_reward, enforcer_action)
				elif p == 1.0:
					action_probabilities = actor_ToM(rationality, actor_reward, enforcer_action, method=method, \
													 cooperation=cooperation, cache=True)

				writer.writerow([enforcer_action[1], action_probabilities[0], action_probabilities[1], p])


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


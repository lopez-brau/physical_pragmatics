from models import * 
from utils import *

import csv
import itertools as it
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import time

if __name__ == "__main__":
	rationality = 1.0
	enforcer_reward = [0, 9]
	method = "proportional"
	cooperation = 2.0
	enforcer_action = [2, 0]
	start_time = time.time()
	for enforcer_action in enforcer_actions:
		# Generate predictions for this parameter set.
		predictions = observer("agent_reward_and_p", rationality, enforcer_reward=enforcer_reward, method=method, \
							   cooperation=cooperation, enforcer_action=enforcer_action, cache=True)

		# Compute the marginal distributions and the expected value of each
		# agent reward and ToM belief.
		P_apple = np.sum(predictions, axis=(1, 2))
		P_pear = np.sum(predictions, axis=(0, 2))
		P_ToM = np.sum(predictions, axis=(0, 1))
		E_apple = np.sum(np.multiply(P_apple, np.arange(10)))
		E_pear = np.sum(np.multiply(P_pear, np.arange(10)))
		E_ToM = np.sum(np.multiply(P_ToM, np.arange(11)/10))

		# Plot the expected values.
		fig, axs = plt.subplots(1, 2, gridspec_kw={'width_ratios': [2, 1]}, sharey=False)
		fig.subplots_adjust(wspace=0.35)
		axs[0].bar(["A", "B"], [expected_A, expected_B])
		axs[0].set_ylim(0, 9)
		axs[0].set_ylabel("E[Reward Value]")
		axs[1].bar(["p"], [expected_p])
		axs[1].set_ylim(0.0, 1.0)
		axs[1].set_ylabel("E[P(ToM)]")
		fig.suptitle("Enforcer Action = %s" % str(enforcer_action))
		plt.savefig("scratch/" + str(enforcer_action) + "_" + str(NATURAL_COST) + ".png", bbox_inches="tight")
		plt.close(fig)

		# Write to a file.
		filename = "data/observer_1/observer_" + str(rationality) + "_" + METHOD + "_" + str(cooperation) + "_" + \
				    str(enforcer_reward) + "_" + str(enforcer_action) + "_" + str(NATURAL_COST) + ".txt"
		with open(filename, "w", newline="") as file:
			writer = csv.writer(file)
			writer.writerows([E_apple, E_pear, E_ToM])

	# p1 = predictions[56]
	# print(p1)
	# predictions = predictions.reshape(MAX_VALUE, MAX_VALUE, 11)
	# p2 = predictions[5][6]
	# print(p2)
	# print(p1-p2)

	# fig, axs = plt.subplots(1, 2, gridspec_kw={'width_ratios': [2, 1]}, sharey=False)
	# fig.subplots_adjust(wspace=0.35)
	# axs[0].bar(["A", "B"], [expected_A, expected_B])
	# axs[0].set_ylim(0, 9)
	# axs[0].set_ylabel("E[Reward Value]")
	# axs[1].bar(["p"], [expected_p])
	# axs[1].set_ylim(0.0, 1.0)
	# axs[1].set_ylabel("E[P(ToM)]")
	# fig.suptitle("Enforcer Action = %s" % str(enforcer_action))
	# plt.savefig("scratch/" + str(enforcer_action) + "_" + str(NATURAL_COST) + ".png", bbox_inches="tight")
	# plt.close(fig)


	print(time.time()-start_time)
	sys.exit("Done.")

	# rationality_set = np.array([0.1, 1.0])
	# methods = ["confidence", "flat", "confidence"]
	# cooperation_subset = np.array([0.0, 0.5, 1.0, 1.5, 2.0, 5.0])
	# generalized_enforcer_rewards = np.array([[0, 0], [0, 3], [0, 6], [0, 9]])
	# for rationality in rationality_set:
	# 	for method in methods:
	# 		for cooperation in cooperation_subset:
	# 			for enforcer_reward in generalized_enforcer_rewards:
	# 				start_time = time.time()
	# 				for enforcer_action in np.array([[0, 0], [1, 0], [2, 0], [3, 0]]):
	# 					predictions = observer("agent_reward_and_p", rationality, enforcer_reward=enforcer_reward, method=method, \
	# 								   		   cooperation=cooperation, enforcer_action=enforcer_action, cache=True)
					
	# 					filename = "data/observer_1/observer_" + str(rationality) + "_" + METHOD + "_" + str(cooperation) + "_" + \
	# 							   str(enforcer_reward) + "_" + str(enforcer_action) + "_" + str(NATURAL_COST) + ".txt"
	# 					with open(filename, "w", newline="") as file:
	# 						writer = csv.writer(file)
	# 						writer.writerows(predictions)	
	# 				print(time.time()-start_time)

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
	p = 1.0
	method = "proportional"
	cooperation = 2.0
	enforcer_action = [2, 0]
	enforcer_actions = [[0, 0], [1, 0], [2, 0], [3, 0]]
	
	# x1 = enforcer(rationality, enforcer_reward, plot=True)
	x2 = enforcer(rationality, enforcer_reward, p=p, method=method, cooperation=cooperation, cache=True, plot=True)

	cooperation = -2.0
	x3 = enforcer(rationality, enforcer_reward, p=p, method=method, cooperation=cooperation, cache=True, plot=True)
	# print(np.where(x1, np.max(x1)))
	plt.show()
	sys.exit("Done.")

	for enforcer_action in enforcer_actions:
		start_time = time.time()
		# Generate predictions for this parameter set.
		predictions = observer("agent_reward_and_p", rationality, enforcer_reward=enforcer_reward, method=method, \
							   cooperation=cooperation, enforcer_action=enforcer_action, cache=True)
		print(time.time()-start_time)
		
		# Compute the marginal distributions and the expected value of each
		# agent reward and ToM belief.
		predictions = predictions.reshape(MAX_VALUE, MAX_VALUE, 11)
		P_pear = np.sum(predictions, axis=(1, 2))
		P_pomegranate = np.sum(predictions, axis=(0, 2))
		P_ToM = np.sum(predictions, axis=(0, 1))
		E_pear = np.sum(np.multiply(P_pear, np.arange(MAX_VALUE)))
		E_pomegranate = np.sum(np.multiply(P_pomegranate, np.arange(MAX_VALUE)))
		E_ToM = np.sum(np.multiply(P_ToM, np.arange(11)/MAX_VALUE))

		# Plot the expected values.
		# fig, axs = plt.subplots(1, 2, gridspec_kw={'width_ratios': [2, 1]}, sharey=False)
		# fig.subplots_adjust(wspace=0.35)
		# axs[0].bar(["Pears", "Pomegranates"], [E_pear, E_pomegranate])
		# axs[0].set_ylim(0, 9)
		# axs[0].set_ylabel("E[Agent Rewards]")
		# axs[1].bar(["p"], [E_ToM])
		# axs[1].set_ylim(0.0, 1.0)
		# axs[1].set_ylabel("E[P(ToM)]")
		# fig.suptitle("Enforcer Action = %s" % str(enforcer_action))
		# plt.savefig("data/model_plots/" + str(np.array(enforcer_action)) + "_" + str(np.array(NATURAL_COST)) + 
		# 			".png", bbox_inches="tight")
		# plt.close(fig)

		# Write to a file.
		# filename = "scratch/" + str(rationality) + "_" + METHOD + "_" + str(cooperation) + "_" + \
		# 		    str(enforcer_reward) + "_" + str(enforcer_action) + "_" + str(NATURAL_COST) + ".txt"
		filename = "data/model_0.1/" + str(np.array(NATURAL_COST)) + "_" + str(np.array(enforcer_action)) + ".txt"
		with open(filename, "w", newline="") as file:
			writer = csv.writer(file)
			writer.writerows([[E_pear], [E_pomegranate], [E_ToM]])

	

	# rationality_set = np.array([0.1, 1.0])
	# methods = ["confidence", "flat", "confidence"]
	# cooperation_subset = np.array([0.5, 1.0, 1.5, 2.0, 5.0])
	# generalized_enforcer_rewards = np.array([[0, 0], [0, 3], [0, 6], [0, 9]])
	# for rationality in rationality_set:
	# 	for method in methods:
	# 		for cooperation in cooperation_subset:
	# 			for enforcer_reward in generalized_enforcer_rewards:
	# 				start_time = time.time()
	# 				for enforcer_action in np.array([[1, 0], [2, 0], [3, 0]]):
	# 					predictions = observer("agent_reward_and_p", rationality, enforcer_reward=enforcer_reward, method=method, \
	# 								   		   cooperation=cooperation, enforcer_action=enforcer_action, cache=True)
					
	# 					filename = "data/observer_1/observer_" + str(rationality) + "_" + METHOD + "_" + str(cooperation) + "_" + \
	# 							   str(enforcer_reward) + "_" + str(enforcer_action) + "_" + str(NATURAL_COST) + ".txt"
	# 					with open(filename, "w", newline="") as file:
	# 						writer = csv.writer(file)
	# 						writer.writerows(predictions)	
	# 				print(time.time()-start_time)

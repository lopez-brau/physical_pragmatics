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

	# Set up model parameters.
	rationality = 1.0
	enforcer_reward = np.array([4, 0])
	method = "confidence"
	cooperation = 5.0
	actor_reward = np.array([0, 5])
	enforcer_action = np.array([6, 4])

	enforcer(rationality, enforcer_reward, p=1.0, method=method, cooperation=cooperation, cache=True, plot=True)

	sys.exit(plt.show())

	# Compute model predictions for all enforcer actions.
	for enforcer_action in enforcer_actions:
		
		# Generate predictions for this parameter set.
		start_time = time.time()
		predictions = observer("agent_reward_and_p", rationality, enforcer_reward=enforcer_reward, method=method, \
							   cooperation=cooperation, enforcer_action=enforcer_action, cache=True)
		print("Done with enforcer_action: " + str(np.array(enforcer_action)) + "\t" + str(time.time()-start_time))
		
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
		filename = "data/observer_1/model/123/" + str(rationality) + "/" + str(np.array(NATURAL_COST)) + "_" + \
				   str(np.array(enforcer_action)) + ".txt"
		with open(filename, "w", newline="") as file:
			writer = csv.writer(file)
			writer.writerows([[E_pear], [E_pomegranate], [E_ToM]])

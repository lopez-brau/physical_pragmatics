from models import * 
from utils import *

import csv
import itertools as it
import matplotlib.pyplot as plt
import numpy as np
import time

# Variables:
# Enforcer's beliefs (distributional assumptions) about agent rewards 
# Enforcer's beliefs of an agent's degree of ToM
# Cooperation
# Enforcer rewards
# Enforcer action

# The question we're trying to answer is how people assign meaning to objects.
# "Starting with Baker 2009..."
# We want to show that in order to do this assignment, we need 
# 	1) ToM
#	2) Intuitive physics (for understanding costs) 
# 	3) A sense of cooperation (or lack of)
# Develop a "one-slider" to my project; like the hat on the chair example
# Loss aversion is not part of our mental models; loss aversion paper was counterintuitive!
# Develop super simple plot or graphic that explains the problem to the core


# We have three problems:
# 	1. Wall-building/deterrent: review increasing MAX_VALUE and psychological implications
#	2. Rationality: easy fix
#	3. Cooperation: method and parameter value. Is there a way we can fix this by collecting empirical data?

if __name__ == "__main__":
	agent_reward = np.array([9, 0])
	enforcer_reward = np.array([0, 9])
	enforcer_action = np.array([1, 0])

	rationality = 0.1
	cooperation = 2.0
	p = 1.0

	# Enforcer reasoning about an agent with no ToM.
	# x1 = enforcer(rationality, enforcer_reward, plot=True)

	# Enforcer reasoning about an agent with ToM.
	# x2 = enforcer(rationality, enforcer_reward, p=p, cooperation=cooperation, plot=True)

	# Observer inferring the enforcer's beliefs about the agent reward and degree of ToM.
	# enforcer_actions = np.array([[0, 0], [0, 1], [1, 0], [1, 1], [4, 0], [0, 4], [4, 4], [4, 1], [1, 4]])
	enforcer_actions = np.array([[0, 0], [1, 0], [4, 0]])
	for enforcer_action in enforcer_actions:
		predictions = observer("agent_reward_and_p", rationality, enforcer_reward=enforcer_reward, cooperation=cooperation, \
							   enforcer_action=enforcer_action)
		filename = "predictions/" + str(cooperation) + "/" + str(NATURAL_COST) + "_" + str(enforcer_action) + ".txt"
		with open(path + filename, "w", newline="") as file:
			writer = csv.writer(file)
			writer.writerows(predictions)

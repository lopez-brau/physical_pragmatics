from utils import *

def convert_cost(enforcer_action):
	agent_cost = np.zeros(NUM_ACTIONS)

	for i in np.arange(NUM_ACTIONS):
		agent_cost[i] = NATURAL_COST[i] + COST_TABLE[enforcer_action[i]]

	return agent_cost

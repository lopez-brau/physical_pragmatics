from utils import *

def convert_cost(enforcer_action):
	agent_cost = np.zeros(NUM_ACTIONS)

	for i in np.arange(NUM_ACTIONS):
		agent_cost[i] = COST_TABLE[NATURAL_COST[i]+enforcer_action[i]]

	return agent_cost

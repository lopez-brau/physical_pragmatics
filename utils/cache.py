import csv
import numpy as np

from .config import *

def cache_enforcer_no_ToM(model, enforcer_rewards, rationality): 
    filename = "cache/enforcer_no_ToM.csv"
    with open(filename, "w", newline="") as file:
        for enforcer_reward in enforcer_rewards:
            writer = csv.writer(file)
            action_probabilities = model(enforcer_reward, rationality)
            writer.writerows(action_probabilities)
            file.write("\n")

def cache_agent_ToM(model, agent_rewards, agent_cost, enforcer_actions, rationality, cooperation_set):
    i = 0
    for cooperation in cooperation_set:
        filename = "cache/agent_ToM/" + METHOD + "/" + str(cooperation) + ".csv"
        with open(filename, "w", newline="") as file:
            for agent_reward in agent_rewards:
                for enforcer_action in enforcer_actions:
                    action_probabilities = model(agent_reward, agent_cost, enforcer_action, rationality, cooperation, cache=True)
                    print("Iteration: " + str(i))
                    i += 1
                    writer = csv.writer(file)
                    writer.writerow(action_probabilities)

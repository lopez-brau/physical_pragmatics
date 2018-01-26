import csv
import numpy as np

from .config import *

def cache_enforcer_no_ToM(model, rationality, enforcer_rewards): 
    filename = "cache/enforcer_no_ToM.csv"
    with open(filename, "w", newline="") as file:
        for enforcer_reward in enforcer_rewards:
            writer = csv.writer(file)
            action_probabilities = model(rationality, enforcer_reward)
            writer.writerows(action_probabilities)
            file.write("\n")

def cache_agent_ToM(model, rationality, agent_rewards, enforcer_actions, p_set, cooperation_set):
    for p in p_set:
        for cooperation in cooperation_set:
            filename = "cache/agent_ToM/" + METHOD + "/" + str(p) + "/" + str(cooperation) + ".csv"
            with open(filename, "w", newline="") as file:
                for agent_reward in agent_rewards:
                    for enforcer_action in enforcer_actions:
                        action_probabilities = model(rationality, agent_reward, enforcer_action, p=p, cooperation=cooperation, 
                                                     cache=True)
                        writer = csv.writer(file)
                        writer.writerow(action_probabilities)

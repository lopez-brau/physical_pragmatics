from .config import *

import csv
import numpy as np

def cache_agent_no_ToM(model, rationality, agent_rewards, enforcer_actions):
    path = "cache/gridworld/" if GRIDWORLD == True else "cache/standard/"
    filename = path + "agent_no_ToM/" + str(rationality) + ".csv"
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        for agent_reward in agent_rewards:
            for enforcer_action in enforcer_actions:
                action_probabilities = model(rationality, agent_reward, enforcer_action)
                writer.writerow(action_probabilities)

def cache_enforcer_no_ToM(model, rationality, enforcer_rewards): 
    path = "cache/gridworld/" if GRIDWORLD == True else "cache/standard/"
    filename = path + "enforcer_no_ToM/" + str(rationality) + ".csv"
    with open(filename, "w", newline="") as file:
        for enforcer_reward in enforcer_rewards:
            writer = csv.writer(file)
            action_probabilities = model(rationality, enforcer_reward, cache=True)
            writer.writerows(action_probabilities)
            file.write("\n")

def cache_agent_ToM(model, rationality, agent_rewards, enforcer_actions, cooperation_set):
    path = "cache/gridworld/" if GRIDWORLD == True else "cache/standard/"
    for cooperation in cooperation_set:
        filename = path + "agent_ToM/" + str(rationality) + "/" + METHOD + "/" + str(cooperation) + ".csv"
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            for agent_reward in agent_rewards:
                for enforcer_action in enforcer_actions:
                    action_probabilities = model(rationality, agent_reward, enforcer_action, cooperation=cooperation, 
                                                 cache=True)
                    writer.writerow(action_probabilities)
        
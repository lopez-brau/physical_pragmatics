from .config import *

import csv
import numpy as np

def cache_agent_no_ToM(model, rationality, agent_rewards, enforcer_actions):
    path = "cache/gridworld_" if GRIDWORLD == True else "cache/standard_"
    filename = path + "agent_no_ToM_" + str(rationality) + "_" + str(NATURAL_COST) + ".csv"
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        data = [""] * (MAX_VALUE**(NUM_ACTIONS*2))
        for agent_reward in agent_rewards:
            agent_reward_index = "".join([str(num) for num in agent_reward])
            for enforcer_action in enforcer_actions:
                enforcer_action_index = "".join([str(num) for num in enforcer_action])
                action_probabilities = model(rationality, agent_reward, enforcer_action)
                data[int("".join([agent_reward_index, enforcer_action_index]))] = action_probabilities
        writer.writerows(data)

def cache_enforcer_no_ToM(model, rationality, enforcer_rewards): 
    path = "cache/gridworld_" if GRIDWORLD == True else "cache/standard_"
    filename = path + "enforcer_no_ToM_" + str(rationality) + "_" + str(NATURAL_COST) + ".csv"
    with open(filename, "w", newline="") as file:
        for enforcer_reward in enforcer_rewards:
            writer = csv.writer(file)
            action_probabilities = model(rationality, enforcer_reward, cache=True)
            writer.writerows(action_probabilities)
            file.write("\n")

def cache_agent_ToM(model, rationality, agent_rewards, enforcer_actions, cooperation_set):
    path = "cache/gridworld_" if GRIDWORLD == True else "cache/standard_"
    for cooperation in cooperation_set:
        filename = path + "agent_ToM_" + str(rationality) + "_" + METHOD + "_" + str(cooperation) + "_" + str(NATURAL_COST) + ".csv"
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            data = [""] * (MAX_VALUE**(NUM_ACTIONS*2))
            for agent_reward in agent_rewards:
                agent_reward_index = "".join([str(num) for num in agent_reward])
                for enforcer_action in enforcer_actions:
                    enforcer_action_index = "".join([str(num) for num in enforcer_action])
                    action_probabilities = model(rationality, agent_reward, enforcer_action, cooperation=cooperation, 
                                                 cache=True)
                    data[int("".join([agent_reward_index, enforcer_action_index]))] = action_probabilities
            writer.writerows(data)

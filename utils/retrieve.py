from .config import *

import csv
import numpy as np

def retrieve_enforcer_no_ToM(enforcer_rewards, enforcer_action, likelihood):
    path = "cache/gridworld/" if GRIDWORLD == True else "cache/standard/"
    filename = path + "enforcer_no_ToM.csv"
    with open(filename, "r") as file:
        reader = csv.reader(file)
        action_probabilities = []
        for enforcer_reward in enforcer_rewards:
            row = next(reader)
            while row != []:
                action_probabilities.append([float(num) for num in row])
                row = next(reader)
            likelihood[tuple(enforcer_reward)] = np.array(action_probabilities)[tuple(enforcer_action)]
            action_probabilities = []

    return likelihood

def retrieve_agent_ToM(enforcer_reward, agent_rewards, enforcer_actions, p, cooperation, U):
    path = "cache/gridworld/" if GRIDWORLD == True else "cache/standard/"
    filename = path + "agent_ToM/" + METHOD + "/" + str(p) + "/" + str(cooperation) + ".csv"
    with open(filename, "r") as file:
        reader = csv.reader(file)
        temp = np.zeros(U.shape)
        for agent_reward in agent_rewards:
            for enforcer_action in enforcer_actions:
                row = next(reader)
                action_probabilities = [float(num) for num in row]
                expected_enforcer_reward = np.dot(enforcer_reward, action_probabilities)
                temp[tuple(enforcer_action)] = expected_enforcer_reward - (COST_RATIO*sum(enforcer_action))
            U = U + temp
        U = U / np.prod(U.shape)

    return U
from .config import *

import csv
import numpy as np

def process_enforcer_no_ToM(rationality, enforcer_rewards, enforcer_action, likelihood):
    path = "cache/gridworld_" if GRIDWORLD == True else "cache/standard_"
    filename = path + "enforcer_no_ToM_" + str(rationality) + "_" + str(NATURAL_COST) + ".csv"
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

def process_agent(rationality, enforcer_reward, agent_rewards, enforcer_actions, p, method, cooperation, U):
    path = "cache/gridworld_" if GRIDWORLD == True else "cache/standard_"
    if p != 1.0:
        filename_agent_no_ToM = path + "agent_no_ToM_" + str(rationality) + "_" + str(NATURAL_COST) + ".csv"
        file_agent_no_ToM = open(filename_agent_no_ToM, "r")
        reader_agent_no_ToM = csv.reader(file_agent_no_ToM)
        lines_agent_no_ToM = [row for row in reader_agent_no_ToM]
    
    if p != 0.0:
        filename_agent_ToM = path + "agent_ToM_" + str(rationality) + "_" + method + "_" + str(cooperation) + "_" + \
                             str(NATURAL_COST) + ".csv"    
        file_agent_ToM = open(filename_agent_ToM, "r")
        reader_agent_ToM = csv.reader(file_agent_ToM)
        lines_agent_ToM = [row for row in reader_agent_ToM]
    
    U_agent_no_ToM = np.zeros(U.shape)
    U_agent_ToM = np.zeros(U.shape)
    temp_agent_no_ToM = np.zeros(U.shape)
    temp_agent_ToM = np.zeros(U.shape)
    for agent_reward in agent_rewards:
        agent_reward_index = "".join([str(num) for num in agent_reward])
        for enforcer_action in enforcer_actions:
            enforcer_action_index = "".join([str(num) for num in enforcer_action])
            if p != 1.0:
                row = lines_agent_no_ToM[int("".join([agent_reward_index, enforcer_action_index]))]
                action_probabilities = [float(num) for num in row]
                expected_enforcer_reward = np.dot(enforcer_reward, action_probabilities)
                temp_agent_no_ToM[tuple(enforcer_action)] = expected_enforcer_reward - (COST_RATIO*sum(enforcer_action))

            if p != 0.0:
                row = lines_agent_ToM[int("".join([agent_reward_index, enforcer_action_index]))]
                action_probabilities = [float(num) for num in row]
                expected_enforcer_reward = np.dot(enforcer_reward, action_probabilities)
                temp_agent_ToM[tuple(enforcer_action)] = expected_enforcer_reward - (COST_RATIO*sum(enforcer_action))
        U_agent_no_ToM = U_agent_no_ToM + temp_agent_no_ToM
        U_agent_ToM = U_agent_ToM + temp_agent_ToM
    U_agent_no_ToM = U_agent_no_ToM / len(agent_rewards)
    U_agent_ToM = U_agent_ToM / len(agent_rewards)
    U = ((1.0-p)*U_agent_no_ToM) + (p*U_agent_ToM)

    return U

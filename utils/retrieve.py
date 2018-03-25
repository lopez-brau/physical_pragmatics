from .config import *

import csv
import numpy as np

def retrieve_enforcer_no_ToM(rationality, enforcer_rewards, enforcer_action, likelihood):
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

def retrieve_agent(rationality, enforcer_reward, agent_rewards, enforcer_actions, p, cooperation, U):
    path = "cache/gridworld_" if GRIDWORLD == True else "cache/standard_"
    if p != 1.0:
        filename_agent_no_ToM = path + "agent_no_ToM_" + str(rationality) + "_" + str(NATURAL_COST) + ".csv"
        file_agent_no_ToM = open(filename_agent_no_ToM, "r")
        reader_agent_no_ToM = csv.reader(file_agent_no_ToM)
    
    if p != 0.0:
        filename_agent_ToM = path + "agent_ToM_" + str(rationality) + "_" + METHOD + "_" + str(cooperation) + "_" + \
                             str(NATURAL_COST) + ".csv"    
        file_agent_ToM = open(filename_agent_ToM, "r")
        reader_agent_ToM = csv.reader(file_agent_ToM)
    
    U_agent_no_ToM = np.zeros(U.shape)
    U_agent_ToM = np.zeros(U.shape)
    temp_agent_no_ToM = np.zeros(U.shape)
    temp_agent_ToM = np.zeros(U.shape)
    for agent_reward in agent_rewards:
        for enforcer_action in enforcer_actions:
            if p != 1.0:
                row = next(reader_agent_no_ToM)
                action_probabilities = [float(num) for num in row]
                expected_enforcer_reward = np.dot(enforcer_reward, action_probabilities)
                temp_agent_no_ToM[tuple(enforcer_action)] = expected_enforcer_reward - (COST_RATIO*sum(enforcer_action))

            if p != 0.0:
                row = next(reader_agent_ToM)
                action_probabilities = [float(num) for num in row]
                expected_enforcer_reward = np.dot(enforcer_reward, action_probabilities)
                temp_agent_ToM[tuple(enforcer_action)] = expected_enforcer_reward - (COST_RATIO*sum(enforcer_action))

        U_agent_no_ToM = U_agent_no_ToM + temp_agent_no_ToM
        U_agent_ToM = U_agent_ToM + temp_agent_ToM
    U_agent_no_ToM = U_agent_no_ToM / np.prod(U.shape)
    U_agent_ToM = U_agent_ToM / np.prod(U.shape)
    U = ((1.0-p)*U_agent_no_ToM) + (p*U_agent_ToM)

    return U

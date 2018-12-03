import csv
import numpy as np
import os
import sys

from .config import *

def process_actor(rationality, enforcer_reward, actor_rewards, enforcer_actions, p, method, cooperation, U):
    environment = "cache/gridworld_" if GRIDWORLD == True else "cache/standard_"
    if p != 1.0:
        filename_actor_no_ToM = environment + "actor_no_ToM_" + str(rationality) + "_" + str(NATURAL_COST) + ".csv"
        with open(PATH+filename_actor_no_ToM, "r") as file_actor_no_ToM:
            reader_actor_no_ToM = csv.reader(file_actor_no_ToM)
            lines_actor_no_ToM = [row for row in reader_actor_no_ToM]
    
    if p != 0.0:
        filename_actor_ToM = environment + "actor_ToM_" + str(rationality) + "_" + method + "_" + str(cooperation) + \
                             "_" + str(NATURAL_COST) + ".csv"    
        with open(PATH+filename_actor_ToM, "r") as file_actor_ToM:
            reader_actor_ToM = csv.reader(file_actor_ToM)
            lines_actor_ToM = [row for row in reader_actor_ToM]
    
    U_actor_no_ToM = np.zeros(U.shape)
    U_actor_ToM = np.zeros(U.shape)
    temp_actor_no_ToM = np.zeros(U.shape)
    temp_actor_ToM = np.zeros(U.shape)
    for actor_reward in actor_rewards:
        actor_reward_index = "".join([str(num) for num in actor_reward])
        for enforcer_action in enforcer_actions:
            enforcer_action_index = "".join([str(num) for num in enforcer_action])
            if p != 1.0:
                row = lines_actor_no_ToM[int("".join([actor_reward_index, enforcer_action_index]))]
                action_probabilities = [float(num) for num in row]
                expected_enforcer_reward = np.dot(enforcer_reward, action_probabilities)
                temp_actor_no_ToM[tuple(enforcer_action)] = expected_enforcer_reward - \
                                                            (COST_RATIO*sum(enforcer_action))

            if p != 0.0:
                row = lines_actor_ToM[int("".join([actor_reward_index, enforcer_action_index]))]
                action_probabilities = [float(num) for num in row]
                expected_enforcer_reward = np.dot(enforcer_reward, action_probabilities)
                temp_actor_ToM[tuple(enforcer_action)] = expected_enforcer_reward - (COST_RATIO*sum(enforcer_action))
        U_actor_no_ToM = U_actor_no_ToM + temp_actor_no_ToM
        U_actor_ToM = U_actor_ToM + temp_actor_ToM
    U_actor_no_ToM = U_actor_no_ToM / len(actor_rewards)
    U_actor_ToM = U_actor_ToM / len(actor_rewards)
    U = ((1.0-p)*U_actor_no_ToM) + (p*U_actor_ToM)

    return U

def process_enforcer(rationality, enforcer_rewards, enforcer_action, likelihood, p=0.0, method=None, \
                     cooperation=None):
    environment = "cache/gridworld_" if GRIDWORLD == True else "cache/standard_"
    if p == 0.0:
        filename = environment + "enforcer_no_ToM_" + str(rationality) + "_" + str(NATURAL_COST) + ".csv"
    else:
        filename = environment + "enforcer_ToM_" + str(rationality) + "_" + str(p) + "_" + method + "_" + \
                   str(cooperation) + "_" + str(NATURAL_COST) + ".csv"
    
    with open(PATH+filename, "r") as file:
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

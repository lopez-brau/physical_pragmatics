import csv
import numpy as np

def retrieve_no_ToM_enforcer(enforcer_reward):
    action_probabilities = []
    filename = "cache/no_ToM_enforcer.csv" 
    with open(filename, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            action_probabilities.append([float(num) for num in row])

    return np.array(action_probabilities)

def retrieve_ToM_agent(agent_reward, enforcer_action, cooperation, method):
    filename = "cache/smart_agent/" + method + "_" + str(cooperation) + "_" + \
               ''.join([str(action_reward) for action_reward in agent_reward]) + "_" + \
               ''.join([str(action) for action in enforcer_action]) + ".csv"
    with open(filename, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            action_probabilities = [float(num) for num in row]

    return np.array(action_probabilities)

import csv
import numpy as np

def cache_no_ToM_enforcer(model, enforcer_rewards, rationality): 
    filename = "cache/no_ToM_enforcer.csv"
    with open(filename, "w", newline="") as file:
        for enforcer_reward in enforcer_rewards:
            writer = csv.writer(file)
            action_probabilities = model(enforcer_reward, rationality)
            writer.writerows(action_probabilities)

def cache_ToM_agent(model, agent_rewards, agent_cost, enforcer_actions, rationality, cooperation_set):
    # methods = ["confidence", "flat", "proportional"]
    methods = ["flat"]
    i = 0
    for method in methods:
        for cooperation in cooperation_set:
            for agent_reward in agent_rewards:
                for enforcer_action in enforcer_actions:
                    action_probabilities = model(agent_reward, agent_cost, enforcer_action, rationality, cooperation, 
                                                 method, cache=True)
                    print("Iteration: " + str(i))
                    i += 1
                    filename = "cache/smart_agent/" + method + "/" + str(cooperation) + ".csv"
                    with open(filename, "a", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow(action_probabilities)

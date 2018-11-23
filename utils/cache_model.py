import csv
import numpy as np

from .config import *

def cache_actor_no_ToM(model, rationality_set, actor_rewards, enforcer_actions):
    environment = "cache/gridworld_" if GRIDWORLD == True else "cache/standard_"
    for rationality in rationality_set:
        filename = environment + "actor_no_ToM_" + str(rationality) + "_" + str(NATURAL_COST) + ".csv"
        with open(PATH+filename, "w", newline="") as file:
            writer = csv.writer(file)
            data = [""] * (MAX_VALUE**(NUM_ACTIONS*2))
            for actor_reward in actor_rewards:
                actor_reward_index = "".join([str(num) for num in actor_reward])
                for enforcer_action in enforcer_actions:
                    enforcer_action_index = "".join([str(num) for num in enforcer_action])
                    action_probabilities = model(rationality, actor_reward, enforcer_action)
                    data[int("".join([actor_reward_index, enforcer_action_index]))] = action_probabilities
            writer.writerows(data)

def cache_enforcer_no_ToM(model, rationality_set, enforcer_rewards): 
    environment = "cache/gridworld_" if GRIDWORLD == True else "cache/standard_"
    for rationality in rationality_set:
        filename = environment + "enforcer_no_ToM_" + str(rationality) + "_" + str(NATURAL_COST) + ".csv"
        with open(PATH+filename, "w", newline="") as file:
            for enforcer_reward in enforcer_rewards:
                writer = csv.writer(file)
                action_probabilities = model(rationality, enforcer_reward, cache=True)
                writer.writerows(action_probabilities)
                file.write("\n")

def cache_actor_ToM(model, rationality_set, actor_rewards, enforcer_actions, methods, cooperation_set):
    environment = "cache/gridworld_" if GRIDWORLD == True else "cache/standard_"
    for rationality in rationality_set:
        for method in methods:
            for cooperation in cooperation_set:
                filename = environment + "actor_ToM_" + str(rationality) + "_" + method + "_" + str(cooperation) + "_" + \
                           str(NATURAL_COST) + ".csv"
                with open(PATH+filename, "w", newline="") as file:
                    writer = csv.writer(file)
                    data = [""] * (MAX_VALUE**(NUM_ACTIONS*2))
                    for actor_reward in actor_rewards:
                        actor_reward_index = "".join([str(num) for num in actor_reward])
                        for enforcer_action in enforcer_actions:
                            enforcer_action_index = "".join([str(num) for num in enforcer_action])
                            action_probabilities = model(rationality, actor_reward, enforcer_action, method=method, \
                                                         cooperation=cooperation, cache=True)
                            data[int("".join([actor_reward_index, enforcer_action_index]))] = action_probabilities
                    writer.writerows(data)

# def cache_enforcer_ToM(model, rationality_set, enforcer_rewards, p_set, methods, cooperation_set, reward_assumptions):
#     environment = "cache/gridworld_" if GRIDWORLD == True else "cache/standard_"
#     for rationality in rationality_set:
#         for method in methods:
#             for cooperation in cooperation_set:
#                 for actor_rewards in reward_assumptions:

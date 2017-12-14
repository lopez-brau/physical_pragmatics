import numpy as np
import csv

def softmax(U, rationality):
    # Subtracting away the max prevents overflow.
    U = U - np.max(U)
    exp = np.exp(U/rationality)

    return exp / sum(exp)

def cooperative_reward(enforcer_rewards, reward_probabilities, cooperation, method):
    num_actions = len(np.shape(reward_probabilities))
    inferred_enforcer_action = np.zeros(num_actions)

    # The "confidence" method computes the probabilities of each enforcer 
    # action being the optimal one.
    if method == "confidence":
        for enforcer_reward in enforcer_rewards:
            optimal_enforcer_action = (max(enforcer_reward) == np.array(enforcer_reward)) + 0.0
            inferred_enforcer_action = inferred_enforcer_action + \
                                       (reward_probabilities[enforcer_reward]*optimal_enforcer_action)

    # The "flat" method computes the expected enforcer rewards and infers that
    # the max of those rewards is the optimal enforcer action.
    elif method == "flat":
        expected_enforcer_rewards = np.zeros(num_actions)
        for enforcer_reward in enforcer_rewards:
            expected_enforcer_rewards = expected_enforcer_rewards + \
                                        (reward_probabilities[enforcer_reward]*np.array(enforcer_reward))
        inferred_enforcer_action = (max(expected_enforcer_rewards) == expected_enforcer_rewards) + 0.0

    # The "proportional" method computes the expected enforcer rewards.
    elif method == "proportional":
        expected_enforcer_rewards = np.zeros(num_actions)
        for enforcer_reward in enforcer_rewards:
            expected_enforcer_rewards = expected_enforcer_rewards + \
                                        (reward_probabilities[enforcer_reward]*np.array(enforcer_reward))
        inferred_enforcer_action = expected_enforcer_rewards

    # Throw an error if there's a typo in the method type.
    else:
        print("Invalid method.")
        return

    return cooperation*inferred_enforcer_action

def cache_no_ToM_enforcer(model, enforcer_rewards, rationality): 
    for enforcer_reward in enforcer_rewards:
        action_probabilities = model(enforcer_reward, rationality)
        filename = "cache/dumb_enforcer/" + ''.join([str(action_reward) for action_reward in enforcer_reward]) + ".csv"
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(action_probabilities)

def cache_no_ToM_enforcer2(model, enforcer_rewards, rationality): 
    for enforcer_reward in enforcer_rewards:
        action_probabilities = model(enforcer_reward, rationality)
        filename = "cache/no_ToM_enforcer.csv"
        with open(filename, "a", newline="") as file:
            writer = csv.writer(file)
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

def access_no_ToM_enforcer(enforcer_reward):
    action_probabilities = []
    # filename = "cache/dumb_enforcer/" + ''.join([str(action_reward) for action_reward in enforcer_reward]) + ".csv"
    filename = "cache/no_ToM_enforcer.csv" 
    with open(filename, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            action_probabilities.append([float(num) for num in row])

    return np.array(action_probabilities)

def access_ToM_agent(agent_reward, enforcer_action, cooperation, method):
    filename = "cache/smart_agent/" + method + "_" + str(cooperation) + "_" + \
               ''.join([str(action_reward) for action_reward in agent_reward]) + "_" + \
               ''.join([str(action) for action in enforcer_action]) + ".csv"
    with open(filename, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            action_probabilities = [float(num) for num in row]

    return np.array(action_probabilities)

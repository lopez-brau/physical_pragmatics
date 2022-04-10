import itertools as it
import matplotlib.pyplot as plt
import numpy as np

from config import *
from cooperative_reward import *
from load_model import *
from softmax import *

def decider(rationality, decider_reward, enforcer_action, ToM=False,
        method="", cooperation=0.0, plot=False):
    # Reason about the enforcer if the decider knows the scene was modified
    # intentionally.
    if ToM == True:
        # Generate possible enforcer rewards.
        enforcer_rewards = np.array(list(it.product(np.arange(MAX_REWARD),
            repeat=NUM_ACTIONS)))

        # Set up the likelihood space.
        space = [MAX_REWARD for action in np.arange(NUM_ACTIONS)]
        likelihood = np.zeros(space)

        # Compute the likelihood.
        if CACHE == True:
            likelihood = load_enforcer("enforcer_reward", rationality,
                enforcer_action, enforcer_rewards, likelihood, ToM=0.0,
                method=method, cooperation=cooperation)
        else:
            for enforcer_reward in enforcer_rewards:
                enforcer_action_probabilities = enforcer(rationality,
                    enforcer_reward)
                likelihood[tuple(enforcer_reward)] = \
                    enforcer_action_probabilities[tuple(enforcer_action)]

        # Normalize the likelihood to generate the posterior.
        likelihood = likelihood.flatten()
        if sum(likelihood) == 0:
            posterior = likelihood.reshape(space)
        else:
            posterior = (likelihood/sum(likelihood)).reshape(space)

        # Plot the posterior over enforcer rewards.
        if plot == True:
            plt.figure()
            plt.title(f"Decider with Rationality = {rationality}")
            plt.xlabel("Enforcer Rewards for Action 1")
            plt.ylabel("Enforcer Rewards for Action 0")
            plt.pcolormesh(posterior)

        # Integrate the inferred rewards of the enforcer.
        decider_reward = decider_reward + cooperative_reward(enforcer_rewards,
            posterior, method, cooperation)

    # Compute the utilities.
    decider_cost = np.array(NATURAL_COST) \
        + (DECIDER_COST_RATIO*enforcer_action)
    U = decider_reward - decider_cost

    # Compute the action probabilities.
    action_probabilities = softmax(U, rationality)

    return action_probabilities

def enforcer(rationality, enforcer_reward, reward_assumptions=[], ToM=0.0,
        method="", cooperation=0.0, plot=False):
    # Generate possible decider rewards and enforcer actions, taking into
    # account any potential assumptions the enforcer may have about decider
    # rewards.
    if len(reward_assumptions) == 0:
        decider_rewards = np.array(list(it.product(np.arange(MAX_REWARD),
            repeat=NUM_ACTIONS)))
    elif np.size(reward_assumptions) == NUM_ACTIONS:
        decider_rewards = np.array([reward_assumptions])
    else:
        decider_rewards = np.array(reward_assumptions)
    enforcer_actions = np.array(list(it.product(np.arange(MAX_ACTION),
        repeat=NUM_ACTIONS)))

    # Set up the utility space.
    space = [MAX_ACTION for action in range(NUM_ACTIONS)]
    U = np.zeros(space)

    # Compute the utilities.
    if CACHE == True:
        U = load_decider(rationality, enforcer_reward, decider_rewards,
            enforcer_actions, ToM, method, cooperation, U)
    else:
        U_decider_no_ToM = np.zeros(space)
        U_decider_ToM = np.zeros(space)
        temp_decider_no_ToM = np.zeros(space)
        temp_decider_ToM = np.zeros(space)
        for decider_reward in decider_rewards:
            for enforcer_action in enforcer_actions:
                # Reason about an decider without a ToM.
                if ToM != 1.0:
                    decider_action_probabilities = decider(rationality,
                        decider_reward, enforcer_action)
                    expected_enforcer_reward = np.dot(enforcer_reward,
                        decider_action_probabilities)
                    temp_decider_no_ToM[tuple(enforcer_action)] = \
                        expected_enforcer_reward \
                        - (ENFORCER_COST_RATIO*sum(enforcer_action))

                # Reason about an decider with a ToM.
                if ToM != 0.0:
                    decider_action_probabilities = decider(rationality,
                        decider_reward, enforcer_action, ToM=True,
                        method=method, cooperation=cooperation)
                    expected_enforcer_reward = np.dot(enforcer_reward,
                        decider_action_probabilities)
                    temp_decider_ToM[tuple(enforcer_action)] = \
                        expected_enforcer_reward \
                        - (ENFORCER_COST_RATIO*sum(enforcer_action))
            U_decider_no_ToM = U_decider_no_ToM + temp_decider_no_ToM
            U_decider_ToM = U_decider_ToM + temp_decider_ToM
        U_decider_no_ToM = U_decider_no_ToM / len(decider_rewards)
        U_decider_ToM = U_decider_ToM / len(decider_rewards)
        U = ((1.0-ToM)*U_decider_no_ToM) + (ToM*U_decider_ToM)

    # Compute the action probabilities.
    action_probabilities = softmax(U.flatten(), rationality).reshape(space)

    # Plot the posterior over enforcer actions.
    if plot == True:
        plt.figure()
        plt.title(f"Enforcer with Rationality = {rationality}")
        plt.xlabel("Enforcer Action Probability for Action 1")
        plt.ylabel("Enforcer Action Probability for Action 0")
        plt.pcolormesh(action_probabilities)

    return action_probabilities

def observer(infer, rationality, enforcer_action, enforcer_reward=[], ToM=0.0,
        method="", cooperation=0.0, plot=False):
    # Infer the enforcer's reward.
    if infer == "enforcer_reward":
        # Generate possible enforcer rewards.
        enforcer_rewards = np.array(list(it.product(np.arange(MAX_REWARD),
            repeat=NUM_ACTIONS)))

        # Set up the likelihood space.
        space = [MAX_REWARD for action in np.arange(NUM_ACTIONS)]
        likelihood = np.zeros(space)

        # Compute the likelihood.
        if CACHE == True:
            likelihood = load_enforcer(infer, rationality, enforcer_action,
                enforcer_rewards, likelihood, ToM=ToM, method=method,
                cooperation=cooperation)
        else:
            for enforcer_reward in enforcer_rewards:
                enforcer_action_probabilities = enforcer(rationality,
                    enforcer_reward, ToM=ToM, method=method,
                    cooperation=cooperation)
                likelihood[tuple(enforcer_reward)] = \
                    enforcer_action_probabilities[tuple(enforcer_action)]

        # Normalize the likelihood to generate the posterior.
        likelihood = likelihood.flatten()
        if sum(likelihood) == 0:
            posterior = likelihood.reshape(space)
        else:
            posterior = (likelihood/sum(likelihood)).reshape(space)

        # Plot the posterior over enforcer rewards.
        if plot == True:
            plt.figure()
            plt.title(f"Observer with Rationality = {rationality}")
            plt.xlabel("Enforcer Rewards for Action 1")
            plt.ylabel("Enforcer Rewards for Action 0")
            plt.pcolormesh(posterior)

    # Infer the enforcer's belief about the degree of ToM of deciders.
    elif infer == "ToM":
        # Generate possible degrees of ToM.
        ToM_set = np.round(np.linspace(0.0, 1.0, num=11), decimals=1)

        # Set up the space of possible proportion parameters and the
        # likelihood space.
        space = len(ToM_set)
        likelihood = np.zeros(space)

        # Compute the likelihood.
        if CACHE == True:
            likelihood = load_enforcer(infer, rationality, enforcer_action,
                ToM_set, likelihood, enforcer_reward=enforcer_reward,
                method=method, cooperation=cooperation)
        else:
            for t in np.arange(len(ToM_set)):
                enforcer_action_probabilities = enforcer(rationality,
                    enforcer_reward, ToM=ToM_set[t], method=method,
                    cooperation=cooperation)
                likelihood[t] = \
                    enforcer_action_probabilities[tuple(enforcer_action)]

        # Normalize the likelihood to generate the posterior.
        if sum(likelihood) == 0:
            posterior = likelihood
        else:
            posterior = likelihood / sum(likelihood)

        # Plot the posterior over the enforcer's belief about decider ToM.
        if plot == True:
            plt.figure()
            plt.title(f"Observer with Rationality = {rationality}")
            plt.xlabel("ToM")
            plt.ylabel("Enforcer Belief of Decider ToM")
            plt.plot(ToM_set, posterior)

    # Infer the enforcer's beliefs about the cooperativeness of deciders.
    elif infer == "cooperation":
        # Generate possible degrees of cooperativeness.
        cooperation_set = {
            "confidence": np.round(np.linspace(-25.0, 25.0, num=11),
                decimals=1),
            "preference": np.round(np.linspace(-25.0, 25.0, num=11),
                decimals=1),
            "proportional": np.round(np.linspace(-2.5, 2.5, num=11),
                decimals=1)
        }[method]

        # Set up the space of possible cooperation parameters and the
        # likelihood space.
        space = len(cooperation_set)
        likelihood = np.zeros(space)

        # Compute the likelihood.
        if CACHE == True:
            likelihood = load_enforcer(infer, rationality, enforcer_action,
                cooperation_set, likelihood, enforcer_reward=enforcer_reward,
                ToM=ToM, method=method)
        else:
            for c in np.arange(len(cooperation_set)):
                enforcer_action_probabilities = enforcer(rationality,
                    enforcer_reward, ToM=ToM, method=method,
                    cooperation=cooperation_set[c])
                likelihood[c] = \
                    enforcer_action_probabilities[tuple(enforcer_action)]

        # Normalize the likelihood to generate the posterior.
        if sum(likelihood) == 0:
            posterior = likelihood
        else:
            posterior = likelihood / sum(likelihood)

        # Plot the posterior over the enforcer's belief about decider
        # cooperativeness.
        if plot == True:
            plt.figure()
            plt.title(f"Observer with Rationality = {rationality}")
            plt.xlabel("Cooperation")
            plt.ylabel("Enforcer Belief of Decider Cooperation")
            plt.plot(cooperation_set, posterior)

    # Infer the enforcer's belief of the reward of deciders.
    if infer == "decider_reward":
        # Generate possible decider rewards.
        decider_rewards = np.array(list(it.product(np.arange(MAX_REWARD),
            repeat=NUM_ACTIONS)))

        # Set up the likelihood space.
        space = [MAX_REWARD for action in np.arange(NUM_ACTIONS)]
        likelihood = np.zeros(space)

        # Compute the likelihood.
        if CACHE == True:
            likelihood = load_enforcer(infer, rationality,
                enforcer_action, decider_rewards, likelihood,
                enforcer_reward=enforcer_reward, ToM=ToM, method=method,
                cooperation=cooperation)
        else:
            for decider_reward in decider_rewards:
                enforcer_action_probabilities = enforcer(rationality,
                    enforcer_reward, reward_assumptions=decider_reward,
                    ToM=ToM, method=method, cooperation=cooperation)
                likelihood[tuple(decider_reward)] = \
                    enforcer_action_probabilities[tuple(enforcer_action)]

        # Normalize the likelihood to generate the posterior.
        likelihood = likelihood.flatten()
        if sum(likelihood) == 0:
            posterior = likelihood.reshape(space)
        else:
            posterior = (likelihood/sum(likelihood)).reshape(space)

        # Plot the posterior over the enforcer's belief about decider rewards.
        if plot == True:
            plt.figure()
            plt.title(f"Observer with Rationality = {rationality}")
            plt.xlabel("Enforcer Belief of Decider Rewards for Option 1")
            plt.ylabel("Enforcer Belief of Decider Rewards for Option 0")
            plt.pcolormesh(posterior)

    # Infer the enforcer's joint belief about the reward and degree of ToM of
    # deciders.
    elif infer == "decider_reward_and_ToM":
        # Generate possible decider rewards and degrees of ToM.
        decider_rewards = np.array(list(it.product(np.arange(MAX_REWARD),
            repeat=NUM_ACTIONS)))
        ToM_set = np.round(np.linspace(0.0, 1.0, num=11), decimals=1)

        # Set up the space of possible proportion parameters and the
        # likelihood space.
        space = [MAX_REWARD**NUM_ACTIONS, len(ToM_set)]
        likelihood = np.zeros(space)

        # Compute the likelihood.
        if CACHE == True:
            likelihood == load_enforcer(infer, rationality, enforcer_action,
                [decider_rewards, ToM_set], likelihood,
                enforcer_reward=enforcer_reward, method=method,
                cooperation=cooperation)
        else:
            for dr in np.arange(len(decider_rewards)):
                for t in np.arange(len(ToM_set)):
                    enforcer_action_probabilities = enforcer(rationality,
                        enforcer_reward,
                        reward_assumptions=decider_rewards[dr],
                        ToM=ToM_set[t], method=method,
                        cooperation=cooperation)
                    likelihood[dr][t] = \
                        enforcer_action_probabilities[tuple(enforcer_action)]

        # Normalize the likelihood to generate the posterior.
        likelihood = likelihood.flatten()
        if sum(likelihood) == 0:
            posterior = likelihood.reshape(space)
        else:
            posterior = (likelihood/sum(likelihood)).reshape(space)

        # Plot the posterior over the enforcer's joint belief about decider
        # rewards and ToM.
        if plot == True:
            plt.figure()
            plt.title(f"Observer with Rationality = {rationality}")
            plt.xlabel("Enforcer Belief of Decider ToM")
            plt.ylabel("Enforcer Belief of Decider Rewards")
            plt.pcolormesh(posterior)

    # Infer the enforcer's joint belief about the reward and cooperativeness
    # of deciders.
    elif infer == "decider_reward_and_cooperation":
        # Identify the hypothesis space.
        decider_rewards = np.array(list(it.product(np.arange(MAX_REWARD),
            repeat=NUM_ACTIONS)))
        cooperation_set = {
            "confidence": np.round(np.linspace(-25.0, 25.0, num=11),
                decimals=1),
            "preference": np.round(np.linspace(-25.0, 25.0, num=11),
                decimals=1),
            "proportional": np.round(np.linspace(-2.5, 2.5, num=11),
                decimals=1)
        }[method]

        # Set up the space of possible proportion parameters and the
        # likelihood space.
        space = [MAX_REWARD**NUM_ACTIONS, len(cooperation_set)]
        likelihood = np.zeros(space)

        # Compute the likelihood.
        if CACHE == True:
            likelihood == load_enforcer(infer, rationality, enforcer_action,
                [decider_rewards, cooperation_set], likelihood,
                enforcer_reward=enforcer_reward, ToM=ToM, method=method)
        else:
            for dr in np.arange(len(decider_rewards)):
                for c in np.arange(len(cooperation_set)):
                    enforcer_action_probabilities = enforcer(rationality,
                        enforcer_reward,
                        reward_assumptions=decider_rewards[dr],
                        ToM=ToM, method=method,
                        cooperation=cooperation_set[c])
                    likelihood[dr][c] = \
                        enforcer_action_probabilities[tuple(enforcer_action)]

        # Normalize the likelihood to generate the posterior.
        likelihood = likelihood.flatten()
        if sum(likelihood) == 0:
            posterior = likelihood.reshape(space)
        else:
            posterior = (likelihood/sum(likelihood)).reshape(space)

        # Plot the posterior over the enforcer's belief of decider
        # rewards and cooperativeness.
        if plot == True:
            plt.figure()
            plt.title(f"Observer with Rationality = {rationality}")
            plt.xlabel("Enforcer Belief of Decider Cooperation")
            plt.ylabel("Enforcer Belief of Decider Rewards")
            plt.pcolormesh(posterior)

    return posterior

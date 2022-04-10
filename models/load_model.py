import numpy as np
import pickle as pk
import time
import sys

from config import *

# Open up cache files here to reduce I/O overhead.
FILENAME = f"cache/{ENVIRONMENT}_decider_no_ToM_{DECIDER_COST_RATIO}_" \
    + f"{ENFORCER_COST_RATIO}_{NATURAL_COST[0]}_{NATURAL_COST[1]}.pkl"
try:
    start_time = time.time()
    DECIDER_NO_TOM = pk.load(open(FILENAME, "rb"))
    print("`decider_no_ToM` load time: %0.4f" % (time.time()-start_time))
except:
    pass

FILENAME = f"cache/{ENVIRONMENT}_enforcer_no_ToM_{DECIDER_COST_RATIO}_" \
    + f"{ENFORCER_COST_RATIO}_{NATURAL_COST[0]}_{NATURAL_COST[1]}.pkl"
try:
    start_time = time.time()
    ENFORCER_NO_TOM = pk.load(open(FILENAME, "rb"))
    print("`enforcer_no_ToM` load time: %0.4f" % (time.time()-start_time))
except:
    pass

FILENAME = f"cache/{ENVIRONMENT}_decider_ToM_{DECIDER_COST_RATIO}_" \
    + f"{ENFORCER_COST_RATIO}_{NATURAL_COST[0]}_{NATURAL_COST[1]}.pkl"
try:
    start_time = time.time()
    DECIDER_TOM = pk.load(open(FILENAME, "rb"))
    print("`decider_ToM` load time: %0.4f" % (time.time()-start_time))
except:
    pass

FILENAME = f"cache/{ENVIRONMENT}_enforcer_ToM_{DECIDER_COST_RATIO}_" \
    + f"{ENFORCER_COST_RATIO}_{NATURAL_COST[0]}_{NATURAL_COST[1]}.pkl"
try:
    start_time = time.time()
    ENFORCER_TOM = pk.load(open(PATH+FILENAME, "rb"))
    print("`enforcer_ToM` load time: %0.4f" % (time.time()-start_time))
except:
    pass

# Process the cached action probabilities for enforcers.
def load_decider(rationality, enforcer_reward, decider_rewards,
        enforcer_actions, ToM, method, cooperation, U):
    U_decider_no_ToM = np.zeros(U.shape)
    U_decider_ToM = np.zeros(U.shape)
    temp_decider_no_ToM = np.zeros(U.shape)
    temp_decider_ToM = np.zeros(U.shape)
    for decider_reward in decider_rewards:
        for enforcer_action in enforcer_actions:
            # Reason about a decider without a ToM.
            if ToM != 1.0:
                parameter_key = f"{rationality}_" \
                    + f"{'_'.join([str(num) for num in decider_reward])}_" \
                    + f"{'_'.join([str(num) for num in enforcer_action])}"
                action_probabilities = DECIDER_NO_TOM[parameter_key]
                expected_enforcer_reward = np.dot(enforcer_reward,
                    action_probabilities)
                temp_decider_no_ToM[tuple(enforcer_action)] = \
                    expected_enforcer_reward \
                    - (ENFORCER_COST_RATIO*sum(enforcer_action))

            # Reason about a decider with a ToM.
            if ToM != 0.0:
                parameter_key = f"{rationality}_{method}_{cooperation}_" \
                    + f"{'_'.join([str(num) for num in decider_reward])}_" \
                    + f"{'_'.join([str(num) for num in enforcer_action])}"
                action_probabilities = DECIDER_TOM[parameter_key]
                expected_enforcer_reward = np.dot(enforcer_reward,
                    action_probabilities)
                temp_decider_ToM[tuple(enforcer_action)] = \
                    expected_enforcer_reward \
                    - (ENFORCER_COST_RATIO*sum(enforcer_action))
        U_decider_no_ToM = U_decider_no_ToM + temp_decider_no_ToM
        U_decider_ToM = U_decider_ToM + temp_decider_ToM
    U_decider_no_ToM = U_decider_no_ToM / len(decider_rewards)
    U_decider_ToM = U_decider_ToM / len(decider_rewards)
    U = ((1.0-ToM)*U_decider_no_ToM) + (ToM*U_decider_ToM)

    return U

# Process the cached action probabilities for enforcers.
def load_enforcer(infer, rationality, enforcer_action, hypothesis_space,
        likelihood, enforcer_reward=[], ToM=0.0, method="", cooperation=0.0):
    # Infer the enforcer's reward.
    if infer == "enforcer_reward":
        # Identify the hypothesis space.
        enforcer_rewards = hypothesis_space

        # Find the enforcer's action probabilities for each enforcer reward.
        for enforcer_reward in enforcer_rewards:
            if ToM == 0.0:
                parameter_key = f"{rationality}_" \
                    + f"{'_'.join([str(num) for num in enforcer_reward])}"
                action_probabilities = ENFORCER_NO_TOM[parameter_key]
            else:
                parameter_key = f"{rationality}_{ToM}_{method}_" \
                    + f"{cooperation}_" \
                    + f"{'_'.join([str(num) for num in enforcer_reward])}"
                action_probabilities = ENFORCER_TOM[parameter_key]
            likelihood[tuple(enforcer_reward)] = \
                action_probabilities[tuple(enforcer_action)]

    # Infer the enforcer's belief about the degree of ToM of deciders.
    if infer == "ToM":
        # Identify the hypothesis space.
        ToM_set = hypothesis_space

        # Find the enforcer's action probabilities for each degree of ToM.
        for t in np.arange(len(ToM_set)):
            parameter_key = f"{rationality}_{ToM_set[t]}_{method}_" \
                + f"{cooperation}_" \
                + f"{'_'.join([str(num) for num in enforcer_reward])}"
            action_probabilities = ENFORCER_TOM[parameter_key]
            likelihood[t] = action_probabilities[tuple(enforcer_action)]

    # Infer the enforcer's belief about the cooperativeness of deciders.
    elif infer == "cooperation":
        # Identify the hypothesis space.
        cooperation_set = hypothesis_space

        # Find the enforcer's action probabilities for each degree of
        # cooperation.
        for c in np.arange(len(cooperation_set)):
            parameter_key = f"{rationality}_{ToM}_{method}_" \
                + f"{cooperation_set[c]}_" \
                + f"{'_'.join([str(num) for num in enforcer_reward])}"
            action_probabilities = ENFORCER_TOM[parameter_key]
            likelihood[c] = action_probabilities[tuple(enforcer_action)]

    # Infer the enforcer's belief about the reward of deciders.
    elif infer == "decider_reward":
        # Identify the hypothesis space.
        decider_rewards = hypothesis_space

        # Find the enforcer's action probabilities for each decider reward.
        for decider_reward in decider_rewards:
            parameter_key = f"{rationality}_{ToM}_{method}_" \
                + f"{cooperation}_" \
                + f"{'_'.join([str(num) for num in decider_reward])}_" \
                + f"{'_'.join([str(num) for num in enforcer_reward])}"
            action_probabilities = ENFORCER_TOM[parameter_key]
            likelihood[tuple(decider_reward)] = \
                action_probabilities[tuple(enforcer_action)]

    # Infer the enforcer's joint belief about the reward and degree of ToM of
    # deciders.
    elif infer == "decider_reward_and_ToM":
        # Identify the hypothesis space.
        decider_rewards = hypothesis_space[0]
        ToM_set = hypothesis_space[1]

        # Find the enforcer's action probabilities for each decider reward and
        # degree of ToM.
        for dr in np.arange(len(decider_rewards)):
            for t in np.arange(len(ToM_set)):
                parameter_key = f"{rationality}_{ToM_set[t]}_{method}_" \
                    + f"{cooperation}_" \
                    + "_".join([str(num) for num in decider_rewards[dr]]) \
                    + "_" \
                    + "_".join([str(num) for num in enforcer_reward])
                action_probabilities = ENFORCER_TOM[parameter_key]
                likelihood[dr][t] = \
                    action_probabilities[tuple(enforcer_action)]

    # Infer the enforcer's joint belief about the reward and cooperativeness
    # of deciders.
    elif infer == "decider_reward_and_cooperation":
        # Identify the hypothesis space.
        decider_rewards = hypothesis_space[0]
        cooperation_set = hypothesis_space[1]

        # Find the enforcer's action probabilities for each decider reward and
        # degree of cooperation.
        for dr in np.arange(len(decider_rewards)):
            for c in np.arange(len(cooperation_set)):
                parameter_key = f"{rationality}_{ToM}_{method}_" \
                    + f"{cooperation_set[c]}_" \
                    + "_".join([str(num) for num in decider_rewards[dr]]) \
                    + "_" \
                    + "_".join([str(num) for num in enforcer_reward])
                action_probabilities = ENFORCER_TOM[parameter_key]
                likelihood[dr][c] = \
                    action_probabilities[tuple(enforcer_action)]

    return likelihood

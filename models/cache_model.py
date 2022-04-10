import itertools as it
import numpy as np
import pickle as pk
import time

from agents import *

# Cache the action probabilities for a decider without a ToM.
def cache_decider_no_ToM(rationality_set, decider_rewards, enforcer_actions):
    # Define the filename of the cached data.
    filename = f"cache/{ENVIRONMENT}_decider_no_ToM_{DECIDER_COST_RATIO}_" \
        + f"{ENFORCER_COST_RATIO}_{NATURAL_COST[0]}_{NATURAL_COST[1]}.pkl"

    # Cache the action probabilities for this decider over the parameter set.
    cached_data = {}
    for rationality in rationality_set:
        for decider_reward in decider_rewards:
            for enforcer_action in enforcer_actions:
                parameter_key = f"{rationality}_" \
                    + f"{'_'.join([str(num) for num in decider_reward])}_" \
                    + f"{'_'.join([str(num) for num in enforcer_action])}"
                action_probabilities = decider(rationality, decider_reward,
                    enforcer_action)
                cached_data[parameter_key] = action_probabilities
    pk.dump(cached_data, open(filename, "wb"))

# Cache the action probabilities for an enforcer reasoning about a decider
# without a ToM.
def cache_enforcer_no_ToM(rationality_set, enforcer_rewards):
    # Define the filename of the cached data.
    filename = f"cache/{ENVIRONMENT}_enforcer_no_ToM_{DECIDER_COST_RATIO}_" \
        + f"{ENFORCER_COST_RATIO}_{NATURAL_COST[0]}_{NATURAL_COST[1]}.pkl"

    # Cache the action probabilities for this enforcer over the parameter set.
    cached_data = {}
    for rationality in rationality_set:
        for enforcer_reward in enforcer_rewards:
            parameter_key = f"{rationality}_" \
                + f"{'_'.join([str(num) for num in enforcer_reward])}"
            action_probabilities = enforcer(rationality, enforcer_reward)
            cached_data[parameter_key] = action_probabilities
    pk.dump(cached_data, open(filename, "wb"))

# Cache the action probabilities for a decider with a ToM.
def cache_decider_ToM(rationality_set, decider_rewards, enforcer_actions,
        cooperative_methods):
    # Define the filename of the cached data.
    filename = f"cache/{ENVIRONMENT}_decider_ToM_{DECIDER_COST_RATIO}_" \
        + f"{ENFORCER_COST_RATIO}_{NATURAL_COST[0]}_{NATURAL_COST[1]}.pkl"

    # Cache the action probabilities for this decider over the parameter set.
    cached_data = {}
    for rationality in rationality_set:
        for method in cooperative_methods.keys():
            for cooperation in cooperative_methods[method]:
                for decider_reward in decider_rewards:
                    for enforcer_action in enforcer_actions:
                        parameter_key = f"{rationality}_{method}_" \
                            + f"{cooperation}_" \
                            + "_".join([str(num) for num in decider_reward]) \
                            + "_" \
                            + "_".join([str(num) for num in enforcer_action])
                        action_probabilities = decider(rationality,
                            decider_reward, enforcer_action, ToM=True,
                            method=method, cooperation=cooperation)
                        cached_data[parameter_key] = action_probabilities
    pk.dump(cached_data, open(filename, "wb"))

# Cache the action probabilities for an enforcer reasoning about a decider
# with a ToM (with reward assumptions).
def cache_enforcer_ToM(rationality_set, enforcer_rewards, decider_rewards,
        ToM_set, cooperative_methods):
    # Define the filename of the cached data.
    filename = f"cache/{ENVIRONMENT}_enforcer_ToM_{DECIDER_COST_RATIO}_" \
        + f"{ENFORCER_COST_RATIO}_{NATURAL_COST[0]}_{NATURAL_COST[1]}.pkl"

    # Cache the action probabilities for this enforcer over the parameter set.
    cached_data = {}
    for rationality in rationality_set:
        for ToM in ToM_set:
            for method in cooperative_methods.keys():
                for cooperation in cooperative_methods[method]:
                    for decider_reward in decider_rewards:
                        for enforcer_reward in enforcer_rewards:
                            parameter_key = f"{rationality}_{ToM}_{method}_" \
                                + f"{cooperation}_" \
                                + "_".join([str(num) \
                                    for num in decider_reward]) \
                                + "_" \
                                + "_".join([str(num) \
                                    for num in enforcer_reward])
                            action_probabilities = enforcer(rationality,
                                enforcer_reward,
                                reward_assumptions=decider_reward, ToM=ToM,
                                method=method, cooperation=cooperation)
                            cached_data[parameter_key] = action_probabilities
    pk.dump(cached_data, open(filename, "wb"))

# Populate the cache with selected models.
def main(model_selection):
    # Set up the rationality set.
    rationality_set = np.array([0.1, 1.0])

    # Set up the range of ToM that deciders can have.
    ToM_set = np.round(np.linspace(0.0, 1.0, num=11), decimals=1)

    # Set up the ways in which deciders can integrate social reward.
    cooperative_methods = {
        "confidence": np.round(np.linspace(-25.0, 25.0, num=11), decimals=1),
        "preference": np.round(np.linspace(-25.0, 25.0, num=11), decimals=1),
        "proportional": np.round(np.linspace(-2.5, 2.5, num=11), decimals=1)
    }

    # Set up the hypothesis spaces.
    decider_rewards = np.array(list(it.product(np.arange(MAX_REWARD),
        repeat=NUM_ACTIONS)))
    enforcer_actions = np.array(list(it.product(np.arange(MAX_ACTION),
        repeat=NUM_ACTIONS)))
    enforcer_rewards = np.array(list(it.product(np.arange(MAX_REWARD),
        repeat=NUM_ACTIONS)))

    # Cache the `decider_no_ToM` model.
    if model_selection[0] == "1":
        start_time = time.time()
        cache_decider_no_ToM(rationality_set, decider_rewards,
            enforcer_actions)
        print("`decider_no_ToM` cache time: %0.4f"
            % (time.time()-start_time))

    # Cache the `enforcer_no_ToM` model.
    if model_selection[1] == "1":
        start_time = time.time()
        cache_enforcer_no_ToM(rationality_set, enforcer_rewards)
        print("`enforcer_no_ToM` cache time: %0.4f"
            % (time.time()-start_time))

    # Cache the `decider_ToM` model.
    if model_selection[2] == "1":
        start_time = time.time()
        cache_decider_ToM(rationality_set, decider_rewards, enforcer_actions,
            cooperative_methods)
        print("`decider_ToM` cache time: %0.4f"
            % (time.time()-start_time))

    # Cache the `enforcer_ToM` model (with reward assumptions).
    if model_selection[3] == "1":
        start_time = time.time()
        cache_enforcer_ToM(rationality_set, enforcer_rewards, decider_rewards,
            ToM_set, cooperative_methods)
        print("`enforcer_ToM` cache time: %0.4f"
            % (time.time()-start_time))

if __name__ == "__main__":
    main(sys.argv[3])

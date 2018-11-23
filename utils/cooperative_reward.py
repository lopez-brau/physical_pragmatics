import numpy as np

from .config import *

def cooperative_reward(enforcer_rewards, reward_probabilities, method, cooperation):
    
    # The "confidence" method computes the probabilities of each enforcer 
    # action being the optimal one.
    if method == "confidence":
        inferred_enforcer_reward = np.zeros(NUM_ACTIONS)
        for enforcer_reward in enforcer_rewards:
            enforcer_preference = (max(enforcer_reward) == enforcer_reward) + 0.0
            if sum(enforcer_preference) == NUM_ACTIONS:
                continue
            elif sum(enforcer_preference) > 1.0:
                enforcer_preference /= sum(enforcer_preference)
            inferred_enforcer_reward = inferred_enforcer_reward + \
                                       (reward_probabilities[tuple(enforcer_reward)]*enforcer_preference)
        return cooperation * inferred_enforcer_reward

    # The "flat" method computes the expected enforcer rewards and infers that
    # the max of those rewards is the enforcer's preference.
    elif method == "preference":
        expected_enforcer_rewards = np.zeros(NUM_ACTIONS)
        for enforcer_reward in enforcer_rewards:
            expected_enforcer_rewards = expected_enforcer_rewards + \
                                        (reward_probabilities[tuple(enforcer_reward)]*enforcer_reward)
        expected_enforcer_preference = (max(expected_enforcer_rewards) == expected_enforcer_rewards) + 0.0
        if sum(expected_enforcer_preference) == NUM_ACTIONS:
            expected_enforcer_preference = np.zeros(NUM_ACTIONS)
        elif sum(expected_enforcer_preference) > 1.0:
            expected_enforcer_preference /= sum(expected_enforcer_preference)
        return cooperation * expected_enforcer_preference

    # The "proportional" method computes the expected enforcer's rewards.
    elif method == "proportional":
        expected_enforcer_rewards = np.zeros(NUM_ACTIONS)
        for enforcer_reward in enforcer_rewards:
            expected_enforcer_rewards = expected_enforcer_rewards + \
                                        (reward_probabilities[tuple(enforcer_reward)]*enforcer_reward)
        return cooperation * expected_enforcer_rewards

    # Throw an error if there's a typo in the method type.
    else:
        print("Invalid method.")
        return

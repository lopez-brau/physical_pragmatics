from .config import *

import numpy as np

def cooperative_reward(enforcer_rewards, reward_probabilities, method, cooperation):
    inferred_enforcer_action = np.zeros(NUM_ACTIONS)

    # The "confidence" method computes the probabilities of each enforcer 
    # action being the optimal one.
    if method == "confidence":
        for enforcer_reward in enforcer_rewards:
            optimal_enforcer_action = (max(enforcer_reward) == enforcer_reward) + 0.0
            inferred_enforcer_action = inferred_enforcer_action + \
                                       (reward_probabilities[tuple(enforcer_reward)]*optimal_enforcer_action)

    # The "flat" method computes the expected enforcer rewards and infers that
    # the max of those rewards is the optimal enforcer action.
    elif method == "flat":
        expected_enforcer_rewards = np.zeros(NUM_ACTIONS)
        for enforcer_reward in enforcer_rewards:
            expected_enforcer_rewards = expected_enforcer_rewards + \
                                        (reward_probabilities[tuple(enforcer_reward)]*enforcer_reward)
        inferred_enforcer_action = (max(expected_enforcer_rewards) == expected_enforcer_rewards) + 0.0

    # The "proportional" method computes the expected enforcer rewards.
    elif method == "proportional":
        expected_enforcer_rewards = np.zeros(NUM_ACTIONS)
        for enforcer_reward in enforcer_rewards:
            expected_enforcer_rewards = expected_enforcer_rewards + \
                                        (reward_probabilities[tuple(enforcer_reward)]*enforcer_reward)
        inferred_enforcer_action = expected_enforcer_rewards

    # Throw an error if there's a typo in the method type.
    else:
        print("Invalid method.")
        return

    return cooperation * inferred_enforcer_action

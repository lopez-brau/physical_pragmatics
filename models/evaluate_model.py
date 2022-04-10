import csv
import itertools as it
import numpy as np
import sys

from agents import *

def evaluate_decider(rationality_set, decider_rewards, enforcer_actions,
        ToM_set, method, cooperative_methods):
    # Define the filename of the model predictions.
    filename = f"data/model/{ENVIRONMENT}_decider_{DECIDER_COST_RATIO}_" \
        + f"{ENFORCER_COST_RATIO}_{NATURAL_COST[0]}_{NATURAL_COST[1]}.csv"

    # Evaluate and write the model predictions.
    with open(filename, "w") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(["rationality", "decider_reward_0",
            "decider_reward_1", "enforcer_action_0", "enforcer_action_1",
            "enforcer_action_0", "enforcer_action_1", "ToM", "method",
            "cooperation"])
        for rationality in rationality_set:
            for ToM in ToM_set:
                for method in cooperative_methods.keys():
                    for cooperation in cooperative_methods[method]:
                        for decider_reward in decider_rewards:
                            for enforcer_action in enforcer_actions:
                                # Evaluate the enforcer model for deciders
                                # without a ToM.
                                if ToM == 0.0:
                                    parameter_key = f"{rationality}_" \
                                        + "_".join([str(num)
                                            for num in decider_reward]) \
                                        + "_" \
                                        + "_".join([str(num)
                                            for num in enforcer_action])
                                    action_probabilities = \
                                        DECIDER_NO_TOM[parameter_key]

                                # Evaluate the enforcer model for deciders
                                # with a ToM.
                                else:
                                    parameter_key = f"{rationality}_" \
                                        + f"{method}_{cooperation}_" \
                                        + "_".join([str(num)
                                            for num in decider_reward]) \
                                        + "_" \
                                        + "_".join([str(num)
                                            for num in enforcer_action])
                                    action_probabilities = \
                                        DECIDER_TOM[parameter_key]

                                # Write the model predictions to a csv.
                                writer.writerow([rationality,
                                    decider_reward[0], decider_reward[1],
                                    action_probabilities[0],
                                    action_probabilities[1],
                                    enforcer_action[0], enforcer_action[1],
                                    ToM, method, cooperation])

def evaluate_enforcer(rationality_set, decider_rewards, enforcer_rewards,
        ToM_set, method, cooperative_methods):
    # Define the filename of the model predictions.
    filename = f"data/model/{ENVIRONMENT}_enforcer_{DECIDER_COST_RATIO}_" \
        + f"{ENFORCER_COST_RATIO}_{NATURAL_COST[0]}_{NATURAL_COST[1]}.csv"

    # Evaluate and write the model predictions.
    with open(filename, "w") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(["rationality", "decider_reward_0",
            "decider_reward_1", "enforcer_action_0", "enforcer_action_1",
            "enforcer_reward_0", "enforcer_reward_1", "ToM", "method",
            "cooperation"])
        for rationality in rationality_set:
            for ToM in ToM_set:
                for method in cooperative_methods.keys():
                    for cooperation in cooperative_methods[method]:
                        for decider_reward in decider_rewards:
                            for enforcer_reward in enforcer_rewards:
                                # Evaluate the enforcer model.
                                parameter_key = f"{rationality}_{ToM}_" \
                                    + f"{method}_{cooperation}_" \
                                    + "_".join([str(num)
                                        for num in decider_reward]) \
                                    + "_" \
                                    + "_".join([str(num)
                                        for num in enforcer_reward])
                                action_probabilities = \
                                    ENFORCER_TOM[parameter_key]

                                # Write the model predictions.
                                writer.writerow([rationality,
                                    decider_reward[0], decider_reward[1],
                                    np.argmax(action_probabilities[:, 0]),
                                    np.argmax(action_probabilities[0, :]),
                                    enforcer_reward[0], enforcer_reward[1],
                                    ToM, method, cooperation])

def evaluate_observer(rationality, enforcer_actions, enforcer_reward, ToM,
        method, cooperative_methods):
    # Define the filename of the model predictions.
    filename = f"data/observer_0/model/{ENVIRONMENT}_observer_" \
        + f"{DECIDER_COST_RATIO}_{ENFORCER_COST_RATIO}_" \
        + f"{NATURAL_COST[0]}_{NATURAL_COST[1]}.csv"

    # Evaluate and write the model predictions for each condition.
    with open(filename, "w") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(["natural_cost", "rationality", "enforcer_reward",
            "enforcer_action", "model_reward_0", "model_cooperation",
            "model_reward_1"])

        # Evaluate the model for each enforcer action.
        for enforcer_action in enforcer_actions:
            # Evaluate the observer model for the agentive condition.
            posterior = observer("decider_reward_and_cooperation",
                rationality, enforcer_action=enforcer_action,
                enforcer_reward=enforcer_reward, ToM=ToM, method=method)

            # Compute marginals and expectations.
            posterior = posterior.reshape(MAX_REWARD, MAX_REWARD,
                cooperative_methods[method].size)
            P_pomegranate = np.sum(posterior, axis=(1, 2))
            P_pear = np.sum(posterior, axis=(0, 2))
            P_cooperation = np.sum(posterior, axis=(0, 1))
            E_pomegranate = np.sum(np.multiply(P_pomegranate,
                np.arange(MAX_REWARD)))
            E_pear = np.sum(np.multiply(P_pear, np.arange(MAX_REWARD)))
            E_cooperation = np.sum(np.multiply(P_cooperation,
                cooperative_methods[method]))
            model_reward_0 = E_pomegranate
            model_cooperation = E_cooperation

            # Evaluate the observer model for the non-agentive condition.
            posterior = observer("decider_reward", rationality,
                enforcer_action=enforcer_action,
                enforcer_reward=enforcer_reward, ToM=ToM, method=method)

            # Compute marginals and expectations.
            posterior = posterior.reshape(MAX_REWARD, MAX_REWARD)
            P_pomegranate = np.sum(posterior, axis=(1))
            P_pear = np.sum(posterior, axis=(0))
            E_pomegranate = np.sum(np.multiply(P_pomegranate,
                np.arange(MAX_REWARD)))
            E_pear = np.sum(np.multiply(P_pear, np.arange(MAX_REWARD)))
            model_reward_1 = E_pomegranate

            # Write the model predictions.
            writer.writerow([str(np.array(NATURAL_COST)), rationality,
                str(enforcer_reward), str(enforcer_action), model_reward_0,
                model_cooperation, model_reward_1])

def main(model_selection):
    # Set up the rationality set.
    rationality_set = np.array([0.1, 1.0])

    # Set up the range of ToM that agents can have.
    ToM_set = np.round(np.linspace(0.0, 1.0, num=11), decimals=1)

    # Set up the ways in which agents can integrate social reward.
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

    if model_selection == "decider":
        # Define the parameters for evaluating the decider model.
        rationality_set = np.array([0.1, 1.0])
        ToM_set = np.array([0.0, 1.0])
        method = "confidence"

        # Evaluate the decider model.
        evaluate_decider(rationality_set, decider_rewards, enforcer_actions,
            ToM_set, method, cooperative_methods)

    if model_selection == "enforcer":
        # Define the parameters for evaluating the enforcer model.
        rationality_set = np.array([0.1, 1.0])
        ToM_set = np.array([0.0, 1.0])
        method = "confidence"

        # Evaluate the enforcer model.
        evaluate_enforcer(rationality_set, decider_rewards, enforcer_rewards,
            ToM_set, method, cooperative_methods)

    if model_selection == "observer":
        # Define the parameters for evaluating the observer model.
        rationality = 1.0
        enforcer_actions = np.array([[1, 0], [2, 0], [3, 0]])
        enforcer_reward = np.array([0, 9])
        ToM = 1.0
        method = "confidence"

        # Evaluate the observer model.
        evaluate_observer(rationality, enforcer_actions, enforcer_reward, ToM,
            method, cooperative_methods)

if __name__ == "__main__":
    main(sys.argv[3])

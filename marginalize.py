from utils import *

import csv
import itertools as it
import matplotlib.pyplot as plt
import numpy as np

# def marginalize():



natural_costs = np.array(list(it.product(np.arange(3), repeat=NUM_ACTIONS)))
enforcer_actions = np.array([[0, 0], [1, 0], [2, 0]])
path = "predictions/plots/gridworld_nc_distance_3/"
cooperation = 2.0
for natural_cost in natural_costs:
    for enforcer_action in enforcer_actions:
        filename = path + str(cooperation) + "/" + str(natural_cost) + "_" + str(enforcer_action) + ".txt"
        with open(filename, "r") as file:
            reader = csv.reader(file)
            data = []
            for row in reader:
                data.append([float(num) for num in row])
            data = np.array(data).reshape(MAX_VALUE, MAX_VALUE, 11)
            prob_A = np.sum(data, axis=(1, 2))
            prob_B = np.sum(data, axis=(0, 2))
            prob_p = np.sum(data, axis=(0, 1))
            expected_A = np.sum(np.multiply(prob_A, np.arange(10)))
            expected_B = np.sum(np.multiply(prob_B, np.arange(10)))
            expected_p = np.sum(np.multiply(prob_p, np.arange(11)/10))
            print("===== Natural Cost = %s, Enforcer Action = %s =====" % (str(natural_cost), str(enforcer_action)))
            print("E[A] = ", expected_A)
            print("E[B] = ", expected_B)
            print("E[p] = ", expected_p)
            # plt.figure()
            # plt.title("Agent Reward A")
            # plt.ylabel("Probability")
            # plt.xlabel("Value")
            # plt.plot(np.arange(prob_A.size), prob_A)
            # plt.figure()
            # plt.title("Agent Reward B")
            # plt.ylabel("Probability")
            # plt.xlabel("Value")
            # plt.plot(np.arange(prob_B.size), prob_B)
            # plt.figure()
            # plt.title("ToM")
            # plt.ylabel("Probability")
            # plt.xlabel("Value")
            # plt.plot(np.arange(prob_p.size)/10, prob_p)
            # plt.savefig("imgs/test_2/" + str(natural_cost) + "_" + str(enforcer_action) + "_prob.png", bbox_inches="tight")
            # plt.close()

            fig, axs = plt.subplots(1, 2, gridspec_kw={'width_ratios':[2, 1]}, sharey=False)
            fig.subplots_adjust(wspace=.35)
            axs[0].bar(["A", "B"], [expected_A, expected_B])
            axs[0].set_ylim(0, 9)
            axs[0].set_ylabel("E[Reward Value]")
            axs[1].bar(["p"], [expected_p])
            axs[1].set_ylim(0.0, 1.0)
            axs[1].set_ylabel("E[P(ToM)]")
            fig.suptitle("Enforcer Action = %s" % str(enforcer_action))
            plt.savefig("imgs/3/2.0/" + str(natural_cost) + "_" + str(enforcer_action) + ".png", bbox_inches="tight")
            plt.close(fig)
        # break
    # break

# plt.figure()
# plt.pcolor(data.T[3])
# print(data.T[3])
# plt.show()
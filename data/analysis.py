import csv
import json
import matplotlib.pyplot as plt
import numpy as np

with open("D:/Research/social_pragmatics/data/trini.json", "r") as file:
    data = json.load(file)

fig, ax = plt.subplots()
fig1, ax1 = plt.subplots()
# fig2, ax2 = plt.subplots()

trials = data["trials"]
x, y = [], []
annotations, natural_costs, enforcer_actions = [], [], []
expected_A, expected_B, expected_p = [], [], []

for trial in trials:
    if trial["target_1"] < 0.1:
    # if trial["target1"] < 0.1:
        print(trial["filename"])
        # print(trial["stimulus"])
        continue
    x.append(trial["target_0"]*10)
    # x.append(trial["target0"]*10)
    y.append(trial["target_1"])
    # y.append(trial["target1"])
    annotations.append(trial["filename"][12:23])
    # annotations.append(trial["stimulus"][0:11])
    natural_cost = np.fromstring(trial["filename"][13:16], dtype=int, sep=" ")
    # natural_cost = np.fromstring(trial["stimulus"][1:4], dtype=int, sep=" ")
    enforcer_action = np.fromstring(trial["filename"][19:22], dtype=int, sep=" ")
    # enforcer_action = np.fromstring(trial["stimulus"][7:10], dtype=int, sep=" ")
    natural_costs.append(natural_cost)
    enforcer_actions.append(enforcer_action)
    filename = "../data/model_comparisons/" + str(2.0) + "/" + str(np.array(natural_cost)) + "_" + str(np.array(enforcer_action)) + ".txt"
    with open(filename, "r") as file:
        reader = csv.reader(file)
        data = []
        for row in reader:
            data.append([float(num) for num in row])
        data = np.array(data).reshape(10, 10, 11)
        prob_A = np.sum(data, axis=(1, 2))
        prob_B = np.sum(data, axis=(0, 2))
        prob_p = np.sum(data, axis=(0, 1))
        expected_A = np.sum(np.multiply(prob_A, np.arange(10)))
        expected_B.append(np.sum(np.multiply(prob_B, np.arange(10))))
        expected_p.append(np.sum(np.multiply(prob_p, np.arange(11)/10)))

# print(expected_p)
# print(y)

# fit = np.polyfit(expected_B, x, deg=1)
# ax.plot(expected_B, fit[0] * expected_B + fit[1], color='red')
ax.scatter(expected_B, x)
ax.set_title("Human-Model Analysis of Agent Reward Inference")
ax.set_xlabel("Model Predictions")
ax.set_ylabel("Human Performance")
ax.set_xlim([0.0, 10.0])
ax.set_ylim([0.0, 10.0])

# fit = np.polyfit(expected_p, y, deg=1)
# ax1.plot(expected_p, fit[0] * expected_p + fit[1], color='red')
ax1.scatter(expected_p, y)
ax1.set_title("Human-Model Analysis of Agent ToM Inference")
ax1.set_xlabel("Model Predictions")
ax1.set_ylabel("Human Performance")

for i, annotation in enumerate(annotations): 
  ax.annotate(annotation, (expected_B[i], x[i]))
  ax1.annotate(annotation, (expected_p[i], y[i]))
  # ax2.annotate(annotation[6:11], (x[i], y[i]))

# for figure in [ax, ax1]:
  # figure.set_xlim([0.0, 1.0])
  # figure.set_ylim([0.0, 1.0])

# ax.set_title("Pilot data - full")
# ax1.set_title("Pilot data - natural_costs")
# ax2.set_title("Pilot data - enforcer_actions")

# print(natural_costs)
# print(enforcer_actions)

plt.show()
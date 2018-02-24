import json
import matplotlib.pyplot as plt

with open("D:/Research/social_pragmatics/data/joan.json", "r") as file:
	data = json.load(file)

print(len(data["trials"]))

fig, ax = plt.subplots()
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()

trials = data["trials"]
x, y = [], []
natural_costs, enforcer_actions, annotations = [], [], []
for trial in trials:
	x.append(trial["target0"])
	y.append(trial["target1"])
	# natural_costs.append(trial["stimulus"][:5])
	# enforcer_actions.append(trial["stimulus"][7:11])
	annotations.append(trial["stimulus"][:11])

for i, annotation in enumerate(annotations): 
	# print(i, annotation)
	ax.annotate(annotation, (x[i], y[i]))
	ax1.annotate(annotation[:5], (x[i], y[i]))
	ax2.annotate(annotation[6:11], (x[i], y[i]))

for figure in [ax, ax1, ax2]:
	figure.scatter(x, y)
	figure.set_xlabel("Agent Rewards (Banana)")
	figure.set_ylabel("Degree of ToM")
	figure.set_xlim([0.0, 1.0])
	figure.set_ylim([0.0, 1.0])

ax.set_title("Pilot data - full")
ax1.set_title("Pilot data - natural_costs")
ax2.set_title("Pilot data - enforcer_actions")

plt.show()
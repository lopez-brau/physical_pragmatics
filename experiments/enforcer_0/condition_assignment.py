import csv
import itertools as it
import numpy as np

# Define the agent conditions.
agent_conditions = ["agentive", "non-agentive"]

# Define the renovation sides.
renovation_sides = ["left", "right"]

# Define the employee preferences.
employee_preferences = ["left", "right", "none"]

# Set the number of participants.
num_participants = 20

# Compute the number of condition blocks.
condition_blocks = num_participants / len(agent_conditions) \
    / len(renovation_sides)

# Initialize an array to store the trial information.
trial_information = []

# Compute the trial information for each participant.
for b in np.arange(condition_blocks):
    # Define all possible variations of conditions for the current condition
    # block.
    trial_parameters_set = \
        it.product(agent_conditions, renovation_sides, repeat=1)

    # Randomize the employee preferences, merge them with the current
    # condition block, and store them.
    for trial_parameters in trial_parameters_set:
        np.random.shuffle(employee_preferences)
        trial_information.append(list(trial_parameters)+list(employee_preferences))
"""
# Compute the trial information for each participant.
trial_parameters_set = it.product(agent_conditions, renovation_sides,
    employee_preferences, repeat=1)
for trial_parameters in trial_parameters_set:
    trial_information.append(trial_parameters)
"""
# Print to a file.
with open("condition_assignment.csv", "w") as file:
    writer = csv.writer(file, lineterminator="\n")
    for row in trial_information:
        writer.writerow(row)

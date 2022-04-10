import csv
import numpy as np

# Define the cost conditions.
conditions = ["none", "low"]

# Define the objects used in the experiment.
objects = [
    "plant",
    "chair",
    "books",
    "cinderblocks",
    "tape",
    "rulers",
    "hat",
    "string"
]

# Define which doors are open and closed.
doors = {
    "plant": "closed",
    "chair": "open",
    "books": "open",
    "cinderblocks": "open",
    "tape": "closed",
    "rulers": "open",
    "hat": "closed",
    "string": "closed"
}

# Set the number of participants.
num_participants = 80

# Initialize an array to store the trial information.
trial_information = []

# Compute the trial information for each participant.
for p in np.arange(num_participants):
    # Determine the trial order for this participant.
    if p < (num_participants/len(conditions)):
        condition_order = ["none", "low"]
    else:
        condition_order = ["low", "none"]

    # Determine the objects to be presented to this participant.
    first_object = objects[p%len(objects)]
    if (p%len(objects)+1) == len(objects):
        second_object = objects[0]
    else:
        second_object = objects[p%len(objects)+1]

    # Store the trial information for this participant.
    trial_information.append([condition_order[0], first_object,
        condition_order[1], second_object])

# Print to a file.
with open("condition_assignment.csv", "w") as file:
    writer = csv.writer(file, lineterminator="\n")
    for row in trial_information:
        writer.writerow(row)

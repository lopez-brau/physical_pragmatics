import csv
import numpy as np

# Define the cost conditions.
conditions = ["none", "low"]

# Define the objects used in the experiment.
objects = [
    "cone",
    "stanchion",
    "tape"
]

# Define which doors are open and closed.
doors = {
    "cone": "closed",
    "books": "closed",
    "tape": "closed"
}

# Set the number of participants.
num_participants = 60

# Initialize an array to store the trial information.
trial_information = []

# Compute the trial information for each participant.
for p in np.arange(num_participants):    
    # Determine the condition for this participant.
    if p < (num_participants/len(conditions)):
        condition = "none"
    else:
        condition = "low"

    # Determine the object to be presented to this participant.
    obj = objects[p%len(objects)]

    # Store the trial information for this participant.
    trial_information.append([condition, obj])

# Print to a file.
with open("condition_assignment.csv", "w") as file:
    writer = csv.writer(file, lineterminator="\n")
    for row in trial_information:
        writer.writerow(row)

import csv
import json
import numpy as np
import sys

filename = sys.argv[1]

with open(filename + ".json", "r") as file:
    data = json.load(file)

trials = data["trials"]

with open(filename + ".csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["target_0", "target_1", "filename"])
    for trial in trials:
        writer.writerow([trial["target_0"], trial["target_1"], trial["filename"]])

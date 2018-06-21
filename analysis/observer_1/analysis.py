import csv
import json
import numpy as np

with open("D:/Research/social_pragmatics/data/michael.json", "r") as file:
    data = json.load(file)

trials = data["trials"]

with open("D:/Research/social_pragmatics/data/temp.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["target_0", "target_1", "filename"])
    for trial in trials:
        writer.writerow([trial["target_0"], trial["target_1"], trial["filename"]])

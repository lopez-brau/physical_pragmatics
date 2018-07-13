#!/bin/bash

declare -a NATURAL_COSTS=("4 4" "4 5" "4 6" "5 4" "5 5" "5 6" "6 4" "6 5" "6 6")

for NATURAL_COST in "${NATURAL_COSTS[@]}"
do
	python3 main.py $NATURAL_COST
	echo "Done running with NATURAL_COST = $NATURAL_COST"
done
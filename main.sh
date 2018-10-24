#!/bin/bash

declare -a NATURAL_COSTS=("3 3" "3 4" "4 3" "4 4")

for NATURAL_COST in "${NATURAL_COSTS[@]}"
do
	python3 main.py $NATURAL_COST
	echo "Done running with NATURAL_COST = $NATURAL_COST"
done
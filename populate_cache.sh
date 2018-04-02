#!/bin/bash

declare -a NATURAL_COSTS=("2 2" "2 3" "2 4" "3 2" "3 3" "3 4" "4 2" "4 3" "4 4")

for NATURAL_COST in "${NATURAL_COSTS[@]}"
do
	python3 populate_cache.py $NATURAL_COST
	echo "Done populating with NATURAL_COST = $NATURAL_COST"
done

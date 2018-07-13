#!/bin/bash

declare -a NATURAL_COSTS=("4 4" "4 5" "4 6" "5 4" "5 5" "5 6" "6 4" "6 5" "6 6")

for NATURAL_COST in "${NATURAL_COSTS[@]}"
do
	python3 populate_cache.py $NATURAL_COST
	echo "Done populating with NATURAL_COST = $NATURAL_COST"
done

#!/bin/bash

declare -a NATURAL_COSTS=("3 3" "3 4" "4 3" "4 4")

for NATURAL_COST in "${NATURAL_COSTS[@]}"
do
	python3 populate_cache.py $NATURAL_COST
	echo "Done populating with NATURAL_COST = $NATURAL_COST"
done

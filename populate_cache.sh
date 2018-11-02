#!/bin/bash

for NATURAL_COST_A in {0..9}
do 
	for NATURAL_COST_B in {0..9}
	do
		python3 populate_cache.py $NATURAL_COST_A $NATURAL_COST_B
		echo "Done populating with NATURAL_COST = [$NATURAL_COST_A, $NATURAL_COST_B]"
	done
done

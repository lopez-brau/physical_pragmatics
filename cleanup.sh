#!/bin/bash

# Clean up cache.
rm cache/*.csv

# Clean up extra files created by tex compilation.
rm *.aux
rm *.log
rm *.pdf
rm -r imgs/observer_1/*/*/*.tex

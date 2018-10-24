#!/bin/bash

# Clean up extra files created by tex compilation.
rm stimuli/*/*.aux
rm stimuli/*/*.log
rm stimuli/*/*.pdf
rm stimuli/*/*synctex.gz
rm -r stimuli/*/*/*/*.tex

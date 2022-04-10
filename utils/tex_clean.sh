#!/bin/bash

# Clean up extra files created by TeX compilation.
find ../stimuli/*/* -name "*.aux" -delete
find ../stimuli/*/* -name "*.log" -delete
find ../stimuli/*/* -name "*.pdf" -delete
find ../stimuli/*/* -name "*.synctex.gz" -delete
find ../stimuli/*/*/*/* -name "*.tex" -delete

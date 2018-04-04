#!/bin/bash

# Clean up cache.
# rm cache/*.csv

# Clean up extra files created by tex compilation.
rm imgs/*/*.aux
rm imgs/*/*.log
rm imgs/*/*.pdf
rm imgs/*/*synctex.gz
rm -r imgs/*/*/*/*.tex

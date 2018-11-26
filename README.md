# Social Pragmatics

## Research Question: How do people communicate their intentions by assigning meaning to objects in the world?

- Read Baker et al. 2009 for background
- We want to show that in order to do this assignment, we need:
	1. Theory of Mind (ToM)
	2. Intuitive physics (for understanding costs) 
	3. A sense of cooperation (or lack of)
- Grice (1957)

`populate_cache.sh`: run this with `bash populate_cache.sh` in a bash terminal to populate the `cache` folder with data from the various agent models.

Make sure to update PATH in `utils/config.py` to
```
PATH = "/path/to/repository/"
```

## To-do

- Clean up `data/observer/model`.
- Implement `cache_enforcer_ToM`.
- ShinyApps: Set up a GUI with sliders for each of the parameters; displays how the model predictions change.

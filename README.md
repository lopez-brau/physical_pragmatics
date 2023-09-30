# Communicative meaning of objects

Project repository for the paper, "People can use the placement of objects to infer communicative goals" ([link](https://doi.org/10.1016/j.cognition.2023.105524)).

## Repository structure

- `analysis`: Contains the R code to generate all results and figures reported in the paper (see our [OSF repository](https://osf.io/57n4g/) for a slimmer version of this same code)
- `cache`: Empty by default; used for storing the model predictions from the intermediate agent models
- `cluster`: Contains the terminal commands for generating the model predictions for each agent
- `data`: Contains the raw and processed participant data and model predictions
- `experiments`: Contains the web code for generating the experiments
- `models`: Contains the Python code for generating model predictions given experiment parameters
- `stimuli`: Contains the stimuli used in the experiments
- `utils`: Contains a Bash script to clean leftover TeX files after generating stimuli

## Experiment structure

The folders use internal names for the experiments. These internal names map onto the experiment names in the paper as follows:

- `decider_0`: Experiment 2a
- `decider_1`: Experiment 1
- `decider_2`: Experiment 2c
- `observer_0`: Experiment 4
- `observer_1`: Experiment 4 (replication)
- `symbols_1`: Experiment 3
- `tsimane_0`: Experiment 2b

## Setup

To run the analysis code, you will need R 4.1.2 (or higher) and R Markdown 2.11 (or higher). To run the model code, you will need any version of Python 3, numpy 1.22.0 (or higher), matplotlib 3.5.0 (or higher), and a terminal capable of using Bash.

## Generating data

`cluster` contains a text file for each level of the recursive model, each with the list of terminal commands for generating the model predictions for each trial. These commands can be run independently and in parallel or (if you dare) sequentially.

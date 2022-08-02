# feature_learning

## Requirements
- pandas
- numpy
- matplotlib
- torch
- sklearn
- missingno
- scipy
- astropy
- toml

## TabNet Customization
- to install the custom TabNet implementation navigate to the feature_learning/03_pytorch_tabnet directory and use "python setup.py install"

## Experiments Setup
- to setup an experiment, use the config.toml
- define the fixed parameters
- to vary a parameter (e.g. run the experiment for the train_val_splits 0.5, 0.6, 0.7, 0.8 and 0.9):
	- set the experiment_variable parameter to the respective variable (e.g. experiment_variable = "train_val_split")
	- set the variable (here: train_val_split) to a list of parameters, instead of a single parameter (e.g. [0.5, 0.6, 0.7, 0.8, 0.9])
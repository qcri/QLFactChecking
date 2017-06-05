# QLFactChecking

This project contains scripts for preparation of Fact Checking in the Qatar Living community forum.

## Setup

Copy the XML file with the annotations for True and False comments in directory *data/input*.
The file name should be input-**set_name**.xml, where **set_name** is the name of the dataset contained in the file.

The set name can be changed in file *RunCV.py -> SET_NAME*.

## Run

The project was built with Python 3.5. You will need Python 3 to run it.

You will need to install the following Python modules: **scikit-learn**, **numpy**.

In order to run the classificaiton, execute the file *RunMultiple.py* in directory *code/classification/answers*.

The results will be saved in directory: *data/results*. The predictions for each examples will be saved in directory *data/predictions*.

## Feature Combinations

To run the features combinations, execute the file **combine_best_feature_groups.py**.

The results are read from file *data/results/results-answers-cross-validation-dev+test.tsv* (this file is also configured in **combine_best_feature_groups.py -> RESULTS_FILE** ) and are written in the same file.

To specify whether the results should be sorted by Accuracy or MAP, change the value of **combine_best_feature_groups.py -> RESULT_SCORE_INDEX**. You can also change the prefix of the runs, to differ them in the results file, in **combine_best_feature_groups.py -> RUN_PREFIX**.


## Features

To add new features:

* Add the feature file in folder **data/features**. To allow unified reading of all feature files, the file name needs to be of the form *PREFIX1-feature_description-PREFIX2*. The prefixes can be changed in file **Features.py**.

The feature files need to contain one line for each answer. The line contains the answer ID followed by the features extracted for this answer, separated with tabs. (*example: Q273_R39_C4	0	0	0	0	114	6	19*)

* In **Features.py** add a new method for reading your file.

* Add your features as a new set or combine it with other features in the file **FeatureSets.py**.

* In file **RunMultiple.py**, add the newly configured set for execution.


## Baselines

Several baselines are being computed when the results file is being created for the first time. If you need a fresh computing of the baselines, you need to remove this file from the **results** directory.

You can exclude execution of the bag-of-words and ngrams baselines by setting the value of *INCLUDE_TEXT_BASELINES* in the file *RunCV.py* to *False*.



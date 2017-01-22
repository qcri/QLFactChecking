# QLFactChecking

This project contains scripts for preparation of Fact Checking in the Qatar Living community forum.

## Setup

Copy the XML file with the annotations for True and False comments in directory *data/input*.
The file name should be input-**set_name**.xml, where **set_name** is the name of the dataset contained in the file.

The set name can be changed in file *RunCV.py -> SET_NAME*.

## Run

The project was built with Python 3.5. You will need Python 3 to run it.

In order to run the classificaiton, execute the file *RunMultiple.py* in directory *code/classification/answers*.

The results will be saved in directory: *data/results*. The predictions for each examples will be saved in directory *data/predictions*.

## Features
  **TODO**
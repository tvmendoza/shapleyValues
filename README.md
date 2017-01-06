# Shapley Values Calculator

Shapley Values calculator is a file that reads a python file with different criteria and calculates the shappley values.  


## Usage Instructions

Just run the script with the input file you want to run the script against:

$ python shapleyCalculation.py test.json

## Input data

Sample input data should be a json file with two or more labeled alternatives, one or more labeled criteria, and the numeric responses to each criteria for each alternative.  This example input file shows response data for 4 criteria for two different patients. 

{
    "participants": [{
        "Cost": {
            "FIT:": 1.0,
            "Colonoscopy:": 0.1,
            "Flexible Sigmoidoscopy:": 0.6
        },
        "Further Testing": {
            "FIT:": 1.0,
            "Colonoscopy:": 1.0,
            "Flexible Sigmoidoscopy:": 1.0
        },
        "Test Preparation": {
            "FIT:": 1.0,
            "Colonoscopy:": 1.0,
            "Flexible Sigmoidoscopy:": 1.0
        },
        "Time": {
            "FIT:": 1.0,
            "Colonoscopy:": 1.0,
            "Flexible Sigmoidoscopy:": 1.0
        }
    },{
        "Cost": {
            "FIT:": 0.1,
            "Colonoscopy:": 1.0,
            "Flexible Sigmoidoscopy:": 1.0
        },
        "Further Testing": {
            "FIT:": 1.0,
            "Colonoscopy:": 1.0,
            "Flexible Sigmoidoscopy:": 1.0
        },
        "Test Preparation": {
            "FIT:": 1.0,
            "Colonoscopy:": 1.0,
            "Flexible Sigmoidoscopy:": 1.0
        },
        "Time": {
            "FIT:": 1.0,
            "Colonoscopy:": 1.0,
            "Flexible Sigmoidoscopy:": 1.0
         }
    }]
}

## Output data

The script will have two outputs: 
1)The shell will print each of the shappley values
2)A results.txt file will be created with the shappley values of each participant plus the average of each criteria. 


Member Shapley Further Testing: 0.234378535551
Member Shapley Cost: 0.113355569852
Member Shapley Time: 0.440930104224
Member Shapley Test Preparation: 0.211335790373
*************
Member Shapley Further Testing: 0.234750368689
Member Shapley Cost: 0.272279323587
Member Shapley Time: 0.247248097151
Member Shapley Test Preparation: 0.245722210573
*************
Further Testing has an average of: 0.23456445212
Cost has an average of: 0.19281744672
Test Preparation has an average of: 0.228529000473
Time has an average of: 0.344089100687

## Requirements

This project requires Python 2.7 or greater.


## Contributions

The Biomedical Informatics mHealth lab welcomes contributions to this project. Please fork and send pull requests with your revisions.
# shapleyValues

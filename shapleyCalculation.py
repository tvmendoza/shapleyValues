import itertools
import random
import operator
import json
import jsonschema
import pprint
import math
from decimal import Decimal
import sys
import argparse
import string
# Created by Tona Mendoza on 01/04/17.
# Copyright © 2017 UF Biomedical Informatics mHealth Lab.

namesDict = {}
averageDict = {}

def make_all_subsets(list_of_members):
        # make every possible subsets of given list_of_members
        # for size in (list_of_members):
            # use combinations to enumerate all combinations of size elements
            # append all combinations to self.data

        set_of_all_subsets = set([])

        for i in range(len(list_of_members),-1,-1):
            for element in itertools.combinations(list_of_members,i):
                set_of_all_subsets.add(frozenset(element))
        return sorted(set_of_all_subsets)


class FuzzyMeasure:
    '''A class to produce a fuzzy measure of based on a list of criteria'''

    def __init__(self, criteria={}, output = ""):
        # initialize a class to hold all fuzzyMeasure related objects
        self.set_of_all_subsets = set([])
        self.mu = ()
        self.criteria = criteria
        self.output = output
        self.list_of_members = frozenset(criteria.keys())
        self.setup()

    def setup(self):
        if len(self.criteria) < 1 :
            return
        self.make_all_subsets()
        self.set_fm_for_trivial_cases()
        self.set_fm_for_singleton_sets()
        self.set_fm_for_complex_sets()
        self.calculate_shapley_values(self.output)

    def store_criteria(self, criteria):
        self.list_of_members = frozenset(criteria.keys())
        self.criteria = criteria

    def make_all_subsets(self):
        # make every possible subsets of given list_of_members
        self.set_of_all_subsets = make_all_subsets(self.list_of_members)

    def set_fm_for_trivial_cases(self):
        # set fuzzyMeasure for empty and complete sets
        # mu[] := 0
        # mu[X] := 1
        self.mu = {frozenset(): 0, self.list_of_members: 1}

    def set_fm_for_singleton_sets(self):
        '''set fuzzyMeasure for sets with exactly one member'''

        sum_of_criteria_values = 0
        for criterium in self.criteria:
            sum_of_criteria_values += self.criteria[criterium]


        for criterium in self.criteria:
            singleton_set = frozenset([criterium])
            self.mu[singleton_set] = self.criteria[criterium]/sum_of_criteria_values

    def set_fm_for_complex_sets(self):
        # set fuzzyMeasure for sets with 2 or more members

        # Random generation of a fuzzy measure mu on a set X
        # note: 'undefined' means we have not yet calculated and stored the value of mu for mu(foo)
        # create list of sets from X and shuffle the list
        list_of_all_subsets = list(self.set_of_all_subsets)
        random.shuffle(list_of_all_subsets)

        for A in list_of_all_subsets:
            if self.mu.get(A) is None:
                minimum_for_mu_A = 0
                maximum_for_mu_A = 1

                subsets_of_A = make_all_subsets(A)
                for B in subsets_of_A:
                    if self.mu.get(B) is not None:
                        minimum_for_mu_A = max(self.mu.get(B), minimum_for_mu_A)

                for B in list_of_all_subsets:
                    if self.mu.get(B) is not None:
                        if B.issuperset(A):
                            maximum_for_mu_A = min(maximum_for_mu_A, self.mu.get(B))

                self.mu[A] = random.uniform(minimum_for_mu_A,maximum_for_mu_A)

        
    ''' 
        To calculate the shapley values we need to do get the Mu of each subset calculated in the function set_fm_for_complex_sets.
        The formula used is as follow:

        I(i,j) = "The sum of" ( ( ( (|I|- [B]-1)!*[B]!) /[I]!)  * [Mu(B U [j]) - Mu(B))] )


            Definitions:
                "The sum of" is defined as all the subsets without {j}
                B is the subset that does not contain {j}
                |I| the total number of members. 
                [b] is the size of the subset without {j}.
                B U {j} = The union of B and {j}


    '''
    def calculate_shapley_values(self,output):
        print("*************")
        memberShapley = 0
        total = 0
        factorialTotal = math.factorial(len(self.list_of_members))
        for member in self.list_of_members:
            for subset in self.set_of_all_subsets:
                if member in subset:
                    #The muSet is the mu of Mu(B U {j})
                    muSet = self.mu.get(subset)
                    remainderSet = subset.difference(set(member))
                    muRemainer = self.mu.get(remainderSet)
                    difference = muSet - muRemainer
                    b = len(remainderSet)
                    factValue = (len(self.list_of_members) - b -1 )
                    divisor = (math.factorial(factValue) * math.factorial(b) * 1.0) / (factorialTotal * 1.0)
                    weightValue = divisor * difference
                    memberShapley = memberShapley + weightValue
            averageDict[namesDict[member]] += memberShapley
            print("Member Shapley " + str(namesDict[member]) + ": " + str(memberShapley))
            output.write("Member Shapley " + str(namesDict[member]) + ": " + str(memberShapley) + "\n")
            total = total + memberShapley
            memberShapley = 0
        print("Total: " + str(total) + " *** Note: This should equal to 1.0")
        output.write("*************\n")
        print("*************")

scores = {}

def get_criteria(scores):
    '''return a list containing labels for each criterium'''
    list_of_criteria = scores.keys()
    return list_of_criteria

def sum_of_criteria_values(scores):
    '''return a dictionary of the sum of each criterium across the alternatives keyed on the criteria labels'''
    dict_of_criteria_sums = {}
    list_of_criteria = get_criteria(scores)
    for criteria in list_of_criteria:
        dict_of_criteria_sums[criteria] = sum(scores[criteria].values())

    return dict_of_criteria_sums


def update_keys(args):
    index = 0
    for key in args.keys():
        new_key = string.ascii_lowercase[index]
        if new_key != key:
            if key not in averageDict: 
                averageDict[key] = 0
            namesDict[new_key] = key 
            args[new_key] = args[key]
            del args[key]
        index += 1
    return args

def print_averages(totalParticipants, outFile):
    total = 0
    for key in averageDict:
        print ("The member: " + str(key) + " has an average of: " + str(averageDict[key]/totalParticipants))
        outFile.write(str(key) + " has an average of: " + str(averageDict[key]/totalParticipants)  + "\n")
        total = averageDict[key]/totalParticipants + total
    print(total)



def main():
   # define the list of acceptable arguments
    outFile = open("results.txt", 'w')
    totalParticipants = 0
    parser = argparse.ArgumentParser(
        description='Provide the name of the json file to be used to calculate the shapley values.')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument(
        '-i',
        '--input',
        choices=['json'],
        dest='input',
        default='json',
        help='Specify the file type used as input. Valid types: json')

    # prepare the arguments we were given
    args = parser.parse_args()
    # Prepare the input
    if args.input == 'json':
    	jsonScores = args.infile.read()
        if len(jsonScores) > 0:
            allParticiants = json.loads(jsonScores)
            print("Process started. ")
            for scoreJson in allParticiants["participants"]:
                totalParticipants += 1
                scores = update_keys(scoreJson)
                list_of_criteria = get_criteria(scores = scores)
                dict_of_criteria_sums = sum_of_criteria_values(scores = scores)
                # compute fuzzy measure
                FuzzyMeasure(criteria=dict_of_criteria_sums, output=outFile)
            print_averages(totalParticipants,outFile);
    	# else:
     #    	print("error: No input supplied")
    else:
        print ("Unsupported input type")
        return()
    outFile.close()
    print("Process completed.")

































main()

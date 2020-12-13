#!/usr/bin/python
# Conor Wallace 20235661
# CT5148 Programming Assignment 3
# manual_solve.py
# My Github repository can be found at the link below
# https://github.com/conorwa/ARC

import os, sys
import json
import numpy as np
import re

### YOUR CODE HERE: write at least three functions which solve
### specific tasks by transforming the input x and returning the
### result. Name them according to the task ID as in the three
### examples below. Delete the three examples. The tasks you choose
### must be in the data/training directory, not data/evaluation.

## The numbers to colour encoding is as follows
## Colour Encoding: Black = 0, Blue = 1, Red =2 , Green = 3 , Yellow = 4 , Grey = 5 , Pink = 6 , Orange = 7 , Light Blue = 8 , Brown = 9

# To solve cdecee7f: The grid has a size 10x10. Each column has a two coluours, Black and another colour. These colours then need to 
# be added to a new grid size 3x3. The way this is populated is shown below, from 1st colour to 9th colour found. 
# If Black colour found it is moved to the end, there fore if 9 colours found then last colour can't be Black.
# [1st Colour, 2nd colour, 3rd colour]
# [6th colour, 5th colour, 4th colour] ## Note this row is reversed
# [7th colour, 8th colour, 9th colour]
# If there are less than 9 colours then the remaining are populated as Black
# We need to get the Max number in each of the columns.
# Then where there are zero's move them to the end of the list, and delete the last index in the list
# Then split the list into three, and append that into the array as the answer. 
def solve_cdecee7f(x):
    #Check for Max number in each column, Black is zero so if there is another colour in the column, it will always be the max
    col_max =np.max(x, axis=0)
    #Next four line removes zero's first and then moves them to the end of the list, and then removes the last item in the list
    col_temp = [x for x in col_max if x !=0]
    col_temp1 = [x for x in col_max  if x == 0]
    col_temp.extend(col_temp1)
    col_temp2 = np.delete(col_temp, [-1])
    #Reshape to size 3x3
    out_array = np.reshape(col_temp2, (3,3))
    #Reverse row 1
    out_array[1]= np.flip(out_array[1])

    x = out_array
    return x

# To solve f8b3ba0a: From the test grid we have to find the frequency of all unique numbers. Then sort the result, and filter out the top too frequencies 
# Then the next three colours need to be placed into a 3 x 1 grid, decending order of colour occurance
def solve_f8b3ba0a(x):
    # Find unique colour frequencies in our array
    (unique, counts) = np.unique(x, return_counts=True)
    colour_freq = np.asarray((unique, counts)).T
    #Sort frequencies
    colour_freq =colour_freq [colour_freq[:,1].argsort()[::-1]]
    # Get colour numbers
    colour_num = colour_freq[2:, 0]
    x = np.reshape(colour_num, (3,1))
    print(colour_freq)
    print (colour_num.shape)
    
    return x

# To solve c8f0f002 we need to replace Orange with Grey
def solve_c8f0f002(x):
    # Replace Orange squares with Grey squares
    np.place(x, x==7, 5)
    return x


#To solve 7c008303 we need to first find the indexes where there are no Black, Green or Light Blue Squares. 
#These indexes will be 2x2 and have a colour associated to each
#Then find the indexes of the 4 Green 3x3 "boxes", and match the index colours that we found above to these, so the  new colour
#pattern matches the Green pattern
#A new 2D Array, 6x6 needs to be created with these new pattern boxes and then split into 3x3 boxes. Each of these 3x3 box

def solve_7c008303(x):
    #Find the colours in the grid that are not Black, or Green or LIght Blue
    fd_colour = np.argwhere((x !=0) & (x !=3) & (x !=8))
    # Extract the unique colours
    unique_col = [x[(row,col)] for (row,col) in fd_colour]
    # Search for 6x6 arrays with only Three's or Zero's
    
    
    return x

def main():
    # Find all the functions defined in this file whose names are
    # like solve_abcd1234(), and run them.

    # regex to match solve_* functions and extract task IDs
    p = r"solve_([a-f0-9]{8})" 
    tasks_solvers = []
    # globals() gives a dict containing all global names (variables
    # and functions), as name: value pairs.
    for name in globals(): 
        m = re.match(p, name)
        if m:
            # if the name fits the pattern eg solve_abcd1234
            ID = m.group(1) # just the task ID
            solve_fn = globals()[name] # the fn itself
            tasks_solvers.append((ID, solve_fn))

    for ID, solve_fn in tasks_solvers:
        # for each task, read the data and call test()
        directory = os.path.join("..", "data", "training")
        json_filename = os.path.join(directory, ID + ".json")
        data = read_ARC_JSON(json_filename)
        test(ID, solve_fn, data)
    
def read_ARC_JSON(filepath):
    """Given a filepath, read in the ARC task data which is in JSON
    format. Extract the train/test input/output pairs of
    grids. Convert each grid to np.array and return train_input,
    train_output, test_input, test_output."""
    
    # Open the JSON file and load it 
    data = json.load(open(filepath))

    # Extract the train/test input/output grids. Each grid will be a
    # list of lists of ints. We convert to Numpy.
    train_input = [np.array(data['train'][i]['input']) for i in range(len(data['train']))]
    train_output = [np.array(data['train'][i]['output']) for i in range(len(data['train']))]
    test_input = [np.array(data['test'][i]['input']) for i in range(len(data['test']))]
    test_output = [np.array(data['test'][i]['output']) for i in range(len(data['test']))]

    return (train_input, train_output, test_input, test_output)


def test(taskID, solve, data):
    """Given a task ID, call the given solve() function on every
    example in the task data."""
    print(taskID)
    train_input, train_output, test_input, test_output = data
    print("Training grids")
    for x, y in zip(train_input, train_output):
        yhat = solve(x)
        show_result(x, y, yhat)
    print("Test grids")
    for x, y in zip(test_input, test_output):
        yhat = solve(x)
        show_result(x, y, yhat)

        
def show_result(x, y, yhat):
    print("Input")
    print(x)
    print("Correct output")
    print(y)
    print("Our output")
    print(yhat)
    print("Correct?")
    # if yhat has the right shape, then (y == yhat) is a bool array
    # and we test whether it is True everywhere. if yhat has the wrong
    # shape, then y == yhat is just a single bool.
    print(np.all(y == yhat))

if __name__ == "__main__": main()


# For argument parsing
import getopt, sys

import matplotlib.pyplot as plt
import numpy as np


def tolerance_formula(N, e):
    '''
    Tolerance formula from Yang, p. 9
    '''
    print(N, e)
    return e <= N/np.log(N)

def tolerance_formula_plot(N):
    '''
    Tolerance formula from Yang, p. 9
    '''
    return N/np.log(N)

def plot_tolerance():
    tot = 100000
    N = np.arange(2,tot,100)
    plt.plot(N, tolerance_formula_plot(N))
    plt.ylim(0, tot)
    plt.xlabel("Total number of items")
    plt.ylabel("Number of exceptions allowed by TP")
    plt.show()




def main():
    
    # Code for parsing arguments from: https://www.geeksforgeeks.org/command-line-arguments-in-python/
    
    # Remove 1st argument from the
    # list of command line arguments
    argumentList = sys.argv[1:]

    # Options
    options = "hmo:d:t:"

    # Long options
    long_options = ["Help", "My_file", "Output=", 'directory=', 'type=']

    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)
        
        # checking each argument
        for currentArgument, currentValue in arguments:

            if currentArgument in ("-h", "--Help"):
                print ("Displaying Help")
                
            elif currentArgument in ("-m", "--My_file"):
                print ("Displaying file_name:", sys.argv[0])
            
            elif currentArgument in ("-d", "--directory"):
                print(f"Analyzing directory {currentValue}")
                root_folder = currentValue
                
            elif currentArgument in ("-o", "--Output"):
                print(f"Output file is {currentValue}")
                save_file = currentValue
                if not ".pkl" in save_file:
                    save_file += ".pkl"
            
            elif currentArgument in ("-t", "--type"):
                if currentValue == 'plot_tolerance':
                    plot_tolerance()
                else:
                    print(f"Did not recognize type {type}, please specify a correct type")
                
    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))
        
        
    

#main()

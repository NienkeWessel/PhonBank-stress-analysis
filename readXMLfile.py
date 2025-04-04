from xml.dom import minidom

import lxml.etree as etree
import os
import pandas as pd
import fnmatch
import math

# For argument parsing
import getopt, sys

def readXMLfile(filename, df = pd.DataFrame(columns=['Name','Age','word','model','actual'])):
    """
        Reads Childes XML file and appends to data frame the name age correct word(orthography)
        correct pronounciation and uttered pronounciation per utterance
        
        filename = the name of the file to be read
        df = the current data frame; optional, if not specified, function will make a new data frame
    """
    
    # Counter counts how many items were problematic to parse in some sense, for future reference purposes
    skipcounter = 0


    # parse an xml file by name
    f = minidom.parse(filename)

    #use getElementsByTagName() to get tag
    session = f.getElementsByTagName('session')[0]
    try: 
        child_name = session.getElementsByTagName('participants')[0].getElementsByTagName('participant')[0].getElementsByTagName('name')[0].firstChild.data
        child_age = session.getElementsByTagName('participants')[0].getElementsByTagName('participant')[0].getElementsByTagName('age')[0].firstChild.data
    except:
        print("Age or name is missing, skip file")
        # If age or name is missing, just return and ignore file
        return df
    
    transcript = session.getElementsByTagName('transcript')[0].getElementsByTagName('u')
    for u in transcript: 
        skip = False # skip boolean keeps track of whether something is wrong in the data
        try: 
            word = u.getElementsByTagName('orthography')[0].getElementsByTagName('g')[0].getElementsByTagName('w')[0].firstChild.data
            l = u.getElementsByTagName('ipaTier')
            
            col = []
        
            for attr in l:
                ipas = attr.getElementsByTagName('pg')
                found_ipa = False
                for ipa_cand in ipas:
                    #print(ipa_cand.toprettyxml())
                    ipa_cand_unpacked = ipa_cand.getElementsByTagName('w')[0].firstChild
                    if ipa_cand_unpacked is not None:
                        ipa = ipa_cand_unpacked
                        found_ipa = True
                        break
                if not found_ipa:
                    # if ipa is None for all of them, something is wrong, so we skip; no use to continue in this word, so break
                    skip = True
                    break
                else: 
                    col.append( (attr.attributes['form'].value, ipa.data) )
        except:
            skip = True
        
        if not skip:
            # We append name, age, word and the actual and model pronun to the list. We do not know/assume in which order the latter two occur, so we use the dictionary structure to account for that and match the value with dict names
            dic = {'Name': child_name, 'Age': child_age, 'word': word, col[0][0]: col[0][1], col[1][0]: col[1][1]}
            df = pd.concat([df, pd.DataFrame.from_records([dic])], ignore_index = True)
        else:
            # We skipped one, so we increment the counter
            skipcounter += 1
    
    # Signal ending of file reading and return completed dataframe
    print("done reading {}, skipped {} items".format(filename, skipcounter))
    return df


def find_files(root_folder='../CLPF'):
    """
    Code from stack overflow: https://stackoverflow.com/questions/2186525/how-to-use-glob-to-find-files-recursively
    """
    
    matches = []
    for root, dirnames, filenames in os.walk(root_folder):
        for filename in fnmatch.filter(filenames, '*.xml'):
            if 'project' in filename:
                continue
            matches.append(os.path.join(root, filename))
    return matches


def save_data(filename, df):
    """
    Code from: https://www.kite.com/python/answers/how-to-save-a-pandas-dataframe-in-python
    """
    df.to_pickle(filename)


def read_data(filename):
    """
    Code from: https://www.kite.com/python/answers/how-to-save-a-pandas-dataframe-in-python
    """
    return pd.read_pickle(filename)



def main():
    
    # Code for parsing arguments from: https://www.geeksforgeeks.org/command-line-arguments-in-python/
    
    # Remove 1st argument from the
    # list of command line arguments
    argumentList = sys.argv[1:]

    # Options
    options = "hmo:d:"

    # Long options
    long_options = ["Help", "My_file", "Output=", 'directory=']

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
                
    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))

    
    # Collect all the file names, you can give it a root folder if you want to
    filenames = find_files(root_folder=root_folder) #'../Penney'
    #print(filenames)

    # To test if it all works (and it does (or did, at least))
    #df2 = readXMLfile("011010.xml")
    #save_data("test.pkl", df2)

    # Make empty data frame for the loop
    df = pd.DataFrame(columns=['Name','Age','word','model','actual'])

    # Loop through all the files and append to current dataframe
    for filename in filenames:
        print('file opened: ' + filename)
        df = readXMLfile(filename, df)

    df.rename(columns={'actual': 'realization'}, inplace=True)

    print(df)
    # Save data frame to pickle file
    save_data(save_file, df)


main()










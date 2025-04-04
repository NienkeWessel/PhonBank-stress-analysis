import csv
import pandas as pd

from settings import file_names_read, file_names_write


ipa_vowels = ['a', 'ɑ', 'œ', 'ɶ', 'æ', 'y', 'o', 'ɑ̈', 'i', 'u', 'ɪ', 'ə', 'ɛ', 'e', 'ɔ', 
              'ʌ', 'ø̈', 'ɛ̝', 'ɛ̈', 'ʉ', '͜u', 'œ̞', 'œ', 'ɛ̞', 'ɒ','ø', 'æ̝', 'ə̆', 'o͡', 'o̝', 
              'ʊ', 'ɯ', 'y', 'ɤ', 'ɨ', 'ɐ', 'ɯ̈', 'ɪ̟', 'ɪ͜']#, '͡']    fɪsˌhɶχ
agnostic_symbols = ['͡', 'ː', '̈', 'ˑ', '‿', '͜', '̞'] # symbols that can either be a vowel or consonant


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
    
def append_representation_to_dataframe(df):
    '''
    Appends the syllable representations of the model and realization to the dataframe 
    to have all information in one place
    
    df: data set, of which the representations need to be appended
    
    No return, as it mutates the df object
    '''
    df['rep_model'] = df.model.apply(build_syllable_representation)
    df['rep_realization'] = df.realization.apply(build_syllable_representation)
    #print(df)

def filter_df(df):
    '''
    Filters words ending in @n from the data set as they complicate things
    
    df: the data set that needs to be filter
    
    return: the filtered dataset
    '''
    return df[df.model.apply(lambda x: not (x[-1] == 'n' and x[-2] == 'ə'))]
    
    
def write_stats_to_csv(filename, a,b,c,d,e):
    '''
    stats_mod, stats_act, stats_match, stats_nonmatch_mod, stats_nonmatch_act
    '''
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(['number','modellengthall','realizationlengthall','lengthmatch', 'modellengthnonmatch', 'realizationlengthnonmatch'])

        # write the data
        for i in range(10):
            writer.writerow([i, a[i], b[i], c[i], d[i], e[i]])

def write_df_to_csv(filename, df):
    '''
    Saves the datafile to a csv
    '''
    df.to_csv(filename, index=False)
    

def find_common_words(df, condition=None):
    if condition == 'disyllable_models':
        df = df[df.rep_model.apply(lambda x: len(x) == 2)]
    if condition == 'disyllable_iamb_models':
        df = df[df.rep_model.apply(lambda x: len(x) == 2 and not x[0] and x[1])]
    if condition == 'SWS':
        df = df[df.rep_model.apply(lambda x: len(x) == 3 and x[0] and not x[1] and x[2])]
    if condition == 'Th':
        df = df[df.rep_model.apply(lambda x: len(x) == 2 and x[0] and not x[1])]
        df = df[df.model.apply(lambda x : is_final_syllable_superheavy(x))]
    write_df_to_csv('common_words_{}.csv'.format(condition), df[['Name', 'word']].value_counts())


def is_final_syllable_superheavy(word):
    '''
    DEPRECATED, JUST HERE TO MAKE THE TESTING CLASS HAPPY
    Use the function in the Word class instead
    
    
    if final is vowel, then check if prefinal is also vowel (or in agnostic and then the one before)
    if final is consonant, then check if prefinal is consonant. 
        If consonant, then superheavy
        If agnostic, check the one before and repeat
        If vowel, check the one before; if vowel again, then superheavy. If agnostic, check the one before. If consonant, not superheavy
    '''
    
    old_word = word
    word = ""
    
    for i in range(0,len(old_word)):
        if old_word[i] == 'ː':
            if old_word[i-1] in ipa_vowels:
                word += 'a'
            else: 
                word += 'c'
        else:
            word += old_word[i]
    
    word = [c for c in word if (c not in agnostic_symbols) and c != 'ˈ' and c != 'ˌ']

    if len(word) < 3:
        return False
    
    if word[-1] in ipa_vowels:
        return False
    else: #last char is a consonant
        if word[-2] not in ipa_vowels:
            # two consonants
            return True
        else:
            if word[-3] in ipa_vowels:
                return True
            else:
                return False


def is_final_syllable_heavy(word):
    '''
    DEPRECATED, JUST HERE TO MAKE THE TESTING CLASS HAPPY
    Use the function in the Word class instead
    '''
    if word[-1] in ipa_vowels:
        # if the last letter is a vowel, we only have a heavy syllable if it is a diphtong, so if the letter before it is also a vowel
        return word[-2] in ipa_vowels
    else: #so final letter in agnostic_symbols or consonants
        return True





def build_syllable_representation(word, secondary=False):
    """
    word: the word of which you want the syllable representation
    
    Returns the representation of the syllable in the form of a list of booleans, where true represents stressed and false unstressed
    """
    if not isinstance(word, str):
        return []
    
    representation = []
    
    found_nucleus = False
    found_coda = False
        
    # If the first character is a consonant, we already know it is not stressed
    # and the script will not work properly for this first syllable
    c = list(word)[0]
    if secondary:
        if c != "ˈ" and c != "ˌ" and c not in ipa_vowels and c not in agnostic_symbols:
            representation.append(False)
    elif c != "ˈ" and c not in ipa_vowels and c not in agnostic_symbols:
        representation.append(False)
    if c in ipa_vowels:
        representation.append(False)
    
    for c in list(word):
        if secondary and (c == "ˈ" or c == "ˌ"):
            representation.append(True)
            found_nucleus = False
            found_coda = False
        elif not secondary and c == "ˈ":
            representation.append(True)
            found_nucleus = False
            found_coda = False
        elif c in ipa_vowels: 
            if found_coda: #and not found_nucleus:
                # start of a new unstressed syllable
                representation.append(False)
            # in all cases, so start of unstressed syllable as well as
            # start of a stressed syllable, or following an onset consonant or following another vowel
            found_nucleus = True
            found_coda = False
        elif c not in agnostic_symbols:
            # So a consonant (because it is not a vowel and not agnostic)
            # if not found_nucleus, there is nothing to be done, because we are in the onset
            if found_nucleus:
                # We found the coda!
                found_coda = True
    return representation

def stringify_representation(representation):
    '''
    representation: list of booleans (representing stress pattern
    
    returns: string of the stress pattern
    '''
    string = ""
    for boolean in representation: 
        if boolean:
            string += 'T'
        else:
            string += 'F'
    return string



def pkl_to_csv(corpus_name):
    # Read data and add representation column to the data

    df = read_data(file_names_read[corpus_name])
    if corpus_name == 'CLPF':
        df = df.replace({'giraffe': 'giraf'}) #turns out that the CLPF corpus has two spellings for 'giraf'
    append_representation_to_dataframe(df)
    if corpus_name == 'Inkelas': #This corpus has a lot of entries without stress annotation
        df = df[df.rep_realization.apply(lambda x: (len(x) < 2) or (len(x) >= 2 and any(x)))]
    orig_length = df.size
    df.dropna(inplace=True)
    print("Dropped {} na items".format(orig_length-df.size))
    df = filter_df(df)
    curr_length = df.size
    print("Went from {} to {} with filtering, removing {}".format(orig_length, curr_length, orig_length - curr_length))
    print(df.head())
    print(df)
    write_df_to_csv(file_names_write[corpus_name], df)





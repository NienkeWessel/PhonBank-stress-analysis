import numpy as np
import pandas as pd

from utils import build_syllable_representation, stringify_representation
from utils import is_final_syllable_superheavy, write_df_to_csv, ipa_vowels

def filter_iambic_bisyllabic_words(df):
    filter_bisyl = [True if l==2 else False for l in df.rep_model.apply(len) ]#df.rep_model.apply(len) #and df.rep_model[1]
    #print(filter_iamb)
    filtered = df[filter_bisyl]
    filter_iamb = [r[1] for r in filtered.rep_model]
    return filtered[filter_iamb] #Second thing returns booleans, we are interested when these are True
    
def filter_trisyllabic_words(df):
    filter_trisyl = [True if l==3 else False for l in df.rep_model.apply(len) ]#df.rep_model.apply(len) #and df.rep_model[1]
    #print(filter_iamb)
    return df[filter_trisyl]

def add_heavy_fin_syl_column(df):
    df['heavy_final_syl'] = df.model.apply(is_final_syllable_superheavy)

def iambic_bysyl_investigation(df):
    iamb_bisyl = filter_iambic_bisyllabic_words(df)
    add_heavy_fin_syl_column(iamb_bisyl)
    print(iamb_bisyl)
    print(np.sum(iamb_bisyl.heavy_final_syl))
    print(iamb_bisyl[ [not b for b in iamb_bisyl.heavy_final_syl] ])

#write_df_to_csv('iamb_bisyl.csv', filter_iambic_bisyllabic_words(df))


def trisyl_investigation(df):
    # main function to collect trisyllabic words
    df_trisyl = filter_trisyllabic_words(df)
    write_df_to_csv('trisyl.csv', df_trisyl)
    df_trisyl_unique = df_trisyl.drop_duplicates(subset = ["word"])
    write_df_to_csv('trisyl_unique.csv', df_trisyl_unique)
    
def collect_unique_words(df):
    '''
    Collects all unique words in the data set
    
    df: complete data set including representations
    returns: set of words (in IPA)
    '''
    words = set()
    for word in df['model']:
        words.add(word)
    return words

def make_df_words_repr(words):
    '''
    Make new dataframe with just the words (in IPA) and the representation
    
    words: set of words (in IPA)
    returns: dataframe with word and repr of word
    '''
    df = pd.DataFrame(columns=['word','representation'])
    for word in words:
        df = pd.concat([df, pd.DataFrame.from_records([{'word': word, 'representation': build_syllable_representation(word)}])], ignore_index=True)
    return df

def calculate_nr_word_types(df):
    '''
    calculates the number of occurrences of each word type
    
    df: dataframe with word (in IPA) and stringified representation
    returns: counts of the representation
    '''
    # Lists are not hashable, so we stringify the list representation, which is hashable
    strings = df['representation'].apply(stringify_representation)
    return strings.value_counts()

def word_type_investigation(df):
    words = collect_unique_words(df)
    words_reprs = make_df_words_repr(words)
    counts = calculate_nr_word_types(words_reprs)
    print(counts)

def collect_disyl_iambs(df):
    table_df = df[df.rep_model.apply(lambda x: len(x) == 2 and not x[0] and x[1])]
    print(table_df)
    print(len(table_df))

def collect_trunc_bisyllables(df):
    print(df.rep_model.apply(lambda x: len(x) == 2))
    table_df = df[df.rep_model.apply(lambda x: len(x) == 2)]
    table_df = table_df[table_df.rep_realization.apply(lambda x: len(x) == 1)]
    write_df_to_csv('truncated_bisyllables.csv', table_df)
    print(table_df)

def is_final_syllable_heavy(word):
        if word[-1] in ipa_vowels:
            # if the last letter is a vowel, we only have a heavy syllable if it is a diphtong, so if the letter before it is also a vowel
            return word[-2] in ipa_vowels
        if word[-2] == 'ə':
            return False
        else: #so final letter in agnostic_symbols or consonants
            return True

def collect_heavy_trochees(df):
    table_df = df[df.rep_model.apply(lambda x: len(x) == 2)]
    table_df = table_df[table_df.model.apply(lambda x: is_final_syllable_heavy(x))]
    table_df = table_df[table_df.rep_model.apply(lambda x: not x[1])]
    write_df_to_csv('heavy_trochees_all.csv', table_df)


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from Wordlist import AllWordList, UniqueWordList, leng
from Word import Word
from tolerance import tolerance_formula_plot

class ChildDevelopment:
    '''
    Object that tracks the entire development of a child
    '''
    
    def __init__(self, name):
        '''
        name: child's name (just for bookkeeping purposes)
        
        wordlists and complete_wordlists are lists of WordLists
        '''
        self.name = name
        self.wordlists = []
        self.complete_wordlists = []
    
    
    def add_wordlist(self, wordlist, complete = False):
        '''
        Appends wordlist to the wordlists of the child
        
        wordlist: the wordlist to be added
        '''
        if not complete:
            self.wordlists.append(wordlist)
        else: 
            self.complete_wordlists.append(wordlist)

    def collect_ages(self):
        '''
        Collects all the ages of the different wordlists and saves in ages attribute
        '''
        self.ages = []
        for wordlist in self.complete_wordlists:
            self.ages.append(wordlist.age)
        
    def calculate_total_vocab_dev(self):
        '''
        Calculates the development of the vocabulary size, i.e. how the vocabulary grows through time
        
        returns: list of cumulative vocabulary sizes
        
        Todo: Add something similar for the dates so that we have those
        '''
        development = []
        total_wordlist = set()
        for wordlist in self.wordlists:
            
            for word in wordlist.wordlist:
                total_wordlist.add(word)
            development.append(len(total_wordlist))
        return development

    
    def calculate_development_by_patterns(self, patterns):
        '''
        Calculates the wordlists for a list of patterns and the total development
        For efficiency, this is done at once (building wordlists is expensive)
        
        patterns: the patterns one wants the developments of
        return: list of developments for the patterns
        '''
        developments_counts = {}
        developments = {}
        
        for p in patterns:
            developments[p] = set()
            developments_counts[p] = []
        
        
        for wordlist in self.wordlists:
            for word in wordlist.wordlist:
                for p in patterns:
                    if word.matches_pattern(p):
                        developments[p].add(word)
            for p in patterns:
                developments_counts[p].append(len(developments[p]))
        
        return developments_counts, developments
    
    def calculate_development_by_patterns_tolerance(self, patterns):
        '''
        Calculates the wordlists for a list of patterns and the total development
        For efficiency, this is done at once (building wordlists is expensive)
        
        patterns: the patterns one wants the developments of
        return: list of developments for the patterns
        
        format of developments:
                dictionary:
                { 'FT' :  (set, {'T': set, 'TF': set} ),
                  'TF' :  (set, {'T': set, 'TF': set} )
                }
        format of developments_counts: 
            dictionary:
                { 'FT' :  ([], {'T': [], 'TF': []} ),
                  'TF' :  ([], {'T': [], 'TF': []} )
                }
        '''
        developments_counts = {}
        developments = {}
        
        for p in patterns:
            d = {}
            d_counts = {}
            for sub_p in patterns[p]:
                d[sub_p] = set()
                d_counts[sub_p] = []
            developments[p] = (set(), d)
            developments_counts[p] = ([], d_counts)
        
        
        for wordlist in self.wordlists:
            for word in wordlist.wordlist:
                for p in patterns:
                    if word.matches_pattern(p):
                        developments[p][0].add(word)
                    for sub_p in patterns[p]:
                        if word.matches_pattern(sub_p):
                            developments[p][1][sub_p].add(word)
            for p in patterns:
                developments_counts[p][0].append(len(developments[p][0]))
                for sub_p in patterns[p]:
                    developments_counts[p][1][sub_p].append(len(developments[p][1][sub_p]))
        
        return developments_counts, developments
        
    def calculate_progress_of_patterns_old(self, goal_patterns, real_patterns):
        '''
        Calculates, through time, how certain 
        
        Idea: instead of separate goal_pattern, make real_patterns linked to goal_pattern so no
        need to fill in same goal pattern twice
        '''
        goal_counts = {}
        real_counts = {}
        
        for i, p in enumerate(goal_patterns):
            goal_counts[p] = np.zeros(len(self.complete_wordlists))
            real_counts[real_patterns[i]] = np.zeros(len(self.complete_wordlists))
        
        for j, wordlist in enumerate(self.complete_wordlists):
            for word in wordlist.wordlist:
                for i, p in enumerate(goal_patterns):
                    # loop through the goal_patterns and count how many of those occurred in the data set
                    # Then count how many of them had the real_pattern as well
                    
                    if word.matches_pattern(p):
                        goal_counts[p][j] += 1
                        if word.matches_pattern(real_patterns[i], model = False): # If realizations matches the corresponding real pattern
                            real_counts[real_patterns[i]][j] += 1
                            
        return goal_counts, real_counts
    
    def calculate_progress_of_patterns(self, patterns):
        '''
        Calculates, through time, how often certain patterns occur
        '''
        #iamb_bisyl_phases = 
        #patterns = {'FT': ['T', 'TF', 'TT', 'FT', 'AA']}
        
        # Goal structure:
        # dictionary:
        # { 'FT' :  ([], {'T': [], 'TF': [] } ),
        #   'TF' :  ([], {'T': [], 'TF': [] } )
        # }
        
        counts = {}
        
        for p in patterns:
            counts[p] = (np.zeros(len(self.complete_wordlists)), {})
            for rp in patterns[p]:
                counts[p][1][rp] = np.zeros(len(self.complete_wordlists))
        
        #for 
        
        for j, wordlist in enumerate(self.complete_wordlists):
            for word in wordlist.wordlist:
                for p in patterns:
                    # loop through the patterns and count how many of those occurred in the data set
                    # Then count how many of them had the real_pattern as well
                    
                    if word.matches_pattern(p):
                        counts[p][0][j] += 1
                        for real_pat in patterns[p]:
                            if word.matches_pattern(real_pat, model = False): # If realizations matches the corresponding real pattern
                                counts[p][1][real_pat][j] += 1
                            
        return counts
    
    
    def plot_vocab_dev(self, patterns):
        '''
        Plots the vocabulary development of a child, showing the size of the vocabulary patterns
        '''
        developments_counts, developments = self.calculate_development_by_patterns(patterns)
        total_dev = self.calculate_total_vocab_dev()
                
        plt.plot(self.ages, total_dev, label='Total vocabulary')
        for p in patterns:
            plt.plot(self.ages, developments_counts[p], label=p)
        plt.title('Development of ' + self.name)
        plt.legend()
        plt.show()
    
    def plot_vocab_dev_tolerance(self, patterns, ax=None, xlim=None, title=True, single_plot=False):
        '''
        Plots the tolerance levels for the patterns specified in patterns
        
        Expected patterns structure:
                dictionary:
                { 'FT' :  ['T', 'TF'],
                  'TF' :  ['T', 'TF', 'FT']
                }
        '''
        if ax is None:
            ax = plt.gca()
        
        developments_counts, developments = self.calculate_development_by_patterns_tolerance(patterns)
        total_dev = self.calculate_total_vocab_dev()
                
        ax.plot(self.ages, total_dev, label='Total vocabulary')
        for p in patterns:
            ax.plot(self.ages, developments_counts[p][0], label=p)
            for sub_p in patterns[p]:
                ax.plot(self.ages, developments_counts[p][1][sub_p], label=sub_p)
            ax.plot(self.ages, tolerance_formula_plot(developments_counts[p][0]), label="Tolerance of {}".format(p), linestyle='dotted')
        
        if title:
            ax.title.set_text('Development of ' + str(self.name))
        ax.set(xlabel="Age (in months)", ylabel="Vocabulary size")
        if xlim is not None:
            ax.set_xlim(xlim)
        if single_plot:
            ax.legend()
        return 
    
    def build_complete_wordlists(self, df):
        '''
        fills the complete_wordlists attribute based on the words in df
        
        df: the complete dataframe (with representations)
        '''
        if self.name is None:
            df_child = df
            indices = df.index
        else:
            df_child = df[df['Name'] == self.name]
            indices = df[df['Name'] == self.name].index
        if len(df_child) == 0: 
            return
        prev_time = df_child.at[indices[0],'Age']
        wordlist = AllWordList(prev_time)
        for index, data_point in df_child.iterrows(): # Might be slow, see https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
            time = data_point['Age']
            if prev_time != time: 
                self.add_wordlist(wordlist, complete = True)
                wordlist = AllWordList(time)

            word = Word(data_point['word'], data_point['model'], data_point['realization'], data_point['rep_model'], data_point['rep_realization'])
            wordlist.add_word(word)

            prev_time = time
        self.complete_wordlists.sort()
        
        self.collect_ages()
    
    
    def plot_count_patterns(self, counts, mode='moving_average', ax=None, word=None, xlim=None, colors = None, 
                            window_size=None, single_plot=False, xlabel=True, title=True, append_to_title=""):
        '''
        Plots the counts over time. 
        
        counts: per wordlist the count of that wordlist for the patterns specified
            Expected counts structure:
                dictionary:
                { 'FT' :  ([], {'T': [], 'TF': [] } ),
                  'TF' :  ([], {'T': [], 'TF': [] } )
                }
        mode: plot mode, options:
            absolute: the simple total counts
            relative: without the main model pattern, plots the counts of the realized subpatterns relative to the main pattern
            per_100: total counts per 100 words (so divided by total words in that wordlist)
            moving_average: moving average of total counts
            per_100_moving: counts per 100 words averaged by moving average
        '''
        if ax is None:
            ax = plt.gca()
        
        if self.name is None:
            window = 25
        else: 
            window = 4
        if window_size is not None:
            window = window_size
        
        if mode == 'relative' or mode == 'relative_moving':
            ax.set_ylim([0.0, 1.0])
        
        for p in counts:
            if mode == 'absolute':
                p_plot = counts[p][0]
            elif mode == 'per_100':
                lengths = list(map(leng, self.complete_wordlists))
                p_plot = (counts[p][0]/lengths)*100
            elif mode == 'moving_average':
                df_count_p = pd.DataFrame(counts[p][0])
                p_plot = df_count_p[0].rolling(window, min_periods=1).mean().to_numpy()
            elif mode == 'per_100_moving':
                lengths = list(map(leng, self.complete_wordlists))
                df_count_p = (pd.DataFrame(counts[p][0])[0]/lengths)*100
                p_plot = df_count_p.rolling(window, min_periods=1).mean().to_numpy()
            elif mode != 'relative' and mode != 'relative_moving':
                raise ValueError("Mode '{}' is an unknown graphing type".format(mode))
            
            if mode != 'relative' and mode != 'relative_moving':
                if colors is None:
                    ax.plot(self.ages, p_plot, label="model {}".format(p), marker='o')
                else:
                    ax.plot(self.ages, p_plot, label="model {}".format(p), marker='o', c=colors['m'+p])
            
            for rp in counts[p][1]:
                if mode == 'absolute':
                    rp_plot = counts[p][1][rp]
                elif mode == 'relative':
                    rp_plot = counts[p][1][rp]/counts[p][0]
                elif mode == 'relative_moving':
                    df_count_rp = pd.DataFrame(counts[p][1][rp]/counts[p][0])
                    rp_plot = df_count_rp[0].rolling(window, min_periods=1).mean().to_numpy()
                elif mode == 'per_100':
                    rp_plot = (counts[p][1][rp]/lengths)*100
                elif mode == 'moving_average':
                    df_count_rp = pd.DataFrame(counts[p][1][rp])
                    rp_plot = df_count_rp[0].rolling(window, min_periods=1).mean().to_numpy()
                elif mode == 'per_100_moving':
                    df_count_rp = ((pd.DataFrame(counts[p][1][rp]))[0]/lengths)*100
                    rp_plot = df_count_rp.rolling(window, min_periods=1).mean().to_numpy()
                
                if colors is None:
                    ax.plot(self.ages, rp_plot, label="realization {}".format(rp), marker='o')
                else:
                    ax.plot(self.ages, rp_plot, label="realization {}".format(rp), marker='o', c=colors['r'+rp])
        if title:
            if self.name is None:
                name = "all children"
            else: 
                name = self.name
            
            if word is not None:
                ax.title.set_text('Dev. of {} for word "{}" ({}){}'.format(name, word, mode, append_to_title))
            else:
                ax.title.set_text('Development of {}{}'.format(name, append_to_title))
        if xlabel:
            ax.set(xlabel="Age (in months)")
        ax.set(ylabel="Occurences ({})".format(mode))
        if xlim is not None:
            ax.set_xlim(xlim)
        if single_plot:
            ax.legend()
        return

def build_wordlists_for_child(name, df):
    '''
    builds the child development object and fills it with word lists through time
    Assumes df is not shuffled (i.e. that the words from the same time point are next to each other)
    
    name: child name
    df: complete dataframe
    returns: child development object
    
    TODO: Maybe move to __init__ of child
    '''
    if name is None:
        df_child = df
        indices = df.index
    else:
        df_child = df[df['Name'] == name]
        indices = df[df['Name'] == name].index
    #print(df_child)
    if len(df_child) == 0:
        return 
    prev_time = df_child.at[indices[0],'Age']
    child_dev = ChildDevelopment(name)
    wordlist = UniqueWordList(prev_time)
    for index, data_point in df_child.iterrows(): # Might be slow, see https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
        #print(data_point)
        time = data_point['Age']
        if prev_time != time: 
            child_dev.add_wordlist(wordlist)
            wordlist = UniqueWordList(time)
        
        word = Word(data_point['word'], data_point['model'], data_point['realization'], data_point['rep_model'], data_point['rep_realization'])
        wordlist.add_word(word)
        
        prev_time = time
    child_dev.wordlists.sort()
    return(child_dev)

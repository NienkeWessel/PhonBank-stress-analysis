import re


class WordList:
    '''
    Object that generates a word list with all words the child knows at a certain point in time
    '''
    def __init__(self, time):
        '''
        time: the point in time to which this wordlist refers
        '''
        pass
        
    def __cmp__(self, other):
        return cmp(self.age, other.age)
    
    def __lt__(self, other):
        return self.age < other.age
    
    def __repr__(self):
        return "%s with length %s" % (self.age, len(self.wordlist))
    
    def add_word(self, word):
        pass

    def add_prev_state_wordlist(self, prev_wordlist):
        for word in prev_wordlist.wordlist:
            self.add_word(word)
    
    def parse_age(self):
        numbers = re.findall('\d+', self.time)
        # the age in months with a approximation for the number of days
        return float(numbers[0])*12 + float(numbers[1]) + float(numbers[2])/31.0

def leng(wordlist):
    return len(wordlist.wordlist)


class UniqueWordList(WordList):
    '''
    WordList that only saves unique words
    '''
    
    def __init__(self, time):
        '''
        time: the point in time to which this wordlist refers
        '''
        self.time = time
        self.age = self.parse_age()
        self.wordlist = set()
    
    def add_word(self, word):
        self.wordlist.add(word)

class AllWordList(WordList):
    '''
    WordList that saves all words
    '''
    
    def __init__(self, time ):
        '''
        time: the point in time to which this wordlist refers
        '''
        self.time = time
        self.age = self.parse_age()
        self.wordlist = []    
    
    def add_word(self, word):
        self.wordlist.append(word)








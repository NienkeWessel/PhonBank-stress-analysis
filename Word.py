from utils import ipa_vowels, agnostic_symbols

class Word:
    '''
    Object that defines a word with five attributes:
    
    written: word in Latin script
    model: model IPA transcription
    realization: IPA transcription of realization by child
    rep_model: stress representation of model
    rep_realization: stress representation of realization by child
    '''
    
    def __init__(self, written, model, realization, rep_model, rep_realization):
        self.written = written
        self.model = model
        self.realization = realization
        self.rep_model = rep_model
        self.rep_realization = rep_realization
    
    def __eq__(self, other):
        return self.written == other.written
    
    def __hash__(self):
        return self.written.__hash__()

    def is_bisyl(self):
        return len(self.rep_model) == 2
    
    def is_iambic_bisyl(self):
        if len(self.rep_model) == 2:
            return self.rep_model[1]
        else:
            return False 
    
    def is_final_syllable_heavy(self):
        if self.model[-1] in ipa_vowels:
            # if the last letter is a vowel, we only have a heavy syllable if it is a diphtong, so if the letter before it is also a vowel
            return self.model[-2] in ipa_vowels
        else: #so final letter in agnostic_symbols or consonants
            return True
    
    def is_final_syllable_superheavy(self):
        '''
        if final is vowel, then check if prefinal is also vowel (or in agnostic and then the one before)
        if final is consonant, then check if prefinal is consonant. 
            If consonant, then superheavy
            If agnostic, check the one before and repeat
            If vowel, check the one before; if vowel again, then superheavy. If agnostic, check the one before. If consonant, not superheavy
        '''

        old_word = self.model
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

    
    def matches_pattern(self, pattern, model = True):
        '''
        Calculates whether the word matches the stress pattern. Pattern characters:
            T: stressed syllable
            F: unstressed syllable
            @: syllable ending in schwa
            +: concatenates two possible patterns; function will return true if either matches
            H: heavy and stressed syllable
            h: heavy and unstressed syllable
            N: nonheavy and stressed syllable
            n: nonheavy and unstressed syllable
        
        pattern: string of F(alse) and T(rue) or A(gnostic) indicating the stress placement
        model: boolean which indicates whether to match to the model representation (True) or realization representation (False)
        Agnostic (or any other symbol) can be used to indicate that one does not care about the stress placement
        
        return: 
        '''
        if model:
            word = self.rep_model
        else:
            word = self.rep_realization
        
        
        # First part is for plusses in the string (e.g. 'AA+AAA') (which recursively checks for the different parts)
        if '+' in pattern:
            parts = pattern.split('+')
            return any([self.matches_pattern(part, model=model) for part in parts])
        
        # Second part is for normal strings without plusses
        
        
        # Initial check for length match. If not equal, no point in persuing (and prevents out of bound errors later on)
        if len(pattern) != len(word):
            return False
        
        for i,c in enumerate(pattern):
            if c == 'T':
                if not word[i]:
                    return False
            if c == 'F': 
                if word[i] or ((self.realization[-1] == 'ə') and i == len(pattern)-1): # we want to exclude the schwa ending words here
                    return False
            if c == '@':
                if not (self.realization[-1] == 'ə'):
                    return False
            if c == 'H':
                if not word[i] or not self.is_final_syllable_superheavy():
                    return False
            if c == 'h':
                if word[i] or not self.is_final_syllable_superheavy():
                    return False
            if c == 'N':
                if not word[i] or self.is_final_syllable_superheavy():
                    return False
            if c == 'n':
                if word[i] or self.is_final_syllable_superheavy():
                    return False
        return True

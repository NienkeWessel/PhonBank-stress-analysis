import unittest

from utils import build_syllable_representation, is_final_syllable_heavy, is_final_syllable_superheavy


class MyTest(unittest.TestCase):
    def test_build_syllable_representation(self, secondary=False):
        '''
        Tests the build_syllable_representation function with different examples
        Also used to see if something breaks after adjusting
        '''
    
        if not secondary:
            #one syllable word, with bridge
            self.assertEqual([True], build_syllable_representation('ˈbu̠t͡s'))
            
            #simple two syllable words with different stress
            self.assertEqual([False, True], build_syllable_representation('koːˈlɛin'))
            self.assertEqual([True, False], build_syllable_representation('ˈpukə'))
            self.assertEqual([True, False], build_syllable_representation('ˈɡʊkʊk'))
            
            #other
            self.assertEqual([True, False, False], build_syllable_representation('ˈʔaːˌkleːdə'))
            
            self.assertEqual([True, False], build_syllable_representation('ˈpinoːŭ'))
            self.assertEqual([True, False, False], build_syllable_representation('ˈzeˌot͡jɑ̈s'))
            self.assertEqual([True, False], build_syllable_representation('ˈnæˑŋi'))
            self.assertEqual([True, False, True, False], build_syllable_representation('ˈzikəˈoto'))
            self.assertEqual([True, False, True], build_syllable_representation('ˈkʁ̣̆oːkoˈdɪ͜ŭ'))
            
            self.assertEqual([False, True], build_syllable_representation('ʔɑˈtoː'))
            self.assertEqual([False, False], build_syllable_representation('ˌʀʉmpi'))
            
            self.assertEqual([True, False], build_syllable_representation('ˈfɪsˌhɶχ'))
            self.assertEqual([True, False], build_syllable_representation('ˈtɛ̈iχəs'))
            
            

            
            

    def test_is_final_syllable_heavy(self):
        self.assertEqual(True, is_final_syllable_heavy('ˈzeˌot͡jɑ̈s'))
        self.assertEqual(True, is_final_syllable_heavy('koːˈlɛin'))
        self.assertEqual(True, is_final_syllable_heavy('koˈnɛi'))
        self.assertEqual(False, is_final_syllable_heavy('ˈpukə'))
        self.assertEqual(True, is_final_syllable_heavy('ˈbu̠t͡s'))
        self.assertEqual(True, is_final_syllable_heavy('kˈɑpχː'))
        self.assertEqual(True, is_final_syllable_heavy('neː'))
        self.assertEqual(True, is_final_syllable_heavy('fiˈjoʋ'))
        
    def test_is_final_syllable_superheavy(self):
        self.assertEqual(False, is_final_syllable_superheavy('ˈzeˌot͡jɑ̈s'))
        self.assertEqual(True, is_final_syllable_superheavy('koːˈlɛin'))
        self.assertEqual(False, is_final_syllable_superheavy('koˈnɛi'))
        self.assertEqual(False, is_final_syllable_superheavy('ˈpukə'))
        self.assertEqual(True, is_final_syllable_superheavy('ˈbu̠t͡s'))
        self.assertEqual(True, is_final_syllable_superheavy('kˈɑpχː'))
        self.assertEqual(False, is_final_syllable_superheavy('neː'))
        self.assertEqual(False, is_final_syllable_superheavy('fiˈjoʋ'))
        self.assertEqual(True, is_final_syllable_superheavy('ˈḅɔːʃ̟'))
        self.assertEqual(False, is_final_syllable_superheavy('ˈmɑm'))
        self.assertEqual(True, is_final_syllable_superheavy('koːˈlɛːn'))
        

test = MyTest()
test.test_build_syllable_representation()
test.test_is_final_syllable_superheavy()
        

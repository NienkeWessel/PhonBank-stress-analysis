'''
The code is made to work on many different files from the Childes Dataset
To easily switch between files, the following dictionaries contain all
necessary information for the rest of the code to make the switching easily
possible and prevent you from having to change it at multiple places in the
code
'''

file_names_read = {
    'Grimm': "Grimm.pkl",
    'CLPF': "CLPF.pkl",
    'FoxBoyer' : "FoxBoyer.pkl",
    'Bracci' : 'Bracci.pkl',
    'ComptonPater' : 'ComptonPater.pkl',
    'Goad' : 'Goad.pkl',
    'Inkelas' : 'Inkelas.pkl',
    'Providence' : 'Providence.pkl',
    'Smith' : 'Smith.pkl',
    'Penney' : 'Penney.pkl',
    'Kuwaiti' : 'Kuwaiti.pkl'
}
file_names_write = {
    'Grimm': "Grimm.csv",
    'CLPF': "CLPF.csv",
    'FoxBoyer' : "FoxBoyer.csv",
    'Bracci' : 'Bracci.csv',
    'ComptonPater' : 'ComptonPater.csv',
    'Goad' : 'Goad.csv',
    'Inkelas' : 'Inkelas.csv',
    'Providence' : 'Providence.csv',
    'Smith' : 'Smith.csv',
    'Penney' : 'Penney.csv',
    'Kuwaiti' : 'Kuwaiti.csv'
}

FoxBoyer_names = []
for i in range(1,33):
    string = 'TD PL-II C'
    if len(str(i))>1:
        string += str(i)
    else:
        string += "0" +str(i)
    FoxBoyer_names.append(string)

children_names_file = {
    'Grimm': ['Sandra', 'Wiglaf', 'Eleonora', 'Nele'],
    'CLPF': ['Catootje', 'David', 'Elke', 'Enzo', 'Eva', 'Jarmo', 'Leon', 'Leonie', 'Noortje', 'Robin', 'Tirza', 'Tom'],
    'CLPF_giraf' : ['Catootje', 'Tirza', 'Robin', 'Leon', 'Tom'],
    'FoxBoyer' : FoxBoyer_names,
    'Bracci' : ['3028', '3025', '1005', '3022', '3023', '1006', '3024', '2017', '2011', '2027', '1002', '2008', '2015', '1001', '1003'],
    'ComptonPater': ['Julia', 'Sean', 'Trevor'],
    'Goad' : ['Julia', 'Sonya'],
    'Inkelas' : ['E'],
    'Providence' : ['Alex', 'Ethan', 'Lily', 'Naima', 'Violet', 'William'],
    'Smith' : 'Amahl',
    'Penney' : ['T42', 'D10', 'D05', 'T19', 'T49', 'T44', 'D38', 'T67', 'D23', 'D37', 'T34', 'T12', 'T68', 'D52', 'T17', 'T21', 'T22', 'T02', 'T58', 'T65', 'D09', 'D43', 'D11', 'T18', 'D08', 'T55'],
    'Kuwaiti' : ['Jamal', 'Jawad', 'Fatma', 'Mask', 'Khaled', 'Khald', 'Dana',
       'Fatema', 'Areej', 'Kawthar', 'Mohammad', 'Najat', 'Zayed',
       'Yousef', 'Mohamed', 'Ameena', 'Abdulaziz', 'Hanayen Almatouq',
       'Muneera ', 'Khalifa', 'Reem Alganem', 'Fares ', 'Sabah ',
       'Bader ', 'Gader', 'Ahmad', 'Alia', 'Ratage ', 'Sara', 'Zainab',
       'Mariam', 'Malak', 'Aysha', 'Abdulrahman', 'Alkady', 'Fajar',
       'Fahad Jammal', 'Omar', 'Hessa', 'Mousa', 'Abdullah', 'Jood',
       'Fahad', 'Sood', 'Fanar', 'Hadeel', 'Ahmed', 'lulwa', 'Zayan',
       'Dorar', 'Traky', 'Sulaiman', 'Haya', 'Falah', 'Farah', 'Aseel']
}

plot_settings = {
    'Grimm' : {
        'nr_per_row' : 2,
        'window_size' : None,
        'padding_top' : 0.01,
    },
    'CLPF' : {
        'nr_per_row' : 3,
        'window_size' : None,
        'padding_top' : -0.05,
    },
    'Providence' : {
        'nr_per_row' : 3,
        'window_size' : 10,
        'padding_top' : 0.01,
    },
    'Bracci' : {
        'nr_per_row' : 2,
        'window_size' : None,
        'padding_top' : 0.01,
    },
    'FoxBoyer' : {
        'nr_per_row' : 3,
        'window_size' : None,
        'padding_top' : -0.05,
    }
    
}



'''
These dictionaries contain different possible patterns that can be used in analyses. Currently, only the
Fikkert patterns are used and work properly. Use other patterns at your own risk!
'''
analysis_dictionary = {
    'Fikkert' : {
        'patterns' : {'FT': ['T+F', 'T@', 'TF', 'FTF', 'TT',  'FT']},
        'patterns_heavy' : {'TF': ['FT']},
        'tolerance' : {'AA': ['TF', 'FT']},
        'elab_tol' : {'FT+TF' : ['FT']},
        'overgen_iamb' : {'Th' : ['Th', 'FH']},
        'color_dict_patterns' : {
            'mFT' : '#b51963',
            'rT+F' : '#c44601', 
            'rT@' : '#f57600', 
            'rTF' : '#8babf1', 
            'rFTF' : '#0073e6',
            'rTT' : '#054fb9',  
            'rFT' : '#89ce00'
        }
    },
    'Fikkert_WWS' : {
        'patterns' : {'FFT': ['T', 'T@', 'TF', 'TT', 'TFT', 'TFF', 'FFT']}, #thesis Fikkert pp. 218-
        'tolerance' : {'AAA': ['FFT']}
    },
    'Kehoe_SWS' : {
        'patterns' : {'TFT': ['T', 'TF', 'TT', 'TTT', 'FF', 'FFF', 'FT', 'TFTF', 'TFT']},
        'tolerance' : {}
    }
    
}

'''
Model pattern: TFT (SWS in paper)
Possible realizations (p. 12): T, TF, level stress (TT, TTT, FF, FFF), FT
'''


'''
These are all kinds of settings for the corpora analyzed. These are mostly used for the plotting
of specific words. 
'''

words_per_child_dict_CLPF = {
    'Catootje' : ['kapot', 'konijn', 'ballon', 'giraf', 'papier', 'banaan'],
    'Enzo' : ['kapot', 'misschien', 'ballon', 'misschien', 'muziek', 'banaan'],
    'Elke' : ['banaan', 'kapot', 'konijn'],
    'Eva' : ['kapot'],
    'Jarmo' : ['kalkoen', 'banaan'],
    'Leon' : ['gitaar', 'ballon', 'giraf', 'waarom', 'hallo'],
    'Leonie' : ['ballon', 'kapot'],
    'Tirza' : ['giraf'],
    'Tom' : ['kameel', 'trompet', 'marmot', 'giraf'],
    'Robin' : ['ballon', 'banaan']
}
words_per_child_dict_Grimm = {
    'Sandra' : ['Kamel', 'kaputt', 'Ballon', 'Gela'],
    'Wiglaf' : ['Kamel', 'Papier', 'kaputt', 'Ernie', 'Gela'],
    'Eleonora' : ['Kamel', 'kaputt', 'Ballon', 'Kakao', 'Ernie'],
    'Nele' : ['Kamel', 'kaputt', 'Ballon', 'Salat', 'Gela', 'galopp', 'Bonbons']
}
words_per_child_dict_Providence = {
    'Alex' : ['hello', 'meow', 'again', 'pretend', 'achoo', 'balloon', 'fourteen', 'balloons', 'eighteen'],
    'Ethan' : ['hello', 'again', 'caboose', 'upstairs', 'sometimes', 'into', 'away', 'balloon', 'balloons', 'inside', 'surprise', 'around'],
    'Lily' : ['hello', 'because', 'again', 'alright', 'goodbye', 'hooray', 'Shamu', 'upstairs', 'into', 'Tamar', 'inside'],
    'Naima' : ['hello', 'meow', 'because', 'Lucille', 'again', 'pretend', 'sometimes', 'giraffe', 'away', 'outside', 'until', 'raccoon'],
    'Violet' : ['hello', 'because', 'again', 'before'],
    'William' : ['hello', 'because', 'again', 'alright', 'caboose', 'away', 'guitar', 'today', 'outside'],
}

xlim_per_child_dict_CLPF = {
    'Catootje' : [22,32],
    'David' : [25.5, 28],
    'Enzo' : [22,32],
    'Elke' : [19,28],
    'Eva' : [15, 30],
    'Jarmo' : [20, 30],
    'Leon' : [21, 34],
    'Leonie' : [21, 25],
    'Noortje' : [24, 36],
    'Tirza' : [15, 30],
    'Tom' : [15, 30],
    'Robin' : [18, 28]
}
xlim_per_child_dict_Grimm = {
    'Sandra' : [19,24],
    'Wiglaf' : [17,26],
    'Eleonora' : [14,23],
    'Nele' : [18,25]
}
xlim_per_child_dict_Providence = {
    'Alex' : [16,40],
    'Ethan' : [14,36],
    'Lily' : [20,50],
    'Naima' : [10,45],
    'Violet' : [22,50],
    'William' : [16,41],
}

words_per_child_dict = {
    'CLPF' : words_per_child_dict_CLPF,
    'Grimm' : words_per_child_dict_Grimm,
    'FoxBoyer' : {None: ['kaputt', 'Geschenk', 'Gespenst']},
    'Bracci' : {None: ['Zitroun', 'Gespenst', 'Banane', 'Giraff']},
    'Providence' : words_per_child_dict_Providence
}

xlim_per_child_dict = {
    'CLPF' : xlim_per_child_dict_CLPF,
    'Grimm' : xlim_per_child_dict_Grimm,
    'FoxBoyer' : {None: [20,120]},
    'Bracci' : {None: [38, 53]},
    'Providence' : xlim_per_child_dict_Providence
}

wordlevel_child_names = {
    'CLPF' : ['Catootje', 'Enzo', 'Elke', 'Eva', 'Jarmo', 'Leon', 'Leonie', 'Robin', 'Tirza', 'Tom'],
    'Grimm' : ['Sandra', 'Wiglaf', 'Eleonora', 'Nele'],
    'FoxBoyer' : [None],
    'Bracci' : [None],
    'Providence' : ['Alex', 'Ethan', 'Lily', 'Naima', 'Violet', 'William']
}






import numpy as np

def reproduce_tables(df, children_names):
    '''
    Reproduces the data from the tables from Fikkert, p. 25
    That is, function calculates the total amount of model bisyllabic words and calculates 
    the percentage that is realized in a truncated way, differentiating between iambic and
    trochaic words. 
    
    df: the complete data from with representations
    children_names: the names of the children for which the calculations need to be done
    returns: dictionary with the child names and the totals of model bisyllabic words and truncated forms
    '''
    data_per_child = {}
    for child in children_names:
        ch_data = df[df['Name'] == child]
        #print(ch_data)
        total_bisyl_iamb = 0
        total_bisyl_troc = 0
        trunc_bisyl_iamb = 0
        trunc_bisyl_troc = 0
        len_two_iamb = 0
        len_two_troc = 0
        stress_error_iamb = 0
        stress_error_troc = 0
        for index, data_point in ch_data.iterrows(): 
            if len(data_point['rep_model'])== 2:
                #if not data_point['rep_model'][0] and data_point['rep_model'][1]:
                if data_point['rep_model'][1]:
                    total_bisyl_iamb += 1
                    if len(data_point['rep_realization']) == 1:
                        trunc_bisyl_iamb += 1
                    if len(data_point['rep_realization']) ==2:
                        len_two_iamb += 1              
                        if not (data_point['rep_realization'][1] and not data_point['rep_realization'][0]):
                            stress_error_iamb += 1
                #if data_point['rep_model'][0] and not data_point['rep_model'][1]:
                if data_point['rep_model'][0]:
                    total_bisyl_troc += 1
                    if len(data_point['rep_realization']) == 1:
                        trunc_bisyl_troc += 1
                    if len(data_point['rep_realization']) ==2: 
                        len_two_troc += 1
                        if not (data_point['rep_realization'][0] and not data_point['rep_realization'][1]):
                            stress_error_troc += 1
        data_per_child[child] = (total_bisyl_iamb, total_bisyl_troc, trunc_bisyl_iamb, trunc_bisyl_troc, len_two_iamb, len_two_troc, stress_error_iamb, stress_error_troc)
    return data_per_child

def pretty_print_tables(data_per_child, children_names):
    '''
    Prints the percentages of truncated bisyllabic trochees and iambs
    
    data_per_child: dictionary with the child names and the totals of model bisyllabic words and truncated forms
    children_names: the names of the children for which the data needs to be printed
    
    '''
    totals = np.zeros(8)
    print("\n")
    print("----- Table 1: Truncation -----")
    for child in children_names:
        data = data_per_child[child]
        print(child, ":")
        print("trochees: {} ({}/{})".format((data[3]/data[1])*100, data[3], data[1] ) )
        print("iamben: {} ({}/{})".format((data[2]/data[0])*100, data[2], data[0] ) )#trunc iamb divided by total iamb
        totals += data
    print("Totals:")
    print("trochees: {} ({}/{})".format((totals[3]/totals[1])*100, totals[3], totals[1] ) )
    print("iamben: {} ({}/{})".format((totals[2]/totals[0])*100, totals[2], totals[0] ) )
    
    print("\n")
    print("----- Table 2: Stress errors -----")
    for child in children_names:
        data = data_per_child[child]
        print(child, ":")
        print("trochees: {} ({}/{})".format((data[7]/data[5])*100, data[7], data[5] ) )
        print("iamben: {} ({}/{})".format((data[6]/data[4])*100, data[6], data[4] ) )
    print("Totals:")
    print("trochees: {} ({}/{})".format((totals[7]/totals[5])*100, totals[7], totals[5] ) )
    print("iamben: {} ({}/{})".format((totals[6]/totals[4])*100, totals[6], totals[4] ) )
    
def pretty_print_tables_latex(data_per_child_norm, data_per_child_filtered, children_names, corpus_name):
    '''
    Prints the tables in latex ready format for easier including them in latex papers
    '''
    
    if corpus_name == 'CLPF':
        extra_rows = " & &"
    else: 
        extra_rows = ""
    
    totals_n = np.zeros(8)
    totals_f = np.zeros(8)
    for child in children_names:
        totals_n += data_per_child_norm[child]
        totals_f += data_per_child_filtered[child]
    data_per_child_norm['Totals'] = totals_n
    data_per_child_filtered['Totals'] = totals_f
    children_names = children_names + ["Totals"]

    print("----- Table 1: Truncation -----")
    for child in children_names:
        data_n = data_per_child_norm[child]
        if corpus_name == 'CLPF':
            data_f = data_per_child_filtered[child]
            filter1 = f"{round(data_f[3]/data_f[1]*100, 1)} & ({data_f[3]}/{data_f[1]})& "
            filter2 = f"{round(data_f[2]/data_f[0]*100, 1)} & ({data_f[2]}/{data_f[0]})& "
        else:
            filter1 = ""
            filter2 = ""
        print(f"{child} &{extra_rows} {filter1}" +
             f"{round(data_n[3]/data_n[1]*100, 1)} & ({data_n[3]}/{data_n[1]})" +
             f"&{extra_rows} {filter2}" +
             f"{round(data_n[2]/data_n[0]*100, 1)} & ({data_n[2]}/{data_n[0]}) \\\\")
    
    print("\n")
    print("----- Table 2: Stress errors -----")
    for child in children_names:
        data_n = data_per_child_norm[child]
        data_f = data_per_child_filtered[child]
        if corpus_name == 'CLPF':
            data_f = data_per_child_filtered[child]
            filter1 = f"{round(data_f[7]/data_f[5]*100, 1)} & ({data_f[7]}/{data_f[5]}) & "
            filter2 = f"{round(data_f[6]/data_f[4]*100, 1)} & ({data_f[6]}/{data_f[4]}) & "
        else:
            filter1 = ""
            filter2 = ""
        print(f"{child} &{extra_rows} {filter1}" +
             f"{round(data_n[7]/data_n[5]*100, 1)} & ({data_n[7]}/{data_n[5]})" +
             f"&{extra_rows} {filter2}" +
             f"{round(data_n[6]/data_n[4]*100, 1)} & ({data_n[6]}/{data_n[4]}) \\\\")
   
   
   
def filtered_table_df(df):
    filtered_df = df[df.word.apply(lambda x: not (x[-1] == 'n' and x[-2] == 'e'))]
    filtered_df = filtered_df[filtered_df.word.apply(lambda x: not (x[-1] == 'e' and x[-2] == 'j'))]
    filtered_df = filtered_df[filtered_df.model.apply(lambda x: not ('ˌ' in x))]
    return filtered_df


def run_reproduce_tables(df, children_names, corpus_name, latex=False):
    '''
    Reproduces the tables from Fikkert p. 25/Fikker 1994 (p. 201)
    '''
    data_per_child_norm = reproduce_tables(df, children_names)
    filtered_df = filtered_table_df(df)
    data_per_child_filtered = reproduce_tables(filtered_df, children_names)
    if latex:
        pretty_print_tables_latex(data_per_child_norm, data_per_child_filtered, children_names, corpus_name)
    else:
        pretty_print_tables(data_per_child_norm, children_names)
        pretty_print_tables(data_per_child_filtered, children_names)


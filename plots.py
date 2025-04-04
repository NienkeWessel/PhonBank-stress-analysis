import matplotlib.pyplot as plt
import math

from ChildDevelopment import build_wordlists_for_child
from utils import write_df_to_csv

def single_xaxis(fig, loc1, loc2):
    '''
    Makes the x-axis match on the two plots at location loc1 and loc2
    '''
    fig.axes[loc1].get_shared_x_axes().join(fig.axes[loc1], fig.axes[loc2])
    fig.axes[loc1].set_xticklabels([])
    fig.axes[loc2].autoscale()

def tight_pairs(n_cols, fig=None):
    """
    Function shamelessy stolen from the internet (but forgot to write down source)
    
    Stitches vertical pairs together.

    Input:
    - n_cols: number of columns in the figure
    - fig: figure to be modified. If None, the current figure is used.

    Assumptions: 
    - fig.axes should be ordered top to bottom (ascending row number). 
      So make sure the subplots have been added in this order. 
    - The upper-half's first subplot (column 0) should always be present

    Effect:
    - The spacing between vertical pairs is reduced to zero by moving all lower-half subplots up.

    Returns:
    - Modified fig
    """
    if fig is None:
        fig = plt.gcf()
    for ax in fig.axes:
        if hasattr(ax, 'get_subplotspec'):
            ss = ax.get_subplotspec()
            row, col = ss.num1 // n_cols, ss.num1 % n_cols
            if (row % 2 == 0) and (col == 0): # upper-half row (first subplot)
                y0_upper = ss.get_position(fig).y0
            elif (row % 2 == 1): # lower-half row (all subplots)
                x0_low, _ , width_low, height_low = ss.get_position(fig).bounds
                ax.set_position(pos=[x0_low, y0_upper - height_low, width_low, height_low])
    return fig

def create_single_legend(fig, mode, padding_top=-0.05, multi_plot=None):
    '''
    Create one legend for multiple plots
    The padding top is a bit inconvenient and might take some trial and error to get to work on different plots
    '''
    
    if mode == 'relative' or mode == 'relative_moving':
        ncol = 6
        padding_top += 0.01
    else:
        ncol = 4
    if multi_plot is None:
        lines, labels = fig.axes[0].get_legend_handles_labels()
    else:
        lines, labels = fig.axes[0].get_legend_handles_labels()
        lines2, labels2 = fig.axes[multi_plot].get_legend_handles_labels()
        for i, label in enumerate(labels2):
            if label not in labels:
                lines.append(lines2[i])
                labels.append(label)
        #lines_labels = list(set(lines_labels1 + lines_labels2))
        #lines, labels = zip(*lines_labels)
    fig.legend(lines, labels, loc='upper center', bbox_to_anchor = (0, padding_top, 1, 1), ncol=4, prop={'size': 15})

def loop_through_children(df, children_names, analysis, nr_per_row = 3, width=5, colors = None, 
                          mode='relative_moving', single_plot=False, window_size=None, padding_top=-0.05,
                          append_to_title=""):
    '''
    Loops through the children_names to make a subplot for each of them and plot it in one
    larger plot. 
    
    df: the data dataframe (it is possible to provide a subframe with only part of the data)
    children_names: the names of the children that should be plotted
    analysis: the analysis patterns which should be plotted
    nr_per_row: nr of plots per row
    '''
    
    # Create graph stuff
    try: 
        rows_necessary = int(math.ceil(len(children_names)/nr_per_row))
    except:
        rows_necessary = 1
    
    if single_plot:
        plot_height = 20
        fig = plt.figure()
        axs = fig.add_subplot(1, 1, 1)
    else:
        plot_height = 3*rows_necessary
        fig, axs = plt.subplots(rows_necessary, nr_per_row, figsize=(width*nr_per_row,plot_height))
    if not single_plot:
        axs = axs.ravel()
    
    for i, child_name in enumerate(children_names):
        child_test = build_wordlists_for_child(child_name, df)
        if child_test is None:
            continue
        child_test.build_complete_wordlists(df) 
        counts = child_test.calculate_progress_of_patterns(analysis['patterns'])
        
        if single_plot:
            axs = child_test.plot_count_patterns(counts, mode=mode, ax=axs, colors=colors, window_size=window_size, 
                                                 single_plot=single_plot, append_to_title=append_to_title)
        else:
            axs[i] = child_test.plot_count_patterns(counts, mode=mode, ax=axs[i], colors=colors, 
                                                    window_size=window_size, single_plot=single_plot, 
                                                    append_to_title=append_to_title)

    if not single_plot:
        create_single_legend(fig, mode, padding_top=padding_top)
        
    fig.tight_layout()
    fig.show()


def loop_through_children_two_modes(df, children_names, analysis, nr_per_row = 3, width=5, xlim=None, mode1='absolute',
                                    mode2='relative', colors=None, single_plot=False, window_size=None, 
                                    padding_top=-0.05, append_to_title=""):
    '''
    Plots two modes per child below each other
    '''
    
    # Create graph stuff
    plot_height = 3 * int(math.ceil(len(children_names)/nr_per_row))*2
    if single_plot:
        plot_height = 20
    fig, axs = plt.subplots(2*(int(math.ceil(len(children_names)/nr_per_row))), nr_per_row, 
                            figsize=(width*nr_per_row,plot_height))
    axs = axs.ravel()
    
    for i, child_name in enumerate(children_names):
        if xlim is not None:
            xlim_child = xlim[child_name]
        else:
            xlim_child = None
        
        child_test = build_wordlists_for_child(child_name, df)
        child_test.build_complete_wordlists(df) 
        counts = child_test.calculate_progress_of_patterns(analysis['patterns'])
        
        loc_graph = 2*i - (i%nr_per_row)
        #print(loc_graph)
        axs[loc_graph] = child_test.plot_count_patterns(counts, mode=mode1, ax=axs[loc_graph], colors=colors, 
                                                        xlim=xlim_child, window_size=window_size, 
                                                        single_plot=single_plot, xlabel=False)
        if mode2 == 'tolerance':
            axs[loc_graph + nr_per_row] = child_test.plot_vocab_dev_tolerance(analysis['elab_tol'], 
                                                                              ax=axs[loc_graph+nr_per_row], 
                                                                              xlim=xlim_child, title=False, 
                                                                              single_plot=single_plot)
        else:
            axs[loc_graph + nr_per_row] = child_test.plot_count_patterns(counts, mode=mode2, 
                                                                         ax=axs[loc_graph+nr_per_row], 
                                                                         colors=colors, xlim=xlim_child, 
                                                                         window_size=window_size, 
                                                                         single_plot=single_plot, title=False)
        
        
        single_xaxis(fig, loc_graph, loc_graph + nr_per_row)
        
    create_single_legend(fig, mode2, padding_top=padding_top, multi_plot=nr_per_row)
    
    tight_pairs(nr_per_row)
    fig.show()

def plot_per_word(df, word, children_names, analysis, save=False, colors=None, mode='absolute', single_plot=False, 
                  padding_top=-0.05, append_to_title=""):
    word_df = df[df.word.apply(lambda x: x == word)]
    if save:
        write_df_to_csv("{}_occurrences.csv".format(word), word_df)
    loop_through_children(word_df, children_names, analysis, colors=colors, mode=mode, single_plot=single_plot, 
                          padding_top=padding_top, append_to_title=append_to_title)


def loop_through_words_for_child(df, child_name, analysis, words, nr_per_row = 3, width=5, xlim=None, 
                                 mode='absolute', colors = None, padding_top=-0.05):
        
    # Create graph stuff
    plot_height = int(math.ceil(len(words)/nr_per_row))*3
    fig, axs = plt.subplots(int(math.ceil(len(words)/nr_per_row)), nr_per_row, figsize=(width*nr_per_row,plot_height))
    axs = axs.ravel()
    
    for i, word in enumerate(words):
        word_df = df[df.word.apply(lambda x: x == word)]
        child = build_wordlists_for_child(child_name, word_df)
        if child is None:
            continue
        child.build_complete_wordlists(word_df) 
        counts = child.calculate_progress_of_patterns(analysis)
        
        axs[i] = child.plot_count_patterns(counts, mode=mode, ax=axs[i], word=word, xlim=xlim, colors = colors)
        
    create_single_legend(fig, mode, padding_top=padding_top)
    fig.tight_layout()
    fig.show()






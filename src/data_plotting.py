"""
This module contains all the necessary function to plot the data. these functions are called by the ones in the data_analysis module.
"""

import os
import pickle
import warnings

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from alive_progress import alive_it

warnings.simplefilter(action='ignore', category=FutureWarning)


def plot_dict_features_from_price_file(dict_features, inplay_idx, plot_path):
    """
    This code block is used to generate a set of line plots and distribution plots for each feature in a given DataFrame.
    Each feature is both plotted as a time series and as a distribution. The point at which in-play begins is indicated with
    a vertical line in the line plot. The plots are saved to the specified path.

    Args:
        df_features (pandas.DataFrame): A DataFrame where each column is a feature to be plotted.
        inplay_idx (int): Index to represent the start of in-play in the line plot.
        plot_path (str): The path where the plots will be saved.

    """
    plt.rcParams["figure.figsize"] = (10,5)
    for feature_name, feature in dict_features.items():
        ## LINE PLOT
        # print(feature_name)
        if feature_name=="Publish time":
            plt.plot(feature, range(len(feature)), label=feature_name)
            if inplay_idx!=None:
                plt.axhline(y = inplay_idx, color = 'r', label = 'in-play')
        else:
            plt.plot(feature, label=feature_name)

            if feature_name!="In-play diff time":
                if inplay_idx!=None:
                    plt.axvline(x = inplay_idx, color = 'r', label = 'in-play')

        if "Mid price" in feature_name:
            plt.ylim(0, 15)
        if "Matched" in feature_name:
            plt.ylim(0, 20000)
        if "Last traded price" in feature_name:
            plt.ylim(0, 20)

        plt.legend()
        if "time" in feature_name and (feature_name!="Publish time"):
            plt.title(f"{feature_name} (seconds)")
        else:
            plt.title(feature_name)

        plt.xlabel("# Orders arrived")
        plt.savefig(os.path.join(plot_path, feature_name))
        plt.close()

        ## DISTRIBUTION PLOT
        ## Note: This was commented out due to too much time to calculate
        # sns.displot(feature, label=feature_name)
        # plt.legend()
        # plt.title(feature_name+" distribution")
        # plt.savefig(os.path.join(plot_path, feature_name)+"_distr")
        # plt.close()



def plot_correlation_matrix(df_features, plot_path):
    """
    This function plots the correlation matrix of the input DataFrame's features and saves the plot to a specified path.

    Args:
        df_features (pandas.DataFrame): A DataFrame whose features' correlation matrix is to be plotted.
        plot_path (str): The path where the plot will be saved.
    """
    corr_methods = ['pearson', 'kendall', 'spearman']

    for method in corr_methods:
        correlation_matrix = df_features.corr(method=method)
        mask = np.triu(correlation_matrix)
        f, ax = plt.subplots(figsize=(12, 9))
        sns.heatmap(correlation_matrix, square=False, annot=True, mask=mask)
        plt.savefig(os.path.join(plot_path, f"corr_matrix_{method}"))
        plt.close()


def plot_distr_volume_traded(dict_volume_traded, path_plot, binwidth):
    """
    This function plots a histogram of the total volume traded for different files.
    The histogram is saved to a file specified by path_plot.

    Args:
        dict_volume_traded (dict): Dictionary with keys being file names and values being the total volume traded in the corresponding file.
        path_plot (str): The path to the directory where the plot will be saved.
        binwidth (int): The size of the bins for the histogram.
    """
    list_tot_vol = [v for k, v in dict_volume_traded.items()
                    if v!=None
                    ]
    sns.displot(list_tot_vol,
                #binwidth=binwidth
                )
    plt.savefig(os.path.join(path_plot))
    plt.close()




def load_dict_from_pickle_and_plot_distr(path_pickle_file, path_plot):
    """
    This function loads a dictionary from a pickle file, retrieves the values from the dictionary,
    and creates a histogram plot of those values. The plot is saved as a file at a specified path.

    The purpose of this function is to visualize the distribution of the values saved in the pickle
    files by the function 'analyse_and_plot_price_files' of the data_analysis module, like
    'tot_volume_traded_dict.pkl' or 'pre_event_volume_traded.pkl'.

    Args:
        path_pickle_file (str): The path to the pickle file containing the dictionary.
        path_plot (str): The path where the plot file should be saved.

    Example:
        path_pickle_file = 'path/to/your/pickle/tot_volume_traded_dict.pkl'
        path_plot = 'path/to/save/your/distr_tot_vol_plot.png'
        load_tot_vol_dict_and_plot_distr(path_pickle_file, path_plot)

    """
    with open(os.path.join(path_pickle_file), 'rb') as f:
        pickle_data_dict = pickle.load(f)

    list_tot_vol = [v for v in pickle_data_dict.values()
                    if v!=None]

    sns.displot(list_tot_vol, binwidth=20000)
    plt.savefig(os.path.join(path_plot))
    plt.close()


def load_and_plot_all_volume_pickle_files(results_dir, name_pickle_file, path_plot, binwidth=1000, limit_volume=None):
    """
    This function recursively searches through a directory and its subdirectories for 'name_pickle_file'
    files. For each 'name_pickle_file' file, it loads the contents using pickle and extends the contents
    to a list, excluding any None values. The resulting list of total volumes is returned.

    The pickle files with that name are the files saved by the function 'analyse_and_plot_price_files' when
    analysing price files. This pickle files contain a dictionary where the keys are the price files' names and
    the values are the value of the feature 'Total volume traded' or of the feature 'Pre-event volume traded'.

    The purpose of this function is to collect all the different values of one of those two feature and plot their
    distribution.

    Args:
        results_dir (str): The root directory containing the pickle files.
        name_pickle_file (str): The name of the pickle files to load.
        path_plot (str): Path where to save the distribution plot.
        limit_volume (float or None): Represent the volume above which values are excluded from the plot. it has
        the purpose of making the plot useful (when very high values are included the plot is useless). Set it
        to None if no you want no limit.

    Returns:
        list: A list of total volumes obtained from all 'tot_volume_traded_dict.pkl' files in the given directory
        and its subdirectories.

    Example:

        results_dir = 'path/to/your/results/directory'
        name_pickle_file = 'tot_volume_traded_dict.pkl'
        total_volumes = load_and_plot_all_tot_volume_dicts(results_dir, name_pickle_file)

    """
    list_tot_volumes = []
    for root, _, files in alive_it(list(os.walk(results_dir))):
        for file_name in files:
            if file_name==name_pickle_file:
                with open(os.path.join(root, file_name), 'rb') as f:
                    tot_volume_traded_dict = pickle.load(f)
                if limit_volume!=None:
                    list_tot_volumes.extend(
                        [v for v in tot_volume_traded_dict.values()
                        if v!=None and
                        #v>0 and
                        v<limit_volume]
                    )
                else:
                    list_tot_volumes.extend(
                        [v for v in tot_volume_traded_dict.values()
                        if v!=None]
                    )

    sorted_list = sorted(list_tot_volumes)
    idx_95_perc = int(len(list_tot_volumes)*0.95)
    value_95_perc = sorted_list[idx_95_perc]
    mean_value = np.mean(list_tot_volumes)
    median_value = np.median(list_tot_volumes)

    print(f"Mean: {mean_value}")
    print(f"Median: {median_value}")
    print(f"95th percentile: {value_95_perc}")

    name_plot = name_pickle_file.split(".pkl")[0] + "_total"

    sns.displot(list_tot_volumes,
                binwidth=binwidth,
                kde=True,
                )
    plt.axvline(value_95_perc, color='red', label="95th percentile")
    plt.axvline(np.mean(list_tot_volumes), color='blue', label="Mean")
    plt.axvline(np.median(list_tot_volumes), color='green', label="Median")
    plt.legend()
    plt.savefig(os.path.join(path_plot, name_plot))
    plt.close()

    return list_tot_volumes










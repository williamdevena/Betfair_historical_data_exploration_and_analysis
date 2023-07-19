"""
This module contains all the functions necessary to analyse the Betfair price files. These functions are used in the
data_exploration module where the data exploration is performed.
"""

import os
import pickle
from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from alive_progress import alive_it

from src import constants, data_plotting, data_processing
from utils import pricefileutils


def calculate_and_plot_mean_correlation_matrix(data_path, path_plot):
    """
    This function extracts several features from all price files in the specified directory,
    computes the mean correlation matrix between these features and then it plots the mean
    correlation matrix as a heatmap and saves it to the specified location.

    Args:
        data_path (str): The path to the directory where the data files are located.
        path_plot (str): The path where the plot should be saved.

    Returns:
        mean_matrix (numpy array): The mean correlation matrix computed from all data files.

    Example:
        data_path = 'path/to/your/data/match_odds'
        path_plot = 'path/to/save/your/corr_matrix.png'
        calculate_and_plot_mean_correlation_matrix(data_path, path_plot)
    """
    list_corr_matrices = []

    for root, _, files in alive_it(list(os.walk(data_path))):
        for file_name in files:
            if ".bz2" in file_name:
                file_path = os.path.join(root, file_name)
                dict_features, inplay_idx = extract_features_from_price_file(price_file=file_path)
                dict_features_only_lists = {feature_name: feature for feature_name, feature in dict_features.items()
                                        if isinstance(feature, list)}

                df_features = pd.DataFrame.from_dict(dict_features_only_lists)
                corr_matrix = df_features.corr()

                if corr_matrix.shape==(11,11):
                    list_corr_matrices.append(corr_matrix)

    mean_matrix = np.nanmean(list_corr_matrices, axis=0)

    f, ax = plt.subplots(figsize=(12, 9))
    mask = np.triu(mean_matrix)
    sns.heatmap(mean_matrix, square=False, annot=True, xticklabels=[col for col in list_corr_matrices[0]],
            yticklabels=[col for col in list_corr_matrices[0]],
            fmt='.2f',
            mask=mask)
    f.tight_layout()
    plt.savefig(path_plot)
    plt.close()

    return mean_matrix





def analyse_and_plot_multiple_price_files(data_path, results_dir, save_result_in_pickle):
    """
    This function traverses through a given directory, analyses and generates plots for every price file found,
    and saves the result in pickle files. It calculates aggregate statistics, identifies missing data,
    and computes total volume and pre-event volume traded.
    The results saved are the following:
        - plots of the extracted festures for each event are saved in a 'plots'
          directory inside 'results_dir' directory.
        - 4 pickle files ('aggregate_stats_dict.pkl', 'missing_data_dict.pkl',
          'tot_volume_traded_dict.pkl', 'pre_event_volume_traded.pkl') are saved
          in the 'results-dir' directory.
        - 2 plots are saved in the 'results_dir' directory. One showes the distribution of the
        feature 'total volume traded' in all the events analysed and the other one shows the
        distribution of the 'Pre event volume traded' feature.

    Args:
        data_path (str): The path for the directory containing price files to be analysed.
        results_dir (str): The path where the plots and some textual results (name, id,
        total volume traded and pre event volume traded) will be saved (the directory doesn't
        have to exist already, it is created in case it doesn't).
        save_result_in_pickle (bool): If True, the function saves the results in pickle files.

    Returns:
        dict: A dictionary containing aggregate statistics, missing data, total volume traded, and pre-event volume
              traded for each price file.

    Example:

        data_path = 'path/to/your/data/Jan/1'
        results_dir = 'path/to/save/your/results_1'
        save_pickle = True
        results = analyse_and_plot_price_files(data_path, results_dir, save_pickle)
    """
    plot_dir = os.path.join(results_dir, "plots")

    if not os.path.exists(plot_dir):
            os.makedirs(plot_dir)

    dict_aggregate_stats = {}
    dict_missing_data = {}
    dict_tot_volume_traded = {}
    dict_pre_event_vol_traded = {}
    dict_all_results = {}

    for root, _, files in alive_it(list(os.walk(data_path))):
        for file_name in files:
            if ".bz2" in file_name:
                plot_dir_name = file_name.split(".bz2")[0]
                file_path = os.path.join(root, file_name)
                plot_path = os.path.join(plot_dir, plot_dir_name)
                print(file_path)

                if not os.path.exists(plot_path):
                    os.makedirs(plot_path)

                dict_result = analyse_and_plot_single_price_file(price_file_path=file_path,
                                        results_dir=results_dir)

                dict_all_results[file_name] = dict_result

                dict_aggregate_stats[file_name] = dict_result['aggr_stats']
                dict_missing_data[file_name] = dict_result['missing_data']
                dict_tot_volume_traded[file_name] = dict_result['tot_vol_traded']
                dict_pre_event_vol_traded[file_name] = dict_result['pre_event_vol_traded']

    data_plotting.plot_distr_volume_traded(dict_volume_traded=dict_tot_volume_traded,
                                                path_plot=os.path.join(results_dir, constants.NAME_PLOT_TOT_VOLUME),
                                                binwidth=20000)
    data_plotting.plot_distr_volume_traded(dict_volume_traded=dict_pre_event_vol_traded,
                                                path_plot=os.path.join(results_dir, constants.NAME_PLOT_PRE_EVENT_VOLUME),
                                                binwidth=5000)

    if save_result_in_pickle:
        with open(os.path.join(results_dir,'aggregate_stats_dict.pkl'), 'wb') as f:
            pickle.dump(dict_aggregate_stats, f)

        with open(os.path.join(results_dir,'missing_data_dict.pkl'), 'wb') as f:
            pickle.dump(dict_missing_data, f)

        with open(os.path.join(results_dir,'tot_volume_traded_dict.pkl'), 'wb') as f:
            pickle.dump(dict_tot_volume_traded, f)

        with open(os.path.join(results_dir,'pre_event_volume_traded.pkl'), 'wb') as f:
            pickle.dump(dict_pre_event_vol_traded, f)

    return {'aggr_stats': dict_aggregate_stats,
            'missing_data': dict_missing_data,
            'tot_vol_traded': dict_tot_volume_traded,
            'pre_event_vol_traded': dict_pre_event_vol_traded,
            'dict_all_results': dict_all_results}




def analyse_and_plot_single_price_file(price_file_path, results_dir):
    """
    This function analyses a given price file, generates several plots based on its features, calculates aggregate
    statistics, identifies missing data, and returns these results in a dictionary format.

    Args:
        price_file_path (str): The path for the price file to be analysed.
        results_dir (str): The path where the plots  and some textaul results will be saved.

    Returns:
        dict: A dictionary containing aggregate statistics, missing data, total volume traded, and pre-event volume
              traded for the price file.

    Example:

        price_file_path = 'path/to/your/price_file.bz2'
        plot_path = 'path/to/save/your/plot'
        results = analyse_and_plotting_price_file(price_file_path, plot_path)

    """
    plot_dir = os.path.join(results_dir, "plots")
    file_name = price_file_path.split("/")[-1].split(".bz2")[0]
    plot_dir_name = file_name.split(".bz2")[0]
    plot_path = os.path.join(plot_dir, plot_dir_name)

    dict_features, inplay_idx = extract_features_from_price_file(price_file=price_file_path)

    dict_features_only_lists = {feature_name: feature for feature_name, feature in dict_features.items()
                               if isinstance(feature, list)}

    df_features = pd.DataFrame.from_dict({k: v for k, v in dict_features_only_lists.items()
                                          if k!='Pre-event diff time' and
                                          k!='In-play diff time'})

    ## PLOTS
    data_plotting.plot_dict_features_from_price_file(dict_features=dict_features_only_lists,
                                                   inplay_idx=inplay_idx,
                                                   plot_path=plot_path)

    data_plotting.plot_correlation_matrix(df_features=df_features,
                                          plot_path=plot_path)

    ## AGGREGATE STATS
    df_aggregate_stats = df_features.describe()

    ## MISSING DATA
    df_missing_data = calculate_missing_data(df_features=df_features)

    # WRITE TOT. VOLUME AND PRE-EVENT VOLUME
    with open(os.path.join(results_dir,'results.txt'), 'a') as f:
        for name, _ in constants.FUNS_FOR_PRICE_FILE.items():
            f.write(f"{name}: {dict_features[name]}\n")
            # f.write(f"Event ID: {dict_features['EventId']}\n")
            # f.write(f"Tot volume traded: {dict_features['Total volume traded']}\n")
            # f.write(f"Pre event volume traded: {dict_features['Pre-event volume']}\n\n")
        f.write("\n")

    return {'aggr_stats': df_aggregate_stats,
            'missing_data': df_missing_data,
            'tot_vol_traded': dict_features['Total volume traded'],
            'pre_event_vol_traded': dict_features['Pre-event volume'],
            'dict_features': dict_features}



def extract_single_feature_from_multiple_price_files(data_path, feature_name):
    """
    This function extracts a specific feature from multiple data files stored in a directory.

    Args:
        data_path (str): The path to the directory where the data files are located.
        feature_name (str): The name of the feature to be extracted from the data files.

    Returns:
        dict_results (dict): A dictionary with file names as keys and another dictionary as values. The nested
            dictionary contains the 'inplay_idx' of each file and the specific feature values.

    Example:
        data_path = 'path/to/your/data/macth_odds'
        feature_name = 'OB imbalance'
        extract_single_feature_from_multiple_price_files(data_path, feature_name)

    Note:
        This function assumes the price files are in .bz2 format.
    """
    dict_results = {}

    for root, _, files in alive_it(list(os.walk(data_path))):
        for file_name in files:
            if ".bz2" in file_name:
                file_path = os.path.join(root, file_name)
                dict_results[file_name] = {}

                dict_results[file_name]['inplay_idx'] = pricefileutils.get_last_pre_event_market_book_id_from_prices_file(file_path)
                dict_results[file_name][feature_name] = extract_single_feature_from_price_file(price_file=file_path,
                                                                feature_name=feature_name)


    return dict_results




def extract_single_feature_from_price_file(price_file, feature_name):
    """
    This function extracts a specific feature from a data file.

    It checks if the feature can be calculated by one of the functions defined in the constants module.
    If so, it calculates the feature; otherwise, it returns None.

    Args:
        price_file (str): The path to the data file.
        feature_name (str): The name of the feature to be extracted from the data file.

    Returns:
        The result of the feature extraction function if the feature can be calculated, otherwise None.

    Example:
        price_file = 'path/to/your/data/1.2338853.bz2'
        feature_name = 'OB imbalance'
        extract_single_feature_from_price_file(price_file, feature_name)
    """
    if feature_name in constants.FUNS_FOR_PRICE_FILE:
        return constants.FUNS_FOR_PRICE_FILE[feature_name](price_file)

    elif feature_name in constants.FUNS_FOR_MB:
        return data_processing.apply_function_for_mb_on_entire_price_file(
            price_file_path=price_file,
            function_for_mb=constants.FUNS_FOR_MB[feature_name],
            parameters=constants.PARAMETERS_FOR_FUNCTIONS.get(feature_name, [])
        )

    elif feature_name in constants.FUNS_FOR_RUNNERS:
        return data_processing.apply_function_for_runner_on_entire_price_file(
            price_file_path=price_file,
            function_for_runner=constants.FUNS_FOR_RUNNERS[feature_name],
            parameters=constants.PARAMETERS_FOR_FUNCTIONS.get(feature_name, [])
        )

    else:
        return None



def extract_features_from_price_file(price_file):
    """
    This function extracts statistics from a given price file. The statistics are calculated based on functions
    defined in FUNS_FOR_PRICE_FILE, FUNS_FOR_MB, and FUNS_FOR_RUNNERS dictionaries in the constants module.

    Args:
        price_file (str): Path to the price file.

    Returns:
        dict: A dictionary containing calculated statistics. The keys of the dictionary are the names of the statistics
        and the values (they could be both single floats or list of floats).
        inplay_idx (int): represents the index of the first in-play market book. It has plotting purposes.

    Example:

        stats = extract_stats_from_price_file('path/to/your/file.bz2')
        print(stats)
        # returns a dictionary with the statistics calculated by the functions defined in the constant dictionaries.

    """
    dict_features = {}
    inplay_idx = pricefileutils.get_last_pre_event_market_book_id_from_prices_file(price_file)


    for name, function in constants.FUNS_FOR_PRICE_FILE.items():
        dict_features[name] = function(price_file)

    for name, function in constants.FUNS_FOR_MB.items():
        dict_features[name] = data_processing.apply_function_for_mb_on_entire_price_file(
            price_file_path=price_file,
            function_for_mb=function,
            parameters=constants.PARAMETERS_FOR_FUNCTIONS.get(name, [])
        )

    for name, function in constants.FUNS_FOR_RUNNERS.items():
        #print(name)
        results = data_processing.apply_function_for_runner_on_entire_price_file(
            price_file_path=price_file,
            function_for_runner=function,
            parameters=constants.PARAMETERS_FOR_FUNCTIONS.get(name, [])
        )
        if results!=None:
            for idx, result in enumerate(results):
                dict_features[name+f"_{idx+1}"] = result

    dict_features['Matched'] = list(np.diff(dict_features['Total matched'], prepend=0))
    final_matched_volume = max(dict_features['Total matched'])
    if final_matched_volume>0:
        dict_features['Normalized matched'] = [volume/final_matched_volume for volume in dict_features['Total matched']]
    dict_features['Diff time'] = calculate_avg_time_between_market_books(dict_features['Publish time'])

    # print(f"Event name: {dict_features['Name']}")
    # print(f"Total volume traded: {dict_features['Total volume traded']}")
    # print(f"Pre-event volume: {dict_features['Pre-event volume']}")
    if inplay_idx!=None:
        dict_features['Pre-event diff time'] = dict_features['Diff time'][:inplay_idx]
        dict_features['In-play diff time'] = dict_features['Diff time'][inplay_idx:]
        dict_features['Pre-event avg diff time'] = np.average(dict_features['Pre-event diff time'])
        dict_features['In-play avg diff time'] = np.average(dict_features['In-play diff time'])
        # print(f"Pre-event avg diff time: {dict_features['Pre-event avg diff time']}")
        # print(f"In-play avg diff time: {dict_features['In-play avg diff time']}")
    # print()


    return dict_features, inplay_idx


def calculate_avg_time_between_market_books(list_timestamps):
    """
    This function calculates the average time in seconds between subsequent market books,
    represented by timestamps.

    Args:
        list_timestamps (list): A list of datetime objects representing the timestamps of the market books.

    Returns:
        list: A list of the time differences (in seconds) between subsequent market books. The last element is always 0
              as it's the difference with itself.

    Example:

        timestamps = [datetime(2020, 1, 1, 10, 0), datetime(2020, 1, 1, 11, 0), datetime(2020, 1, 1, 12, 0)]
        diffs_seconds = calculate_avg_time_between_market_books(timestamps)
        # diffs_seconds would be [3600.0, 3600.0, 0]
    """
    diffs = [(list_timestamps[i+1]-list_timestamps[i])
            for i in range(len(list_timestamps)-1)]

    diffs_seconds = [diff.total_seconds() for diff in diffs]
    diffs_seconds.append(0)

    return diffs_seconds



def calculate_time_from_inplay(list_timestamps, inplay_idx):
    """
    This function calculates the time difference between each timestamp in a list and a specific timestamp
    (identified by the inplay_idx) that represents the first in-play timestamp in the same list.

    It returns a list of differences in seconds between each timestamp and the "in-play" timestamp.

    Args:
        list_timestamps (list): The list of timestamps.
        inplay_idx (int): The index of the "in-play" timestamp in the list_timestamps.

    Returns:
        diffs_seconds (list): A list of time differences in seconds.

    Example:
        list_timestamps = [datetime(2023, 7, 11, 13, 0, 0), datetime(2023, 7, 11, 13, 5, 0), datetime(2023, 7, 11, 13, 10, 0)]
        inplay_idx = 1
        calculate_time_from_inplay(list_timestamps, inplay_idx)
        # Output: [0, 300, 600]
    """
    diffs = [(timestamp-list_timestamps[inplay_idx])
            for idx, timestamp in enumerate(list_timestamps)]

    diffs_seconds = [diff.total_seconds() for diff in diffs]

    return diffs_seconds





def calculate_missing_data(df_features):
    """
    This function calculates the count and percentage of missing data in each column of the given DataFrame.

    Args:
        df_features (pandas.DataFrame): The DataFrame for which missing data is to be calculated.

    Returns:
        pandas.DataFrame: A DataFrame with each column's total missing values and percentage of missing values.
        The DataFrame is sorted in descending order of the total count of missing values. The columns in the returned
        DataFrame are 'Total' and 'Percent', where 'Total' is the count of missing values and 'Percent' is the
        percentage of missing values in the column.

    Example:

        data = {'A': [1, 2, None], 'B': [4, None, 6], 'C': [7, 8, 9]}
        df = pd.DataFrame(data)
        missing_data = calculate_missing_data(df)
        print(missing_data)
        # Output:
        #    Total   Percent
        # B      1  0.333333
        # A      1  0.333333
        # C      0  0.000000

    """
    total = df_features.isnull().sum().sort_values(ascending = False)
    percent = (df_features.isnull().sum() / df_features.isnull().count()).sort_values(ascending = False)
    df_missing_data = pd.concat([total, percent], axis = 1, keys = ['Total', 'Percent'])

    return df_missing_data





#from ydata_profiling import ProfileReport
import os
import pickle
from pprint import pprint

import numpy as np
import pandas as pd

from src import constants, data_plotting, data_processing, utils


def analyse_and_plot_price_files(data_path, plot_dir, save_result_in_pickle):
    """
    This function analyses and plots data from multiple price files, provided by a path to a directory
    containing price files. The plots are saved to specified directories (param 'plot_dir'). The function
    returns two dictionaries ('dict_aggregate_stats' and 'dict_missing_data') containing aggregate statistics
    and missing data for each file. The keys are the files' names and the values are DataFrames containg the
    aggregate stats and the info on missing data.
    Additionally, if param 'save_result_in_pickle' is True it saves the two dictionaries in separate pickle files.

    Args:
        list_price_files (list): A list of paths (str) for the price files to be analysed.
        plot_dir (str): The directory where the plots will be saved.

    Returns:
        dict: A dictionary where keys are file names and values are DataFrames containing
        aggregate statistics for each price file.
        dict: A dictionary where keys are file names and values are DataFrames containing
        info on missing data for each price file.

    Example:

        files = ['path/to/your/price_file1.bz2', 'path/to/your/price_file2.bz2']
        directory = 'path/to/save/your/plots'
        stats, missing_data = analyse_and_plot_price_files(files, directory, save_result_in_pickle=True)

    """
    if not os.path.exists(plot_dir):
            os.makedirs(plot_dir)

    dict_aggregate_stats = {}
    dict_missing_data = {}

    for root, dirs, files in os.walk(data_path):
        for file_name in files:
            if ".bz2" in file_name:
                plot_dir_name = file_name.split(".bz2")[0]
                file_path = os.path.join(root, file_name)
                plot_path = os.path.join(plot_dir, plot_dir_name)
                print(file_path)

                if not os.path.exists(plot_path):
                    os.makedirs(plot_path)

                dict_aggregate_stats[file_name], dict_missing_data[file_name] = analyse_and_plotting_price_file(price_file_path=file_path,
                                            plot_path=plot_path)

    if save_result_in_pickle:
        with open('aggregate_stats_dict.pkl', 'wb') as f:
            pickle.dump(dict_aggregate_stats, f)

        with open('missing_data_dict.pkl', 'wb') as f:
            pickle.dump(dict_missing_data, f)

    return dict_aggregate_stats, dict_missing_data




def analyse_and_plotting_price_file(price_file_path, plot_path):
    """
    This function analyses and generates plots for data from a given price file. It also calculates aggregate
    statistics and identifies missing data. The plots are saved to the specified directory.
    This function is called by the 'analyse_and_plot_price_files' function for each price file.

    Args:
        price_file_path (str): The path for the price file to be analysed.
        plot_path (str): The path where the plots will be saved.

    Returns:
        pandas.DataFrame: A DataFrame containing the aggregate statistics for the file.
        pandas.DataFrame: A DataFrame containing the missing data information for the file.

    Example:

        file = 'path/to/your/price_file'
        directory = 'path/to/save/your/plots'
        stats, missing_data = analyse_and_plotting_price_file(file, directory)
    """
    file_name = price_file_path.split("/")[-1].split(".bz2")[0]
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

    print(f"Total volume traded: {dict_features['Total volume traded']}")
    print(f"Pre-event volume: {dict_features['Pre-event volume']}")
    print()

    return df_aggregate_stats, df_missing_data



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
    inplay_idx = utils.get_last_pre_event_market_book_id_from_prices_file(price_file)

    for name, function in constants.FUNS_FOR_PRICE_FILE.items():
        dict_features[name] = function(price_file)

    for name, function in constants.FUNS_FOR_MB.items():
        dict_features[name] = data_processing.apply_function_for_mb_on_entire_price_file(
            price_file_path=price_file,
            function_for_mb=function,
            parameters=constants.PARAMETERS_FOR_FUNCTIONS.get(name, [])
        )

    for name, function in constants.FUNS_FOR_RUNNERS.items():
        results = data_processing.apply_function_for_runner_on_entire_price_file(
            price_file_path=price_file,
            function_for_runner=function,
            parameters=constants.PARAMETERS_FOR_FUNCTIONS.get(name, [])
        )
        for idx, result in enumerate(results):
            dict_features[name+f"_{idx+1}"] = result

    dict_features['Matched'] = list(np.diff(dict_features['Total matched'], prepend=0))
    dict_features['Diff time'] = calculate_avg_time_between_market_books(dict_features['Publish time'])

    if inplay_idx!=None:
        dict_features['Pre-event diff time'] = dict_features['Diff time'][:inplay_idx]
        dict_features['In-play diff time'] = dict_features['Diff time'][inplay_idx:]
        dict_features['Pre-event avg diff time'] = np.average(dict_features['Pre-event diff time'])
        dict_features['In-play avg diff time'] = np.average(dict_features['In-play diff time'])
        print(f"Pre-event avg diff time: {dict_features['Pre-event avg diff time']}")
        print(f"In-play avg diff time: {dict_features['In-play avg diff time']}")


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





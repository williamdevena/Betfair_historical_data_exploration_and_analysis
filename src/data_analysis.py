from pprint import pprint

import numpy as np
import pandas as pd
from ydata_profiling import ProfileReport

from src import constants, data_plotting, data_processing, utils


def analyse_price_file(price_file_path, plot_path, profiling_path):
    file_name = price_file_path.split("/")[-1].split(".bz2")[0]
    dict_features, inplay_idx = extract_features_from_price_file(price_file=price_file_path)

    dict_features_only_lists = {feature_name: feature for feature_name, feature in dict_features.items()
                               if isinstance(feature, list)}

    df_features = pd.DataFrame.from_dict(dict_features_only_lists)

    ## PLOTS
    print("plotting")
    data_plotting.plot_df_features_from_price_file(df_features=df_features,
                                                   inplay_idx=inplay_idx,
                                                   plot_path=plot_path)

    print("corr matrix")
    data_plotting.plot_correlation_matrix(df_features=df_features,
                                          plot_path=plot_path)

    ## AGGREGATE STATS
    print("aggr")
    df_aggregate_stats = df_features.describe()

    ## MISSING DATA
    print("missing")
    df_missing_data = calculate_missing_data(df_features=df_features)

    ## OUTLIERS


    ## PROFILING (OPTIONAL)
    # profiling_df_features(df_features=df_features,
    #                       path_file=profiling_path)

    return df_aggregate_stats, df_missing_data





def profiling_df_features(df_features, path_file):
    profile = ProfileReport(df_features, title="Profiling features")
    profile.to_file(path_file)


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
    _, inplay_idx = utils.get_last_pre_event_market_book_id_from_prices_file(price_file)

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

    print(dict_features['Mid price_1'])

    return dict_features, inplay_idx


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





# def calculate_aggregate_stats_of_features(df_features):
#     """
#     This function calculates aggregate statistics of features calculated from a price file,
#     like 'available volume', 'mid price', ...

#     The function only accepts a DataFrame with columns of the same length (this means
#     that single value features like 'Total volume traded' can't be in the DataFrame).

#     Args:
#         dict_features (dict): A dictionary where the keys are feature names (str) and the values are lists of feature
#         values.

#     Returns:
#         pandas.DataFrame: A DataFrame of the calculated aggregate statistics for each feature. The aggregate statistics
#         include: count, mean, std, min, 25%, 50%, 75%, max.

#     Example:

#         features = {'Feature1': [1, 2, 3, 4, 5], 'Feature2': [6, 7, 8, 9, 10]}
#         stats = calculate_stats_of_features(features)
#         print(stats)
#         # Output:
#         #        Feature1  Feature2
#         # count  5.000000  5.000000
#         # mean   3.000000  8.000000
#         # std    1.581139  1.581139
#         # min    1.000000  6.000000
#         # 25%    2.000000  7.000000
#         # 50%    3.000000  8.000000
#         # 75%    4.000000  9.000000
#         # max    5.000000 10.000000

#     """
#     # dict_features_only_lists = {feature_name: feature for feature_name, feature in dict_features.items()
#     #               if isinstance(feature, list)}

#     ## AGGREGATE STATS
#     #df_features_only_lists = pd.DataFrame.from_dict(dict_features_only_lists)
#     df_aggregate_stats = df_features.describe()

#     return df_aggregate_stats




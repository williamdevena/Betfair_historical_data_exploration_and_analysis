from pprint import pprint

import numpy as np
import pandas as pd
from ydata_profiling import ProfileReport

from src import constants, data_processing, utils


def profiling_df_features(df_features):
    profile = ProfileReport(df_features, title="Profiling features")
    profile.to_file("your_report.html")


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

    Note:
        This function depends on the following:
            - The 'constants' module and its FUNS_FOR_PRICE_FILE, FUNS_FOR_MB, and FUNS_FOR_RUNNERS dictionaries.
            - The 'data_processing' module and specifically its 'apply_function_for_mb_on_entire_price_file' and
              'apply_function_for_runner_on_entire_price_file' functions.
            - The 'utils' module and specifically its 'get_last_pre_event_market_book_id_from_prices_file' function.
        It's important to ensure these modules and functions are correctly defined and imported.

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

    return dict_features, inplay_idx





def calculate_stats_of_features(dict_features):
    #pprint(dict_features)
    #print(len(dict_features))
    dict_stats = {feature_name: feature for feature_name, feature in dict_features.items()
                  if isinstance(feature, list)}
    #print(len(dict_stats))

    df_stats = pd.DataFrame.from_dict(dict_stats)
    print(df_stats.describe())

    total = df_stats.isnull().sum().sort_values(ascending = False)
    percent = (df_stats.isnull().sum() / df_stats.isnull().count()).sort_values(ascending = False)
    missing_data = pd.concat([total, percent], axis = 1, keys = ['Total', 'Percent'])
    print(missing_data)


    # import matplotlib.pyplot as plt
    # import seaborn as sns

    # # sns.distplot(df_stats['Matched'])
    # # plt.show()

    # correlation_matrix = df_stats.corr()
    # mask = np.triu(correlation_matrix)
    # f, ax = plt.subplots(figsize=(12, 9))
    # sns.heatmap(correlation_matrix, square=False, annot=True, mask=mask)
    # plt.show()




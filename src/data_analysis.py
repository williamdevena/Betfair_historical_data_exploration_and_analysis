import numpy as np

from src import constants, data_processing, utils


def extract_stats_from_price_file(price_file):
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
    dict_stats = {}
    _, inplay_idx = utils.get_last_pre_event_market_book_id_from_prices_file(price_file)

    for name, function in constants.FUNS_FOR_PRICE_FILE.items():
        dict_stats[name] = function(price_file)

    for name, function in constants.FUNS_FOR_MB.items():
        dict_stats[name] = data_processing.apply_function_for_mb_on_entire_price_file(
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
            dict_stats[name+f"_{idx+1}"] = result

    dict_stats['Matched'] = list(np.diff(dict_stats['Total matched']))

    return dict_stats, inplay_idx
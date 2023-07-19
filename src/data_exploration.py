"""
This module executes the data exploration of the Betfair price files.

The different analysis in the data_exploration function are commented so that the reader can execute them one at the time and
indipendently, by removing the comments.
"""

import os

import dotenv
import matplotlib.pyplot as plt
import numpy as np
from alive_progress import alive_it

from src import constants, data_analysis, data_plotting


def data_exploration():
    dotenv.load_dotenv()
    data_directory = os.environ.get("DATA_DIRECTORY")


    ## CALCULATE MEAN CORRELATION MATRIX
    # data_path = os.path.join(data_directory, "djokovic_match_odds")
    # data_path = os.path.join(data_directory, "match_odds")
    # mean_matrix = data_analysis.calculate_and_plot_mean_correlation_matrix(data_path=data_path,
    #                                                                        path_plot="./mean_corr_matrix_all_days")



    ### ANALYSE SINGLE PRICE FILE
    # file_path = os.path.join(data_directory, "match_odds/19/32035350/1.208791811.bz2")
    # results_dir = "./results_test"
    # dict_result = data_analysis.analyse_and_plot_price_file(price_file_path=file_path,
    #                                     results_dir=results_dir)






    # ## ANALYSE MULTIPLE PRICE FILES IN FOLDER
    # data_path = os.path.join(data_directory, "djokovic_match_odds")
    # # data_path = os.path.join(data_directory, "match_odds")
    # results_dir = "./results_djokovic_3"

    # # READ, ANALYSE AND PLOT DATA
    # # Check 'analyse_and_plot_price_files' documentation for more details
    # dict_result = data_analysis.analyse_and_plot_multiple_price_files(data_path=data_path,
    #                                         results_dir=results_dir,
    #                                         save_result_in_pickle=True)





    # ## ANALYSE ENTIRE DATA FOLDER (CONTAINING MULTIPLE DAYS)
    # ## This piece of code is useful is you have a directory of price files
    # ## divided in days, like the structure of the data downloaded from the
    # ## Betfair hstorical data service.
    # ## Example of data of January 2023: "2023/Jan/1", "2023/Jan/2", ..., "2023/Jan/31"
    # for day_of_the_month in range(1, 32):
    #     day_folder_path = os.path.join(data_path, str(day_of_the_month))
    #     results_dir = f"./results/results_{day_of_the_month}"

    #     ## the if statement is in case in the data directory you don't have all the days continuosly
    #     ## (if you skip some days) and in case you have already analyzed some of
    #     ## the days' folder and produced the plots (hence the 'results_dir' directory
    #     ## already exists).
    #     if os.path.exists(day_folder_path) and not os.path.exists(results_dir):
    #         data_analysis.analyse_and_plot_price_files(data_path=day_folder_path,
    #                                                 results_dir=results_dir,
    #                                                 save_result_in_pickle=True)






    # ## LOAD DATA ON TOTAL VOLUME TRADED
    # ## This is to load and plot the data in the pickle files produced by the analysis ('tot_volume_traded_dict.pkl' or
    # ## 'pre_event_volume_traded.pkl').
    # data_plotting.load_dict_from_pickle_and_plot_distr(path_pickle_file=os.path.join(results_dir,
    #                                                                              constants.PICKLE_FILE_NAME_TOT_VOLUME),
    #                                                    path_plot=os.path.join(results_dir,
    #                                                                       constants.NAME_PLOT_TOT_VOLUME))






    # ## LOAD AND PLOT DISTRIBUTION OF ALL VOLUME PICKLE FILES
    # ## This is to load all the pickle files in a results directory
    # ## ('tot_volume_traded_dict.pkl' or 'pre_event_volume_traded.pkl') and
    # ## plot the total distribution of the data saved in these files (total volume
    # ## traded or pre event volume traded) in one histogram plot.
    # ## The purpose is calculate and plot the distribution of the entire data and
    # ## not just one of the data of one day.

    # ## TOTAL VOLUME
    # data_plotting.load_and_plot_all_volume_pickle_files(
    #     results_dir="./results",
    #     path_plot="./results",
    #     name_pickle_file=constants.PICKLE_FILE_NAME_TOT_VOLUME,
    #     limit_volume=100000,
    #     binwidth=1500,

    # )
    # ## PRE EVENT VOLUME
    # data_plotting.load_and_plot_all_volume_pickle_files(
    #     results_dir="./results",
    #     path_plot="./results",
    #     name_pickle_file=constants.PICKLE_FILE_NAME_PRE_EVENT_VOLUME,
    #     limit_volume=10000,
    #     binwidth=200,

    # )



if __name__=="__main__":
    data_exploration()

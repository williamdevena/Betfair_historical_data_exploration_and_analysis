import os

import dotenv
import matplotlib.pyplot as plt
import numpy as np
from alive_progress import alive_it

from src import constants, data_analysis, data_plotting


def data_exploration():
    dotenv.load_dotenv()
    data_path = os.environ.get("DATA_PATH")



    ## MEAN CORR MATRIX
    data_path = "/Users/william.devena/Desktop/UCL/RESEARCH_PROJECT/QST/Data/djokovic_match_odds_little/29"
    mean_matrix = data_analysis.calculate_and_plot_mean_correlation_matrix(data_path=data_path,
                                                                           path_plot="./mean_corr_matrix_29")




    # #### MEN OF TIME SERIES OF A FEATURE
    # data_path = "/Users/william.devena/Desktop/UCL/RESEARCH_PROJECT/QST/Data/djokovic_match_odds_little"
    # # mean_time_series, list_features = data_analysis.calculate_mean_time_series_of_feature(data_path=data_path,
    # #                                                     feature_name="Total matched")

    # mean_time_series, list_features = data_analysis.calculate_mean_normalized_matched_volume_time_series(data_path=data_path)

    # # print(mean_time_series)

    # # print(len(list_features))

    # for feature in list_features:
    #     plt.plot(feature)

    # plt.plot(mean_time_series, label="Mean")
    # plt.legend()
    # plt.show()






    ### ANALYSE SINGLE PRICE FILE
    # file_path = "/Users/william.devena/Desktop/UCL/RESEARCH_PROJECT/QST/Data/match_odds/19/32035350/1.208791811.bz2"
    # results_dir = "./results_test"
    # dict_result = data_analysis.analyse_and_plot_price_file(price_file_path=file_path,
    #                                     results_dir=results_dir)





    # ## ANALYSE SINGLE DAY FOLDER
    # day_of_the_month = "3"
    # data_path = os.path.join(data_path, day_of_the_month)
    # results_dir = f"./results/results_{day_of_the_month}"

    # data_path = "/Users/william.devena/Desktop/UCL/RESEARCH_PROJECT/QST/Data/djokovic_match_odds_little"
    # results_dir = "./results_djokovic_2"
    # # READ, ANALYSE AND PLOT DATA
    # # Check 'analyse_and_plot_price_files' documentation for
    # # more details
    # dict_result = data_analysis.analyse_and_plot_price_files(data_path=data_path,
    #                                         results_dir=results_dir,
    #                                         save_result_in_pickle=True)

    # tot_volumes_macthed = [
    #     np.array(dict_file_results['dict_features']['Total matched']) for file_name, dict_file_results in dict_result['dict_all_results'].items()
    # ]

    # #print(tot_volumes_macthed[0])
    # mean_tot_vol = [np.mean(k) for k in zip(*tot_volumes_macthed)]

    # print(len(mean_tot_vol), len(tot_volumes_macthed[0]), len(tot_volumes_macthed[1]))

    #multiple_lists = [[2,5,1,9], [4,9,5,10]]
    # arrays = [np.array(x) for x in multiple_lists]
    # [np.mean(k) for k in zip(*arrays)]

    # for tot_vol in tot_volumes_macthed:
    #     plt.plot(tot_vol)

    # plt.plot(mean_tot_vol)
    # plt.show()


    #print([np.mean(k) for k in zip(*tot_volumes_macthed)])





    # ### ANALYSE ENTIRE DATA FOLDER (CONTAINING MULTIPLE DAYS)
    # for day_of_the_month in range(22, 32):
    #     print(day_of_the_month)
    #     day_folder_path = os.path.join(data_path, str(day_of_the_month))
    #     results_dir = f"./results/results_{day_of_the_month}"

    #     if os.path.exists(day_folder_path) and not os.path.exists(results_dir):
    #         data_analysis.analyse_and_plot_price_files(data_path=day_folder_path,
    #                                                 results_dir=results_dir,
    #                                                 save_result_in_pickle=True)
    #         print(day_of_the_month)






    ## LOAD DATA ON TOTAL VOLUME TRADED
    # data_plotting.load_tot_vol_dict_and_plot_distr(path_pickle_file=os.path.join(results_dir,
    #                                                                              constants.PICKLE_FILE_NAME_TOT_VOLUME),
    #                                                path_plot=os.path.join(results_dir,
    #                                                                       constants.NAME_PLOT_TOT_VOLUME))






    # ### LOAD AND PLOT DISTRIBUTION OF ALL VOLUME PICKLE FILES
    # data_plotting.load_and_plot_all_volume_pickle_files(
    #     results_dir="./results",
    #     path_plot="./results",
    #     # TOTAL VOLUME
    #     name_pickle_file="tot_volume_traded_dict.pkl",
    #     limit_volume=100000,
    #     binwidth=1500,
    #     # ## PRE EVENT VOLUME
    #     # name_pickle_file="pre_event_volume_traded.pkl",
    #     # limit_volume=10000,
    #     # binwidth=200,

    # )



if __name__=="__main__":
    data_exploration()

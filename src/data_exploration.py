import os

import dotenv
from alive_progress import alive_it

from src import constants, data_analysis, data_plotting


def data_exploration():
    dotenv.load_dotenv()
    data_path = os.environ.get("DATA_PATH")


    ### ANALYSE SINGLE PRICE FILE
    # file_path = "/Users/william.devena/Desktop/UCL/RESEARCH_PROJECT/QST/Data/match_odds/19/32035350/1.208791811.bz2"
    # results_dir = "./results_test"
    # dict_result = data_analysis.analyse_and_plot_price_file(price_file_path=file_path,
    #                                     results_dir=results_dir)





    # ## ANALYSE SINGLE DAY FOLDER
    # day_of_the_month = "3"
    # data_path = os.path.join(data_path, day_of_the_month)
    # results_dir = f"./results/results_{day_of_the_month}"
    # ## READ, ANALYSE AND PLOT DATA
    # ## Check 'analyse_and_plot_price_files' documentation for
    # ## more details
    # data_analysis.analyse_and_plot_price_files(data_path=data_path,
    #                                         results_dir=results_dir,
    #                                         save_result_in_pickle=True)





    ## ANALYSE ENTIRE DATA FOLDER (CONTAINING MULTIPLE DAYS)
    for day_of_the_month in range(17, 32):
        print(day_of_the_month)
        day_folder_path = os.path.join(data_path, str(day_of_the_month))
        results_dir = f"./results/results_{day_of_the_month}"

        if os.path.exists(day_folder_path) and not os.path.exists(results_dir):
            data_analysis.analyse_and_plot_price_files(data_path=day_folder_path,
                                                    results_dir=results_dir,
                                                    save_result_in_pickle=True)
            #print(day_of_the_month)






    ## LOAD DATA ON TOTAL VOLUME TRADED
    # data_plotting.load_tot_vol_dict_and_plot_distr(path_pickle_file=os.path.join(results_dir,
    #                                                                              constants.PICKLE_FILE_NAME_TOT_VOLUME),
    #                                                path_plot=os.path.join(results_dir,
    #                                                                       constants.NAME_PLOT_TOT_VOLUME))






    # ### LOAD AND PLOT DISTRIBUTION OF ALL VOLUME PICKLE FILES
    # data_plotting.load_and_plot_all_volume_pickle_files(
    #     results_dir="./results",
    #     #name_pickle_file="tot_volume_traded_dict.pkl",
    #     name_pickle_file="pre_event_volume_traded.pkl",
    #     path_plot="./results",
    #     limit_volume=20000
    # )



if __name__=="__main__":
    data_exploration()

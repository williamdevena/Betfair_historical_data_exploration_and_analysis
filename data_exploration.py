import os

from src import constants, data_analysis, data_plotting


def data_exploration():
    day_of_the_month = "1"
    data_path = f"/Users/william.devena/Desktop/UCL/RESEARCH_PROJECT/QST/Data/match_odds/{day_of_the_month}"
    results_dir = f"./results_{day_of_the_month}"


    #print(len(list(os.walk(data_path))))

    # for x in os.walk(data_path):
    #     print(x)

    ## READ, ANALYSE AND PLOT DATA
    data_analysis.analyse_and_plot_price_files(data_path=data_path,
                                               results_dir=results_dir,
                                               save_result_in_pickle=True)

    ## LOAD DATA ON TOTAL VOLUME TRADED
    # data_plotting.load_tot_vol_dict_and_plot_distr(path_pickle_file=os.path.join(results_dir,
    #                                                                              constants.PICKLE_FILE_NAME_TOT_VOLUME),
    #                                                path_plot=os.path.join(results_dir,
    #                                                                       constants.NAME_PLOT_TOT_VOLUME))



if __name__=="__main__":
    data_exploration()

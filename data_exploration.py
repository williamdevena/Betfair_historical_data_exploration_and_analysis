from src import data_analysis


def data_exploration():
    data_path = "/Users/william.devena/Desktop/UCL/RESEARCH_PROJECT/QST/Data/match_odds/1"
    results_dir = "./results"

    data_analysis.analyse_and_plot_price_files(data_path=data_path,
                                               results_dir=results_dir,
                                               save_result_in_pickle=True)


if __name__=="__main__":
    data_exploration()

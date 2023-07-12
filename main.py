import logging
import os
import pickle
import time
from pprint import pprint

import betfairutil
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from alive_progress import alive_it

from src import constants, data_analysis, data_plotting, data_processing, utils


def main():
    #start_time = time.time()

    # logging.basicConfig(
    #     level=logging.INFO,
    #     format="%(message)s",
    #     handlers=[
    #         #logging.FileHandler("project_log/assignment.log"),
    #         logging.StreamHandler()
    #     ]
    # )

    # file_dir = "/Users/william.devena/Desktop/UCL/RESEARCH PROJECT/QST/Data/PRO/2023/Jan/1/31993143"
    # file_name = "1.208134612"
    # file_path = os.path.join(file_dir, file_name)

    # data = data_processing.parse_file(file_path=file_path)
    # #print(data[0])

    # markets = data_processing.parse_historical_data(data)
    # #print(markets)
    # #print(type(markets))
    # #print(markets.keys())
    # #data_processing.save_markets(markets, "./")
    # #print(markets[list(markets)[0]][1672534645534])
    # runners = [24931403, 8942269, 58805]
    # order_book_history = data_processing.get_order_book_history(runner_ids=runners,
    #                                                             max_load_limit=40000,
    #                                                             markets=markets)
    # #print(order_book_history)
    # data, game_start_time, game_end_time = data_processing.get_runner_data(runners[0], order_book_history)
    # #print(data["Volume"])




    # file_dir = "/Users/william.devena/Desktop/UCL/RESEARCH PROJECT/QST/Data/PRO/2023/Jan/1"
    # runners_names = data_reading.read_dir_and_plot(data_dir=file_dir, plot_path="./plots")
    # print(runners_names)


    #path = "/Users/william.devena/Desktop/UCL/RESEARCH PROJECT/QST/Data/PRO/2023/Jan/1/31993143/1.208134610.bz2"

    #path = "/Users/william.devena/Desktop/UCL/RESEARCH_PROJECT/QST/Data/nadal_deminaur.bz2"
    # path = "/Users/william.devena/Desktop/UCL/RESEARCH_PROJECT/QST/Data/djokovic/29/32060431/1.209205488.bz2"

    # market_books = utils.read_prices_file(path)
    # #print(market_books[1002]["runners"])
    # # vol = utils.calculate_available_volume(market_book=market_books[1002], side=utils.Side.BACK, max_book_percentage=None)
    # # print(vol)

    # print(market_books[0]['marketDefinition']["name"])
    # pprint(market_books[100])


    #### VOLUMES
    # volume_back = [utils.calculate_available_volume(market_book=mb, side=utils.Side.BACK, max_book_percentage=None)
    #           for mb in market_books]
    # volume_acc_back = np.cumsum(volume_back)

    # volume_lay = [utils.calculate_available_volume(market_book=mb, side=utils.Side.LAY, max_book_percentage=None)
    #           for mb in market_books]
    # volume_acc_lay = np.cumsum(volume_lay)

    # plt.plot(volume_acc_back)
    # plt.plot(volume_acc_lay)
    # plt.savefig("./volumes_acc")
    # plt.close()
    # plt.plot(volume_back)
    # plt.plot(volume_lay)
    # plt.savefig("./volumes")
    # plt.close()

    # plt.plot(volume_acc_lay)
    # plt.savefig("./volumes_acc_lay")
    # plt.close()
    # plt.plot(volume_lay)
    # plt.savefig("./volumes_lay")
    # plt.close()






    ## PRINT NAMES IN EVENT FOLDER
    # event_path = "/Users/william.devena/Desktop/UCL/RESEARCH_PROJECT/QST/Data/djokovic/29/32060431"
    # dir_names = {}
    # for file in os.listdir(event_path):
    #     print(file)
    #     if ".bz2" in file:
    #         market_books = utils.read_prices_file(os.path.join(event_path, file))
    #         dir_names[file] = market_books[0]['marketDefinition']["name"]

    # pprint(dir_names)



    # dir_path = "/Users/william.devena/Desktop/UCL/RESEARCH_PROJECT/QST/Data/match_odds"
    # dict_data = {}
    # for root, dirs, files in os.walk(dir_path):
    #     #print(root)
    #     for file in files:
    #         if ".bz2" in file:


    #             market_books = utils.read_prices_file(os.path.join(root, file))
    #             event = market_books[0]['marketDefinition']['eventName']
    #             name = market_books[0]['marketDefinition']['name']

    #             if event in dir_names_and_events:
    #                 dir_names_and_events[event].append(name)
    #             else:
    #                 dir_names_and_events[event] = [name]













    #### STATS AND PLOTTING
    # paths = [
    #     "/Users/william.devena/Desktop/UCL/RESEARCH_PROJECT/QST/Data/matches/nadal_deminaur.bz2"
    # ]
    # dict_features = {}

    # for price_file in paths:
    #     file_name = price_file.split("/")[-1].split(".bz2")[0]
    #     dict_features[file_name], inplay_idx = data_analysis.extract_features_from_price_file(price_file=price_file)

    # # data_plotting.plot_dict_stats_from_price_file(dict_stats=dict_stats,
    # #                                               inplay_idx=inplay_idx,
    # #                                               plot_path="./plots")

    #     # data_analysis.calculate_stats_of_features(dict_features=dict_features[file_name])

    #     df_features = pd.DataFrame.from_dict(dict_features[file_name])
    #     data_analysis.profiling_df_features(df_features=df_features)


    path = "/Users/william.devena/Desktop/UCL/RESEARCH_PROJECT/QST/Data/matches/nadal_deminaur.bz2"

    df_aggregate_stats, df_missing_data = data_analysis.analyse_price_file(price_file_path=path,
                                     plot_path="./plots",
                                     profiling_path="")

    ## HANDLING MISSING DATA
    # handle_missing_data()

    print(df_aggregate_stats, df_missing_data)







    # with open('test.pkl', 'wb') as f:  # open a text file
    #      pickle.dump(dict, f) # serialize the list

    # with open('test.pkl', 'rb') as f:
    #     a = pickle.load(f) # deserialize using load()
    #     #print(a) # print student names

    #print("--- %s seconds ---" % (time.time() - start_time))

    # for item in alive_it(range(100)):   # <<-- wrapped items
    #     #print(item)
    #     time.sleep(1)







if __name__=="__main__":
    main()


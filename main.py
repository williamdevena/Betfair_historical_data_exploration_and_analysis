import logging
import os
import pickle
import time
from pprint import pprint

import betfairutil
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from alive_progress import alive_it

from src import (betfairutil_copy, constants, data_analysis, data_exploration,
                 data_plotting, data_processing)
from utils import pricefileutils, utils


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


    ## PRINT BET NAMES IN SINGLE EVENT FOLDER
    # event_path = "/Users/william.devena/Desktop/UCL/RESEARCH_PROJECT/QST/Data/djokovic/29/32060431"
    # event_names_dict = utils.get_bet_names_from_event_folder(event_path=event_path)
    # pprint(event_names_dict)



    ## PRINT BET NAMES FOR EACH EVENT IN DATA FOLDER
    # event_folder = "/Users/william.devena/Desktop/UCL/RESEARCH_PROJECT/QST/Data/match_odds/1"
    # dict_names_and_events = utils.get_bet_names_for_each_event(events_folder=event_folder)
    # pprint(dict_names_and_events)


    # ## HANDLING MISSING DATA
    # # handle_missing_data()


    ## DATA EXPLORATION
    data_exploration.data_exploration()







if __name__=="__main__":
    main()


import logging
import os
import pickle
import time
from pprint import pprint

import betfairutil
import dotenv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from alive_progress import alive_it

from src import data_analysis, data_exploration


def main():

    dotenv.load_dotenv()
    data_directory = os.environ.get("DATA_DIRECTORY")

    ## DATA EXPLORATION
    data_exploration.data_exploration()

    ## PRINT BET NAMES FOR EACH EVENT IN DATA FOLDER
    # event_folder = os.path.join(data_directory, "djokovic/29")
    # dict_names_and_events = utils.get_bet_names_for_each_event(events_folder=event_folder)
    # pprint(dict_names_and_events)


    # ## HANDLING MISSING DATA
    # ## (not implemented yet)
    # # handle_missing_data()



if __name__=="__main__":
    main()


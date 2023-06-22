import bz2
import json
import os
from datetime import datetime
from typing import Dict, List

import pandas as pd

from src import data_writing, runner_order_book


def parse_file(file_path: str) -> Dict[str, Dict]:
        """ Parse a file into a dictionary

        Args:
            file_path (str): File path to parse

        Returns:
            Dict[str, List]: Dictionary of parsed file
        """
        with open(file_path, "r") as file:
            market_data = []
            for line in file:
                market_data.append(json.loads(line))

        return market_data


def parse_historical_data(data: List) -> dict:
    markets = {}

   # with open(file_path, "r") as file:
    #    data = json.load(file)
     #   print("Dataset Size: ", len(data))

    for packet in data:
        time = packet["pt"]
        operation = packet["op"]

        if operation == "mcm":
            for market in packet["mc"]:
                if market["id"] not in markets:
                    markets.update({
                        market["id"]: {
                            time: market
                        }
                    })
                else:
                    markets[market["id"]].update({
                        time: market
                    })
    return markets



def save_markets(markets: dict, save_path: str) -> None:
    for market_id, market_data in markets.items():
        with open(os.path.join(save_path, f"{market_id}.json"), "w") as file:
            json.dump({"mcm": market_data}, file)



def get_order_book_history(runner_ids, max_load_limit, markets) -> runner_order_book.MarketOrderBookHistory:
    market_history = runner_order_book.MarketOrderBookHistory(runner_ids)
    market_data = markets[list(markets)[0]]
    counter = 0

    for timestamp, packet in market_data.items():
        market_history.update(timestamp, packet)

        counter += 1
        if counter > max_load_limit:
            print(f"Reached Limit: Processed {len(market_history)} packets")
            break
    return market_history




def convert_timestamp_to_datetime(timestamp: str) -> datetime:
    return datetime.fromtimestamp(int(timestamp)/1000)

def get_runner_data(runner_id, order_book_history):
    runner_history = order_book_history.get_runner_order_book(runner_id)
    game_start_time = convert_timestamp_to_datetime(runner_history.timestamps[0]).time()
    game_end_time = convert_timestamp_to_datetime(runner_history.timestamps[-1]).time()
    runner_timestamps = pd.to_datetime(runner_history.timestamps, unit='ms')

    data = pd.DataFrame({"Volume": runner_history.delta_tv_history,
                         "ATL Price": runner_history.atl_price_history,
                         "ATL Volume": runner_history.atl_volume_history,
                         "ATB Price": runner_history.atb_price_history,
                         "ATB Volume": runner_history.atb_volume_history,
                         "Close": runner_history.ltp_history,
                         "Total Volume": runner_history.tv_history},
                        index=runner_timestamps)
    return data, game_start_time, game_end_time




def extract_runners_id(markets):
    #print(list(markets.keys())[0])

    id = list(markets.keys())[0]
    id2 = list(markets[id].keys())[0]

    #print(markets[id][id2]['marketDefinition']['runners'])
    runners = markets[id][id2]['marketDefinition']['runners']

    # for runner in runners:
    #     print(runner['id'])

    return [runner['id'] for runner in runners]



def read_data_and_plot(file_path, plot_path):
    data_1, data_2 = read_data_from_file(file_path=file_path)
    file_dir = file_path.split("/")[-2]
    file_name = file_path.split("/")[-1]
    path_plot_runner_1 = os.path.join(plot_path, file_dir, file_name, "runner_1")
    path_plot_runner_2 = os.path.join(plot_path, file_dir, file_name, "runner_2")

    if not os.path.exists(path_plot_runner_1):
        os.makedirs(path_plot_runner_1)

    if not os.path.exists(path_plot_runner_2):
        os.makedirs(path_plot_runner_2)

    data_writing.plot_data(data=data_1, path=path_plot_runner_1)
    data_writing.plot_data(data=data_2, path=path_plot_runner_2)



def read_dir_and_plot(data_dir, plot_path):
    #data_dir = "/Users/william.devena/Desktop/UCL/RESEARCH PROJECT/QST/Data/PRO/2023/Jan/1"
    for dir in os.listdir(data_dir):
        #print(dir)
        dir_path = os.path.join(data_dir, dir)
        files = os.listdir(dir_path)
        for file in files:
            #print(file)
            if ".bz2" in file:
                unzipped_file = file.replace(".bz2", "")
                zipped_path = os.path.join(dir_path, file)
                unzipped_path = os.path.join(dir_path, unzipped_file)
                if unzipped_file not in files:
                    with open(zipped_path, 'rb') as source, open(unzipped_path, 'wb') as dest:
                        dest.write(bz2.decompress(source.read()))
                    read_data_and_plot(file_path=unzipped_path,
                                       plot_path=plot_path)
            else:
                unzipped_path = os.path.join(dir_path, file)
                read_data_and_plot(file_path=unzipped_path,
                                   plot_path=plot_path)



def read_data_from_file(file_path):
    data = parse_file(file_path=file_path)
    markets = parse_historical_data(data)

    runners = extract_runners_id(markets=markets)

    order_book_history = get_order_book_history(runner_ids=runners,
                                                                max_load_limit=40000,
                                                                markets=markets)

    runner_id1 = runners[0]
    data_1, game_start_time1, game_end_time1 = get_runner_data(runner_id=runner_id1,
                                                                        order_book_history=order_book_history)

    runner_id2 = runners[1]
    data_2, game_start_time2, game_end_time2 = get_runner_data(runner_id=runner_id2,
                                                                       order_book_history=order_book_history)

    return data_1, data_2
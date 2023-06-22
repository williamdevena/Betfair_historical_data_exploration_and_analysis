import os

from src import data_reading


def main():

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

    file_dir = "/Users/william.devena/Desktop/UCL/RESEARCH PROJECT/QST/Data/PRO2/2023/Jan/1"
    data_reading.read_dir_and_plot(data_dir=file_dir, plot_path="./plots2")

if __name__=="__main__":
    main()
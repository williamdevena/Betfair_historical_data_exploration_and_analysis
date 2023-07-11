import logging
import os

import matplotlib.pyplot as plt


def plot_dict_stats_from_price_file(dict_stats, inplay_idx, plot_path):
    plt.rcParams["figure.figsize"] = (10,5)
    for file_name, stats in dict_stats.items():
        #print(file_name)
        for stat, value in stats.items():
            if isinstance(value, list):
                logging.info(f"{stat}")
                plt.plot(value, label=stat)
                plt.axvline(x = inplay_idx, color = 'r', label = 'in-play')
                if "Mid price" in stat:
                    plt.ylim(0, 15)
                if "Matched" in stat:
                    plt.ylim(0, 20000)
                plt.legend()
                plt.title(stat)
                plt.savefig(os.path.join(plot_path, stat))
                plt.close()
            else:
                logging.info(f"{stat}: {value}")

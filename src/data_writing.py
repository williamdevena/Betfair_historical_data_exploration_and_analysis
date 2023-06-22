import os

import matplotlib.pyplot as plt


def plot_data(data, path):
        cols = ["Volume",
                #"ATL Price",
                #"ATL Volume",
                #"ATB Price",
                #"ATB Volume",
                "Close",
                "Total Volume"]

        for col in cols:
                plt.plot(data[col])
                plt.title(col)
                plt.savefig(os.path.join(path, col))
                plt.close()
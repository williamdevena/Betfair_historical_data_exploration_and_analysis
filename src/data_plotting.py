import logging
import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def plot_df_features_from_price_file(df_features, inplay_idx, plot_path):
    """
    This code block is used to generate a set of line plots and distribution plots for each feature in a given DataFrame.
    Each feature is both plotted as a time series and as a distribution. The point at which in-play begins is indicated with
    a vertical line in the line plot. The plots are saved to the specified path.

    Args:
        df_features (pandas.DataFrame): A DataFrame where each column is a feature to be plotted.
        inplay_idx (int): Index to represent the start of in-play in the line plot.
        plot_path (str): The path where the plots will be saved.

    """
    plt.rcParams["figure.figsize"] = (10,5)
    for feature_name, feature in df_features.items():
        ## LINE PLOT
        print(feature_name)
        plt.plot(feature, label=feature_name)
        plt.axvline(x = inplay_idx, color = 'r', label = 'in-play')

        if "Mid price" in feature_name:
            plt.ylim(0, 15)
        if "Matched" in feature_name:
            plt.ylim(0, 20000)

        if "Last traded price" in feature_name:
            plt.ylim(0, 20)

        plt.legend()
        plt.title(feature_name)
        plt.savefig(os.path.join(plot_path, feature_name))
        plt.close()

        ## DISTRIBUTION PLOT
        # sns.displot(feature, label=feature_name)
        # plt.legend()
        # plt.title(feature_name+" distribution")
        # plt.savefig(os.path.join(plot_path, feature_name)+"_distr")
        # plt.close()



def plot_correlation_matrix(df_features, plot_path):
    """
    This function plots the correlation matrix of the input DataFrame's features and saves the plot to a specified path.

    Args:
        df_features (pandas.DataFrame): A DataFrame whose features' correlation matrix is to be plotted.
        plot_path (str): The path where the plot will be saved.
    """
    corr_methods = ['pearson', 'kendall', 'spearman']

    for method in corr_methods:
        correlation_matrix = df_features.corr(method=method)
        mask = np.triu(correlation_matrix)
        f, ax = plt.subplots(figsize=(12, 9))
        sns.heatmap(correlation_matrix, square=False, annot=True, mask=mask)
        plt.savefig(os.path.join(plot_path, f"corr_matrix_{method}"))









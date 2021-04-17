import gzip
import pandas as pd
from sklearn.cluster import KMeans

# This file is for Michael


def parse(path):
    result = []
    g = gzip.open(path, "r")
    for l in g:
        result.append(eval(l))
    return result


def build_dataframe(path, num_samples, selected_cols):
    """
    Builds a dataframe from the repository of steam reviews keeping only the selected columns.
    Args:
        path:
        num_samples:

    Returns:

    """
    # Read data from file into Panda structure
    dataframe = pd.DataFrame(parse(path))

    # randomly select num_sample number of rows
    if num_samples != "MAX":
        dataframe = dataframe.sample(n=num_samples)
    print("Number of rows: " + str(len(dataframe.index)))
    print(dataframe.head())

    # Only keep selected columns
    dataframe = dataframe[selected_cols].copy()
    # print(dataframe.head())

    # One hot encode categorical columns
    categorical_cols = selected_cols  # temp
    dataframe = pd.get_dummies(dataframe, columns=categorical_cols)
    # print(dataframe.head())
    return dataframe


def kmeans_clustering(dataframe):
    kmeans = KMeans(n_clusters=2, random_state=0).fit(dataframe)
    centroids = kmeans.cluster_centers_
    print(centroids)
    return centroids


if __name__ == "__main__":
    # For steam_games.json.gz
    path = "../data/steam_games.json.gz"
    selected_cols = [
        "publisher", "app_name", "title", "developer", "sentiment"
    ]
    dataframe = build_dataframe(path, 1000, selected_cols)
    kmeans_clustering(dataframe)

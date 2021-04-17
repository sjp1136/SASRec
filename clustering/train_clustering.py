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
    dataframe = pd.DataFrame(parse(path))
    print(dataframe.head())

    # Only keep selected columns
    dataframe = dataframe[selected_cols].copy()
    print(dataframe.head())

    # One hot encode categorical columns
    categorical_cols = selected_cols  # temp
    onehotencode = pd.get_dummies(dataframe, columns=categorical_cols)
    dataframe = pd.concat([dataframe, onehotencode], axis=1)
    print(dataframe.head())
    return dataframe


def kmeans_clustering(dataframe):
    kmeans = KMeans(n_clusters=2, random_state=0).fit(dataframe)
    centroids = kmeans.cluster_centers_
    print(centroids)


if __name__ == "__main__":
    # Testing
    path = "../data/steam_games.json.gz"
    # selected_cols = [
    #     "publisher", "genres", "app_name", "title", "developer", "sentiment"
    # ]
    selected_cols = ["publisher"]
    dataframe = build_dataframe(path, "", selected_cols)
    # kmeans_clustering(dataframe)

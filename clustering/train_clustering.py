import gzip

import numpy as np

import pandas as pd
from sklearn.cluster import KMeans
from joblib import dump


# This file is for Michael


def parse(path):
    result = []
    g = gzip.open(path, "r")
    for l in g:
        result.append(eval(l))
    return result


def build_dataframe(path, num_samples, categorical_cols, num_cols):
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
    print(dataframe.columns)
    print("Number of rows: " + str(len(dataframe.index)))
    print(dataframe.head())
    for col in num_cols:
        dataframe[col] = pd.to_numeric(dataframe[col], errors="coerce").replace(np.NaN, 0)

    # Only keep selected columns
    dataframe = dataframe[categorical_cols + num_cols + ["id"]].copy()
    print(dataframe.columns)
    print("Number of rows: " + str(len(dataframe.index)))
    print(dataframe.head())

    # Only keep selected columns
    dataframe = dataframe[categorical_cols + num_cols + ["id"]].copy()

    # One hot encode categorical columns
    dataframe = pd.get_dummies(dataframe, columns=categorical_cols, prefix=categorical_cols)

    return dataframe


def kmeans_fit(data_frame, min_cluster=2, max_cluster=10, min_improvement=.25):
    last_loss = 0
    k_means_fit = None
    num_clusters = list(range(min_cluster, max_cluster))
    for i in range(len(num_clusters)):
        k_means = KMeans(n_clusters=num_clusters[i], random_state=0).fit(data_frame)
        if i == 0 or k_means.inertia_ <= last_loss * (1 - min_improvement):
            last_loss = k_means.inertia_
            k_means_fit = k_means
        else:
            break
    return k_means_fit


# def get_centroids(k_means):
#     kmeans = KMeans(n_clusters=2, random_state=0).fit(dataframe)
#     centroids = kmeans.cluster_centers_
#     print(centroids)
#     return centroids
def main():
    # For steam_games.json.gz
    path = "../data/steam_games.json.gz"
    cat_cols = [
        "publisher", "app_name", "title", "developer", "sentiment"
    ]
    num_cols = ["price"]
    dataframe = build_dataframe(path, 10000, cat_cols, num_cols)
    dataframe.to_csv("clustering_examples.csv", index=False)
    # cat_cols_one_hot = list(filter(lambda x: x in dataframe.columns, cat_cols))
    # dataframe = dataframe[cat_cols_one_hot + num_cols]
    dataframe.drop(labels=["id"], inplace=True, axis=1)
    print(dataframe.head())

    sol = kmeans_fit(dataframe, min_improvement=.2)
    with open("kmeans_fit.bin", "wb") as fp:
        dump(sol, fp)




if __name__ == "__main__":
    main()

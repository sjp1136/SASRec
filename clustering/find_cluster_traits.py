import sklearn
from joblib import load
import pandas as pd
import sys
import json


def find_cluster_attributes(k_means, all_items, item, num_features_use, cat_features_use):
    """

    Args:
        features_use: A list of features that will be used in the explanation
        k_means_labels: This is the second object returned by the k_means methods in sklearn, and provides
        the nearest centroid to the
        all_items: An ordered collection of all items in consideration in the same order as k_means_labels
        item: The input to SASRec for which the cluster is being examined.

    Returns: Dictionary of the form {"item_feature": cluster_value} ( This allows us to flexibly change how many
    features we are looking at to explain the item's selection. )
    """

    all_items["labels"] = k_means.labels_

    item_df = pd.DataFrame(item)
    item_df = item_df[num_features_use + cat_features_use].copy()
    item_df = pd.get_dummies(item_df, columns=num_features_use, prefix=cat_features_use)
    item_label = k_means.predict(item_df)[0]

    common_cluster = all_items[all_items.label == item_label]

    means = {}
    for feature in num_features_use:
        means["feature"] = common_cluster[feature].means()

    modes = {}
    for feature in cat_features_use:
        max_cnt = 0
        max_val = ""
        one_hot_cols = list(filter(lambda x: feature in x, common_cluster.columns))
        for col in one_hot_cols:
            curr_cnt = common_cluster[col].sum()
            if max_cnt < curr_cnt:
                curr_cnt = max_cnt
                max_val = col.lstrip(feature + "_")
        modes[feature] = max_val

    return modes, means


def main():
    k_means = load("clustering/kmeans_fit.bin")
    df = pd.read_csv("clustering_examples.csv", index_col=False)
    item_path = sys.argv[1]
    with open(item_path, "r") as fp:
        item = eval(fp.read())

    print(find_cluster_attributes(k_means, df, item, ["publisher", "app_name", "title", "developer"], ["price"]))


if __name__ == '__main__':
    main()

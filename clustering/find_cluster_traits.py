import json

import sklearn
from joblib import load
import pandas as pd
import sys


def get_item_label(item_dict, k_means, num_features_use, cat_features_use):
    item_df = pd.DataFrame(item_dict)
    item_df = item_df[num_features_use + cat_features_use].copy()
    item_df = pd.get_dummies(item_df, columns=num_features_use, prefix=cat_features_use)
    item_label = k_means.predict(item_df)[0]
    return item_label


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

    item_label = get_item_label(item, k_means, num_features_use, cat_features_use)

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
                max_cnt = curr_cnt
                max_val = col.lstrip(feature + "_")
        modes[feature] = max_val

    return modes, means


def main():
    with open("clustering/kmeans_fit.bin", "rb") as fp:
        k_means = load(fp)

    df = pd.read_csv("clustering_examples.csv", index_col=False)
    item_path = sys.argv[1]
    with open(item_path, "r") as fp:
        item = eval(fp.read())

    modes, means = find_cluster_attributes(k_means, df, item, ["publisher", "app_name", "title", "developer"],
                                           ["price"])


    with open("out.num_attrs.json", "w") as fp:
        json.dump(means, fp)
    with open("out.cat_attrs.json", "w") as fp:
        json.dump(modes, fp)


if __name__ == '__main__':
    main()

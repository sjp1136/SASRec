import sklearn


def find_cluster_attributes(k_means_labels, all_items, item, features_use):
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

    all_items["labels"] = k_means_labels

    item_label = all_items.loc[all_items.id == item["id"], ["label"]]

    common_cluster = all_items[all_items.label == item_label]

    modes = {}
    for feature in features_use:
        # TODO: Add code to decode one hot encoded attributes.
        modes["feature"] = common_cluster[feature].mode()

    return modes




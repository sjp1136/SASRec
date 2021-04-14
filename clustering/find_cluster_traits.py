import sklearn


def find_cluster_attributes(k_means_labels, all_items, item):
    """

    Args:
        k_means_labels: This is the second object returned by the k_means methods in sklearn, and provides
        the nearest centroid to the
        all_items: An ordered collection of all items in consideration in the same order as k_means_labels
        item: The input to SASRec for which the cluster is being examined.

    Returns: Dictionary of the form {"item_feature": cluster_value} ( This allows us to flexibly change how many
    features we are looking at to explain the item's selection. )
    """



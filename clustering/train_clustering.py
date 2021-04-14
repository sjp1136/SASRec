import gzip

# This file is for Michael

def parse(path):
    g = gzip.open(path, 'r')
    for l in g:
        yield eval(l)


def build_dataframe(path, num_samples, selected_cols):
    """
    Builds a dataframe from the repository of steam reviews keeping only the selected columns.
    Args:
        path:
        num_samples:

    Returns:

    """
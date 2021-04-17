import gzip
import pandas as pd

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
    drop_columns = dataframe[selected_cols].copy()
    print(drop_columns.head())
    return drop_columns


if __name__ == "__main__":
    # Testing
    build_dataframe("../data/steam_games.json.gz", "", ["publisher"])

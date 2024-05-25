import os
import csv
import pandas as pd


def save_csv(
    data: pd.DataFrame | list | set, path: str, name: str, enc: str, new="\n"
) -> str:
    """
    Saves Pandas DataFrames and Python iterables
    Args:
        data - the content to be saved
        path - str, location of intended directory
        name - str, filename
        enc - str, encoding (e.g. utf-8)
        new - str, newlines (e.g. \n)
    """
    filename = name + ".csv"
    filepath = os.path.join(path, filename)

    try:
        if isinstance(data, pd.DataFrame):
            data.to_csv(filepath, encoding=enc, index=False)

        else:
            with open(filepath, "w", encoding=enc, newline=new) as f:
                writer = csv.writer(f, delimiter=",")
                for element in data:
                    writer.writerow(str(element))

        return f"Saved {name}.csv with {enc} encoding"

    except Exception as e:
        return f"Save failed for {name}: {str(e)}"

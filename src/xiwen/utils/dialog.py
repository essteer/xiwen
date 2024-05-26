import csv
import os
import pandas as pd
from tkinter import filedialog
from xiwen.config import ENCODING, ENCODING_HANZI


def get_file_path():
    """
    Opens a Tkinter dialog to select a file
    If file selected, updates global selected_file_path
    """
    # Open file dialog to select file
    file_path = filedialog.askopenfilename(title="Select Text File")
    # Check if a file was selected
    if file_path:
        # Update global selected_file_path
        # global selected_file_path
        # selected_file_path = file_path
        return file_path


def is_valid_file(filename: str) -> bool:
    """
    Checks whether a selected file is compatible
    Args:
        - filename, str, the path of the selected file
    Returns:
        - bool, True if valid else False
    """
    extension = os.path.splitext(filename)[1].lower()
    if extension in (".pdf", ".csv", ".tsv", ".txt"):
        return True
    else:
        return False


def export_to_csv(data: pd.DataFrame | list, file_path=None):
    """
    Opens a Tkinter dialog to select a file save location
    If location selected, saves Pandas DataFrame or list to .csv
    Args:
        - data, Pandas DataFrame | list, data to be saved
    """
    filename = filedialog.asksaveasfilename(
        title="Save CSV File",
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
    )

    if filename:
        # Pandas DataFrames
        if isinstance(data, pd.DataFrame):
            data.to_csv(filename, index=False)

        # Lists
        elif isinstance(data, list):
            # Open file in write mode with UTF-8 encoding
            with open(filename, "w", newline="", encoding=ENCODING) as csvfile:
                # Write the CSV data to the file
                writer = csv.writer(csvfile)
                for row in data:
                    writer.writerow(row)

        # Coerce .csv to utf-8 encoding for hanzi display
        df = pd.read_csv(filename, encoding=ENCODING)
        df.to_csv(filename, encoding=ENCODING_HANZI, index=False)

        print(f"Exported to {filename}")

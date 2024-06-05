import csv
import os
import pandas as pd
import sys

sys.path.append("..")
from config import ENCODING, ENCODING_HANZI


def export_to_csv(data: pd.DataFrame | list):
    """
    Opens a Tkinter dialog to select a file save location
    If location selected, saves Pandas DataFrame or list to .csv

    Parameters
    ----------
    data, Pandas DataFrame | list
        data to be saved
    """
    filename = input("Enter file name: ")
    filename = os.path.join(os.getcwd(), "assets", filename)

    filename = filename.split(".")[0]
    filename = filename + ".csv"

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


def custom_export(
    hanzi_setlist: list[str], hanzi_df: pd.DataFrame, variant: str
) -> None:
    """
    Permits user to specify HSK grades for export

    Parameters
    ----------
    hanzi_setlist : list[str]
        list of unique characters found

    hanzi_df : pd.DataFrame
        df with counts applied by _get_counts()

    variant : str
        character variant of text
    """
    while True:
        selection = input("Enter HSK Grades or X to exit: ")

        if selection.upper() == "X":
            break

        try:
            assert selection.isdecimal()
            # Grades 7, 8, 9 share the same hanzi
            selection = selection.replace("8", "7").replace("9", "7")
            selection = list(set(selection))
            assert all("1" <= char <= "7" for char in selection)
            sorted_selection = sorted([int(char) for char in selection])
            custom_grades = [f"[{i}]" for i in sorted_selection]
            custom_grades = list(
                set(["[7-9]" if x == "[7]" else x for x in custom_grades])
            )
            # Export unique HSK hanzi in text - filter hanzi_df with custom_grades
            if variant == "Simplified":
                filtered_df = hanzi_df[hanzi_df["Simplified"].isin(hanzi_setlist)]
            else:
                # If traditional or unknown character variant, export based on traditional
                filtered_df = hanzi_df[hanzi_df["Traditional"].isin(hanzi_setlist)]
            # Filter based on grade selection
            filtered_grades_df = filtered_df[
                filtered_df["HSK Grade"].isin(custom_grades)
            ]
            print(filtered_grades_df)
            print("Selection displayed above.")

            # Confirm selection before export
            while True:
                print("Proceed to export? Enter y/n: ")
                command = input().upper()
                if command not in ["Y", "N"]:
                    continue
                elif command == "Y":
                    export_to_csv(filtered_grades_df)
                    break
                elif command == "N":
                    break

        except AssertionError:
            print("Enter digits from 1 to 9 only")

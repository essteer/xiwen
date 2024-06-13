import csv
import os
import pandas as pd
from .config import CUSTOM_EXPORT, ENCODING, ENCODING_HANZI, EXPORT_OPTIONS, PINYIN_PATH
from .pinyin import map_pinyin, get_pinyin


def export_to_csv(data: pd.DataFrame | list):
    """
    Saves dataframes to CSV

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
        selection = input("Enter HSK Grades (x to exit): ")

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
                print("Proceed y/n?: ")
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


def export_hanzi(
    zi_df: pd.DataFrame,
    st_df: pd.DataFrame,
    zi_list: list[str],
    out_list: list[str],
    var: str,
) -> bool:
    """
    Interactive loop for export options
    """
    options = ["A", "C", "F", "O", "S", "X"]
    while True:
        print(EXPORT_OPTIONS)
        command = input().upper()

        if command not in options:  # Repeat options
            continue

        elif command == "X":  # Exit to main screen
            return True

        elif command == "F":  # Export full HSK hanzi data
            export_to_csv(zi_df)

        elif command == "S":  # Export stats for this content
            export_to_csv(st_df)

        elif command == "A":  # Export all unique HSK hanzi in text
            hanzi_set = list(set(zi_list))  # filter zi_df with zi_list
            if var == "Simplified":
                filtered_df = zi_df[zi_df["Simplified"].isin(hanzi_set)]
            else:
                # If traditional or unknown, export based on traditional
                filtered_df = zi_df[zi_df["Traditional"].isin(hanzi_set)]
            export_to_csv(filtered_df)

        elif command == "O":  # Export outliers (non-HSK hanzi) in text
            # Map characters to accented pinyin
            pinyin_map = map_pinyin(PINYIN_PATH)
            # Get list of unique outlier hanzi
            outliers = list(set(out_list))
            # Get pinyin for outlier hanzi
            recognised_outliers, outliers_pinyin = get_pinyin(outliers, pinyin_map)
            # Create DataFrame of outlier hanzi, unicode, and pinyin
            outliers_df = pd.DataFrame(
                {
                    "Hanzi": recognised_outliers,
                    "Unicode": [ord(hanzi) for hanzi in recognised_outliers],
                    "Pinyin": outliers_pinyin,
                }
            )
            # Sort DataFrame on Unicode value
            outliers_df = outliers_df.sort_values(by="Unicode")
            # Export outliers
            export_to_csv(outliers_df)

        elif command == "C":
            print(CUSTOM_EXPORT)
            # Pass to custom export options
            unique_hanzi = list(set(zi_list))
            custom_export(unique_hanzi, zi_df, var)

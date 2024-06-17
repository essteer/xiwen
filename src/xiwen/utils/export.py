import os
import polars as pl
from .config import CUSTOM_EXPORT, EXPORT_OPTIONS
from .pinyin import map_pinyin, get_pinyin


def save_file(data: pl.DataFrame) -> None:
    """
    Saves dataframes to CSV or Parquet

    Parameters
    ----------
    data : pl.DataFrame
        data to be saved
    """
    print("Example: home/user/docs/xiwen.csv")
    filepath = input("Enter CSV (default) or Parquet file path (x to exit): ").strip()

    if not filepath or filepath.upper() == "X":
        print("No file path provided.")
        return

    try:
        # Get directory path and filename
        directory_path, filename = os.path.split(filepath)
        # Create dirs if they don't exist
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        if "." not in filename:
            filename += ".csv"

        extension = filename.split(".")[-1].lower()

        if extension == "csv":
            data.write_csv(os.path.join(directory_path, filename))
        elif extension == "parquet":
            data.write_parquet(os.path.join(directory_path, filename))
        else:
            print(f"Unsupported file extension: .{extension}")
            return

        print(f"Saved to {os.path.join(directory_path, filename)}")

    except Exception as e:
        print(f"Error saving to {os.path.join(directory_path, filename)}: {e}")


def custom_export(
    hanzi_setlist: list[str], hanzi_df: pl.DataFrame, variant: str
) -> None:
    """
    Permits user to specify HSK grades for export

    Parameters
    ----------
    hanzi_setlist : list[str]
        list of unique characters found

    hanzi_df : pl.DataFrame
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
            custom_grades = sorted([int(char) for char in selection])
            # Export unique HSK hanzi in text - filter hanzi_df with custom_grades
            if variant == "Simplified":
                filtered_df = hanzi_df.filter(pl.col("Simplified").is_in(hanzi_setlist))
            else:
                # If traditional or unknown character variant, export based on traditional
                filtered_df = hanzi_df.filter(
                    pl.col("Traditional").is_in(hanzi_setlist)
                )

            filtered_grades_df = filtered_df.filter(
                pl.col("HSK Grade").is_in(custom_grades)
            )

            with pl.Config(
                tbl_formatting="ASCII_MARKDOWN",
                tbl_hide_column_data_types=True,
                tbl_hide_dataframe_shape=True,
                set_tbl_cols=10,
                set_tbl_cell_numeric_alignment="RIGHT",
            ):
                print(filtered_grades_df)

            print("Selection displayed above.")
            # Confirm selection before export
            while True:
                print("Proceed y/n?: ")
                command = input().upper()
                if command == "Y":
                    save_file(filtered_grades_df)
                    break
                if command == "N":
                    break

        except AssertionError:
            print("Enter digits from 1 to 9 only")


def format_stats(stats: pl.DataFrame) -> pl.DataFrame:
    """
    Formats columns for stats dataframe
    Then passes dataframe to export function

    Parameters
    ----------
    stats : pl.DataFrame
        dataframe with stats for target content

    Returns
    -------
    stats : pl.DataFrame
        stats dataframe with formatted column names
    """
    for col in stats.columns:
        new_col = col.replace("\n", " ")
        stats = stats.rename({col: new_col})

    columns_to_format = [
        "% of Total Unique",
        "% of Cumul. Unique",
        "% of Total",
        "% of Cumul. Count",
    ]
    # Round floats
    for col in columns_to_format:
        stats = stats.with_columns(
            pl.col(col)
            .map_elements(lambda x: round(x, 2), return_dtype=pl.Float64)
            .alias(col)
        )

    return stats


def export_hanzi(
    hanzi_df: pl.DataFrame,
    stats_df: pl.DataFrame,
    hanzi_list: list[str],
    outliers_list: list[str],
    variant: str,
) -> bool:
    """
    Interactive loop for export options
    """
    options = ["A", "C", "F", "O", "S", "X"]
    while True:
        print(EXPORT_OPTIONS)
        command = input("Enter selection: ").upper()

        if command not in options:  # Repeat options
            continue

        elif command == "X":  # Exit to main screen
            return True

        elif command == "F":  # Export full HSK hanzi data
            save_file(hanzi_df)

        elif command == "S":  # Export stats for this content
            formatted_stats = format_stats(stats_df)
            save_file(formatted_stats)

        elif command == "A":  # Export all unique HSK hanzi in text
            hanzi_set = list(set(hanzi_list))  # filter hanzi_df with hanzi_list

            if variant == "Simplified":
                filtered_df = hanzi_df.filter(pl.col("Simplified").is_in(hanzi_set))
            else:
                # If traditional or unknown, filter based on traditional
                filtered_df = hanzi_df.filter(pl.col("Traditional").is_in(hanzi_set))

            save_file(filtered_df)

        elif command == "O":  # Export outliers (non-HSK hanzi) in text
            # Map characters to accented pinyin
            pinyin_map = map_pinyin()
            # Get list of unique outlier hanzi
            outliers = list(set(outliers_list))
            # Get pinyin for outlier hanzi
            recognised_outliers, outliers_pinyin = get_pinyin(outliers, pinyin_map)
            # Create DataFrame of outlier hanzi, unicode, and pinyin
            outliers_df = pl.DataFrame(
                {
                    "Hanzi": recognised_outliers,
                    "Unicode": [ord(hanzi) for hanzi in recognised_outliers],
                    "Pinyin": outliers_pinyin,
                }
            )
            # Sort DataFrame on Unicode value
            outliers_df = outliers_df.sort(by="Unicode")
            # Export outliers
            save_file(outliers_df)

        elif command == "C":
            print(CUSTOM_EXPORT)
            # Pass to custom export options
            unique_hanzi = list(set(hanzi_list))
            custom_export(unique_hanzi, hanzi_df, variant)

import os
import pandas as pd
from .data import process_data, analyse_data
from .export import custom_export, export_to_csv
from .pinyin import map_pinyin, get_pinyin
from .config import ASSETS_DIR, CUSTOM_EXPORT, EXPORT_OPTIONS, PINYIN_PATH


# Load HSK Hanzi database (unigrams only)
HSK_HANZI = pd.read_csv(os.path.join(ASSETS_DIR, "hsk30_hanzi.csv"))
# Replace HSK7-9 with 7 and convert grades to ints for iteration
HSK_HANZI["HSK Grade"] = HSK_HANZI["HSK Grade"].replace("7-9", 7)
HSK_HANZI["HSK Grade"] = HSK_HANZI["HSK Grade"].astype(int)
HSK_SIMP = list(HSK_HANZI["Simplified"])
HSK_TRAD = list(HSK_HANZI["Traditional"])


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


def extract_hanzi(html: str) -> None:
    """
    Passes HTML to functions to extract and process hanzi
    Passes results to interactive loop for export options

    Parameters
    ----------
    html : str
        HTML extracted from URL
    """
    # Get hanzi lists from file
    hanzi_list, simp, trad, outl = process_data(html, HSK_SIMP, HSK_TRAD)
    # Get hanzi stats
    variant, stats_df, hanzi_df = analyse_data(HSK_HANZI, hanzi_list, simp, trad)
    # Print stats to CLI
    print(stats_df.to_markdown(index=False))

    if variant == "Unknown":
        print("Character set undefined - stats for reference only")
    else:
        print(f"{variant.title()} character set detected")

    while True:
        print(
            "Select option:\n-> 'e' = see export options\n-> 'x' = exit to main screen\n"
        )
        command = input().upper()

        if command == "X":
            return  # Exit to main screen

        if command == "E":
            # Flag to break out of nested menus
            exit_to_main = export_hanzi(hanzi_df, stats_df, hanzi_list, outl, variant)

            if exit_to_main:
                return  # Exit to main screen

import os
import pandas as pd
import sys
from utils.data import process_data, analyse_data
from utils.export import custom_export, export_to_csv
from utils.pinyin import map_pinyin, get_pinyin

sys.path.append("..")
from config import ASSETS_DIR, CUSTOM_EXPORT, ENCODING, EXPORT_OPTIONS, PINYIN_PATH


# Load HSK Hanzi database (unigrams only)
HSK_HANZI = pd.read_csv(os.path.join(ASSETS_DIR, "hsk30_hanzi.csv"))
# Replace HSK7-9 with 7 and convert grades to ints for iteration
HSK_HANZI["HSK Grade"] = HSK_HANZI["HSK Grade"].replace("7-9", 7)
HSK_HANZI["HSK Grade"] = HSK_HANZI["HSK Grade"].astype(int)
HSK_SIMP = list(HSK_HANZI["Simplified"])
HSK_TRAD = list(HSK_HANZI["Traditional"])


def extract_hanzi(html: str) -> None:
    """
    Menu loops to handle:
        - viewing stats for a scanned file or URL
        - exporting content to csv

    Parameters
    ----------
    html : str
        HTML extracted from URL
    """
    # Get hanzi lists from file
    hanzi_list, simp, trad, neut, outl = process_data(html, HSK_SIMP, HSK_TRAD)
    # Get hanzi stats
    variant, stats_df, hanzi_df = analyse_data(HSK_HANZI, hanzi_list, simp, trad, neut)
    # Print stats to CLI
    print(stats_df.to_markdown(index=False))

    if variant == "unknown":
        print("Character set undefined - simplified and traditional hanzi present")
        print("Stats above for reference only")
    else:
        print(f"{variant.title()} character set detected")

    while True:
        # Flag to break out of nested menus
        exit_to_main = False
        print(
            "Select an option:\n-> 'e' = see export options\n-> 'x' = exit to main screen\n"
        )
        command = input().upper()

        if command not in ["E", "X"]:
            continue  # Repeat options

        elif command == "X":
            break  # Exit to main screen

        elif command == "E":
            while True:
                # Give export options
                print(EXPORT_OPTIONS)
                command = input().upper()

                if command not in ["A", "C", "F", "O", "S", "X"]:
                    continue  # Repeat options

                elif command == "X":
                    # Set flag to break out of parent loop to main screen
                    exit_to_main = True
                    break

                elif command == "F":
                    # Export all unique HSK hanzi
                    export_to_csv(hanzi_df)

                elif command == "A":
                    # Export all unique HSK hanzi in text - filter hanzi_df with hanzi_list
                    hanzi_set = list(set(hanzi_list))

                    if variant == "Simplified":
                        filtered_df = hanzi_df[hanzi_df["Simplified"].isin(hanzi_set)]
                    else:
                        # If traditional or unknown character variant, export based on traditional
                        filtered_df = hanzi_df[hanzi_df["Traditional"].isin(hanzi_set)]

                    export_to_csv(filtered_df)

                elif command == "S":
                    # Export stats - save stats_df
                    export_to_csv(stats_df)

                elif command == "O":
                    # Get mapping of characters to accented pinyin
                    pinyin_map = map_pinyin(PINYIN_PATH, ENCODING)
                    # Get list of unique outlier hanzi
                    outliers = list(set(outl))
                    # Get pinyin for outlier hanzi
                    recognised_outliers, outliers_pinyin = get_pinyin(
                        outliers, pinyin_map
                    )
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
                    unique_hanzi = list(set(hanzi_list))
                    custom_export(unique_hanzi, hanzi_df, variant)

        if exit_to_main:
            break  # exit extract_text() to main screen

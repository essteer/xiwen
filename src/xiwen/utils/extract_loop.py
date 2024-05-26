import pandas as pd
from utils.data import process_data, analyse_data
from utils.dialog import export_to_csv
from utils.pinyin import map_pinyin, get_pinyin
from xiwen.config import DATA_OUT, ENCODING, PINYIN_PATH


# Load HSK Hanzi database (unigrams only)
HSK_HANZI = pd.read_csv(DATA_OUT + "hsk30_hanzi.csv")
# Replace HSK7-9 with 7 and convert grades to ints for iteration
HSK_HANZI["HSK Grade"] = HSK_HANZI["HSK Grade"].replace("7-9", 7)
HSK_HANZI["HSK Grade"] = HSK_HANZI["HSK Grade"].astype(int)
HSK_SIMP = list(HSK_HANZI["Simplified"])
HSK_TRAD = list(HSK_HANZI["Traditional"])


def extract_hanzi(target: str, html: bool = False):
    """
    Menu loops to handle:
        - viewing stats for a scanned file or URL
        - exporting content to csv
    Args:
        - html, bool, flag True if url else False
        - target, str:
            - if url=False: path to file on device
            - if url=True: HTML extracted from URL
    Returns:
        - None
    """
    # Get hanzi lists from file
    hanzi_list, simp, trad, neut, outl = process_data(
        target, HSK_SIMP, HSK_TRAD, html=html
    )
    # Get hanzi stats
    variant, stats_df, hanzi_df = analyse_data(HSK_HANZI, hanzi_list, simp, trad, neut)

    # Print stats to CLI
    print(stats_df.to_markdown(index=False), "\n")

    if variant == "unknown":
        print("Character set undefined - simplified and traditional hanzi present\n")
        print("Stats above for reference only")
    else:
        print(f"{variant.title()} character set detected\n")

    while True:
        # Flag to break out of nested menus
        exit_to_main = False
        print(
            "Select an option:\n-> 'E' = see export options\n-> 'X' = exit to main screen\n"
        )
        command = input().upper()

        if command not in ["E", "X"]:
            # Repeat options
            continue

        elif command == "X":
            # Exit to main screen
            break

        elif command == "E":
            while True:
                # Give export options
                print(
                    "Select an option to export to .csv:\n-> 'A' = export all detected HSK hanzi (excludes outliers)\n-> 'C' = export custom HSK hanzi selection\n-> 'F' = export full HSK hanzi list\n-> 'O' = export detected outliers (non-HSK hanzi)\n-> 'S' = export stats\n-> 'X' = exit to main screen"
                )
                command = input().upper()

                if command not in ["A", "C", "F", "O", "S", "X"]:
                    # Repeat options
                    continue

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
                    print("\nCustom export:\n")
                    print("Enter the HSK grade(s) to export in any order")
                    print("-> e.g., to export HSK2 and HSK5, enter '25' or '52'")

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
                                set(
                                    [
                                        "[7-9]" if x == "[7]" else x
                                        for x in custom_grades
                                    ]
                                )
                            )

                            # Export unique HSK hanzi in text - filter hanzi_df with custom_grades
                            hanzi_set = list(set(hanzi_list))

                            if variant == "Simplified":
                                filtered_df = hanzi_df[
                                    hanzi_df["Simplified"].isin(hanzi_set)
                                ]
                            else:
                                # If traditional or unknown character variant, export based on traditional
                                filtered_df = hanzi_df[
                                    hanzi_df["Traditional"].isin(hanzi_set)
                                ]

                            # Filter based on grade selection
                            filtered_grades_df = filtered_df[
                                filtered_df["HSK Grade"].isin(custom_grades)
                            ]

                            print(filtered_grades_df)
                            print("\nSelection displayed above.")

                            # Confirm selection before export
                            while True:
                                print("Proceed to export? Enter Y/N: ")
                                command = input().upper()

                                if command not in ["Y", "N"]:
                                    continue

                                elif command == "Y":
                                    export_to_csv(filtered_grades_df)
                                    break

                                elif command == "N":
                                    break

                        except AssertionError:
                            print("\nEnter digits from 1 to 9 only\n")

        if exit_to_main:
            # exit extract_text() to main screen
            break

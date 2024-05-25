import pandas as pd
import random
import tkinter as tk
from src.config import DATA_OUT, TEST_FILES
from utils.data import process_data, analyse_data
from utils.dialog import get_file_path, is_valid_file
from utils.extract_html import extractor
from utils.extract_loop import extract_hanzi


# Load HSK Hanzi database (unigrams only)
HSK_HANZI = pd.read_csv(DATA_OUT + "hsk30_hanzi.csv")
# Replace HSK7-9 with 7 and convert grades to ints for iteration
HSK_HANZI["HSK Grade"] = HSK_HANZI["HSK Grade"].replace("7-9", 7)
HSK_HANZI["HSK Grade"] = HSK_HANZI["HSK Grade"].astype(int)
HSK_SIMP = list(HSK_HANZI["Simplified"])
HSK_TRAD = list(HSK_HANZI["Traditional"])
# Test case (simplified hanzi)
BJZD = TEST_FILES + "beijingzhedie.txt"
# Test case (traditional hanzi)
TTC = TEST_FILES + "taoteching.txt"


# Initialise Tkinter
ROOT = tk.Tk()


def handle_quit(self):
    """Closes Tkinter window on quit"""
    self.destroy()
    exit()


welcome_message = """
Welcome to Xiwen 析文
Xiwen scans text for traditional 繁體 and simplified 简体
Chinese characters (hanzi) to compare against HSK grades 1 to 9.
Load a file or choose a URL, and Xiwen will output a grade-by-grade
breakdown of the hanzi in the text.
Export hanzi for further use - including hanzi not in the HSK.
"""
print(welcome_message)


while True:
    # Main menu - get user command
    print(
        "Select an option:\n-> 'D' = demo\n-> 'S' = scan from device [.csv, .pdf, .tsv, .txt]\n-> 'U' = scan URL\n-> 'Q' = quit\n"
    )
    command = input().upper()
    # Invalid command
    if command not in ["D", "S", "U", "Q"]:
        # Repeat options
        continue
    # Quit command
    elif command == "Q":
        # Quit programme
        break
    # Valid "D", "S" or "U" command
    else:
        # "D" = Demo command
        if command == "D":
            print("Loading demo...")
            # Demo random choice of beijingzhedie.txt or taoteching.txt
            content = random.choice([BJZD, TTC])
            # Get hanzi lists
            hanzi_list, simp, trad, neut, outl = process_data(
                content, HSK_SIMP, HSK_TRAD
            )
            # Get hanzi stats
            variant, stats_df, hanzi_df = analyse_data(
                HSK_HANZI, hanzi_list, simp, trad, neut
            )
            # Print stats to CLI
            print(stats_df.to_markdown(index=False), "\n")
            print(f"Loaded {variant.lower()} character demo:")
            print(
                "-> '10+' under 'HSK Grade' captures any hanzi found beyond the HSK7-9 band."
            )
            print(
                "-> 'Unique' columns capture the number of unique hanzi in the text per grade."
            )
            print(
                "-> 'Count' columns capture the total number of hanzi per grade, duplicates included ('今天天氣很好' = 5 unique hanzi, 6 total hanzi)."
            )
            print(
                "-> '% of Total' gives the % of the figure on the left relative to all hanzi found in the text."
            )
            print(
                "-> 'Cumul No.' columns give the running totals per grade (the first 'Cumul. No.' column at the HSK3 row gives the sum of unique characters found that belong to HSK1, HSK2, and HSK3).\n"
            )
            print("This demo does not support file exports - select 'S'")
            print("at the main menu to select a file from your device")
            print("or try with the demo files in src/data/test_files.")
            # Continue to main screen loop
            continue

        # "S" = Scan command
        elif command == "S":
            # Initialise file path
            selected_file_path = None
            # Open dialog to get path of user-selected file
            selected_file_path = get_file_path()
            # Return to main screen if no file chosen
            if selected_file_path:
                # Confirm whether valid file type chosen
                valid_file = is_valid_file(selected_file_path)
                if not valid_file:
                    # Return to main screen if file invalid
                    print("Invalid file: please select from [.csv, .pdf, .tsv, .txt]\n")
                else:
                    print("Scanning document...")
                    # Read file and extract text
                    try:
                        extract_hanzi(selected_file_path)
                    except ZeroDivisionError:
                        print(
                            "No hanzi found: either none are present, or there's an issue with this format."
                        )
                        break
                    except Exception as e:
                        print(f"An error occurred: {e}")
                        break

            # Continue to main screen loop - no file chosen at "S"
            continue

        # "U" = URL command
        elif command == "U":
            # Get text from user-provided URL
            selected_url = None
            # Add user input dialog for URL
            selected_url = str(input("Enter target URL: "))

            if selected_url:
                print("Scanning for HTML...")
                # Send HTML to parser for text extraction
                try:
                    raw_html = extractor(selected_url)
                    if raw_html:
                        # Read HTML and extract text
                        try:
                            extract_hanzi(str(raw_html), html=True)
                        except ZeroDivisionError:
                            print(
                                f"No hanzi found: either none are present, or there's an issue reading '{selected_url}'."
                            )
                        except Exception as e:
                            print(f"An error occurred: {e}")

                except AssertionError:
                    print(f"Could not extract from '{selected_url}'")

                except Exception as e:
                    print(f"An error occurred: {e}")

            # Continue to main screen loop - no valid URL selected
            continue


# Exit Tkinter
handle_quit(ROOT)
ROOT.mainloop()

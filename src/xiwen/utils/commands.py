import pandas as pd
import random
from xiwen.config import ASSETS_DIR, BJZD, TTC, DEMO_MESSAGE
from utils.data import process_data, analyse_data
from utils.dialog import get_file_path, is_valid_file
from utils.extract_html import extractor
from utils.extract_loop import extract_hanzi

# Load HSK Hanzi database (unigrams only)
HSK_HANZI = pd.read_csv(ASSETS_DIR + "hsk30_hanzi.csv")
# Replace HSK7-9 with 7 and convert grades to ints for iteration
HSK_HANZI["HSK Grade"] = HSK_HANZI["HSK Grade"].replace("7-9", 7)
HSK_HANZI["HSK Grade"] = HSK_HANZI["HSK Grade"].astype(int)
HSK_SIMP = list(HSK_HANZI["Simplified"])
HSK_TRAD = list(HSK_HANZI["Traditional"])


def cmd_demo() -> None:
    """
    Demo command - shows example character analysis
    """
    # Demo random choice of beijingzhedie.txt or taoteching.txt
    content = random.choice([BJZD, TTC])
    # Get hanzi lists
    hanzi_list, simp, trad, neut, _ = process_data(content, HSK_SIMP, HSK_TRAD)
    # Get hanzi stats
    variant, stats_df, _ = analyse_data(HSK_HANZI, hanzi_list, simp, trad, neut)
    # Print stats to CLI
    print(stats_df.to_markdown(index=False))
    print(f"Loaded {variant.lower()} character demo:")
    print(DEMO_MESSAGE)


def cmd_scan() -> None:
    """
    Scan command - prompts user to select file
    """
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
            return

        try:  # Read file and extract text
            extract_hanzi(selected_file_path)
            return

        except ZeroDivisionError:
            print("No hanzi found: possible issue reading file.")
            return

        except Exception as e:
            print(f"An error occurred: {e}")
            return


def cmd_url() -> None:
    """
    URL command - prompts user to provide URL
    """
    # Get text from user-provided URL
    selected_url = None
    # Add user input dialog for URL
    selected_url = str(input("Enter target URL: "))
    if selected_url:
        print("Scanning for HTML...")
        # Send HTML to parser for text extraction
        try:
            raw_html = extractor(selected_url)

            if raw_html:  # Read HTML and extract text
                extract_hanzi(str(raw_html), html=True)
                return
            return

        except ZeroDivisionError:
            print(f"No hanzi found: possible issue reading '{selected_url}'.")
            return

        except Exception as e:
            print(f"An error occurred: {e}")
            return

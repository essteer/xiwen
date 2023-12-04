# -*- coding: utf-8 -*-
import csv
import os
import pandas as pd
import random
import tkinter as tk
from tkinter import filedialog
from utils.data_funcs import process_data, analyse_data
from utils.pinyin_funcs import map_pinyin, get_pinyin

##########################################################################
# Prepare files
##########################################################################

ENCODING = "utf-8"
ENCODING_HANZI = "utf_8_sig"
DATA_IN = "./data/input/"
DATA_OUT = "./data/output/"
TEST_FILES = "./data/test_files/"
# Initialise Tkinter
ROOT = tk.Tk()
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
# Pinyin for outliers
PINYIN_PATH = DATA_IN + "hanzi_pinyin_characters.tsv.txt"

##########################################################################
# Dialog and file handling
##########################################################################

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
        global selected_file_path
        selected_file_path = file_path


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


def export_to_csv(data: pd.DataFrame|list, file_path=None):
    """
    Opens a Tkinter dialog to select a file save location
    If location selected, saves Pandas DataFrame or list to .csv
    Args:
        - data, Pandas DataFrame | list, data to be saved
    """
    global ENCODING, ENCODING_HANZI
    
    filename = filedialog.asksaveasfilename(title="Save CSV File", defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

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
        
        print(f"\nExported to {filename}\n")


def handle_quit(self):
    """
    Closes Tkinter window on quit
    """
    self.destroy()
    exit()


##########################################################################
# Landing screen
##########################################################################

print("\nWelcome to Xiwen 析文\n")
print("Xiwen scans text for traditional 繁體 and simplified 简体")
print("Chinese characters (hanzi) to compare against HSK grades 1 to 9.\n")
print("Load a file and Xiwen will output a grade-by-grade") 
print("breakdown of the hanzi in the text.\n")
print("Export hanzi for further use - including hanzi not in the HSK.\n")

##########################################################################
# Interface
##########################################################################

while True:
    
    # Main menu - get user command
    print("Select an option:\n-> 'D' = demo\n-> 'S' = scan from device [.csv, .pdf, .tsv, .txt]\n-> 'U' = scan URL (coming soon)\n-> 'Q' = quit\n")
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
            print("\nLoading demo...\n")
            # Demo random choice of beijingzhedie.txt or taoteching.txt
            content = random.choice([BJZD, TTC])
            # Get hanzi lists
            hanzi_list, simp, trad, neut, outl = process_data(content, HSK_SIMP, HSK_TRAD)
            # Get hanzi stats
            variant, stats_df, hanzi_df = analyse_data(HSK_HANZI, hanzi_list, simp, trad, neut)
            # Print stats to CLI
            print(stats_df.to_markdown(index=False), "\n")
            print(f"Loaded {variant.lower()} character demo:\n")
            print("-> '10+' under 'HSK Grade' captures any hanzi found beyond the HSK7-9 band.")
            print("-> 'Unique' columns capture the number of unique hanzi in the text per grade.")
            print("-> 'Count' columns capture the total number of hanzi per grade, duplicates included ('今天天氣很好' = 5 unique hanzi, 6 total hanzi).")
            print("-> '% of Total' gives the % of the figure on the left relative to all hanzi found in the text.")
            print("-> 'Cumul No.' columns give the running totals per grade (the first 'Cumul. No.' column at the HSK3 row gives the sum of unique characters found that belong to HSK1, HSK2, and HSK3).\n")
            print("This demo does not support file exports - select 'S'")
            print("at the main menu to select a file from your device")
            print("or try with the demo files in src/data/test_files.\n")
            # Continue to main screen loop
            continue
        
        # "S" = Scan command
        elif command == "S":
            # Initialise file path
            selected_file_path = None
            # Open dialog to get path of user-selected file
            get_file_path()            
            # Return to main screen if no file chosen
            if selected_file_path:
                # Confirm whether valid file type chosen
                valid_file = is_valid_file(selected_file_path)
                if not valid_file:
                    # Return to main screen if file invalid
                    print("Invalid file: please select from [.csv, .pdf, .tsv, .txt]\n")
                
                else:
                    print("\nScanning document...\n")
                    # Read file and extract text
                    try:
                        # Get hanzi lists
                        hanzi_list, simp, trad, neut, outl = process_data(selected_file_path, HSK_SIMP, HSK_TRAD)
                        # Get hanzi stats
                        variant, stats_df, hanzi_df = analyse_data(HSK_HANZI, hanzi_list, simp, trad, neut)
                    except ZeroDivisionError:
                        print("\nNo hanzi found: either none are present, or there is an issue with this format.\n")
                        break
                    
                    # Print stats to CLI
                    print(stats_df.to_markdown(index=False), "\n")
                    
                    if variant == "unknown":
                        print("Character set undefined - simplified and traditional hanzi present\n")
                        print("Stats above for reference only")
                    else:
                        print(f"{variant.title()} character set detected\n")
                    
                    while True:
                        # Flag to break out of nested menus
                        return_to_main = False
                        print("Select an option:\n-> 'E' = see export options\n-> 'X' = exit to main screen\n")
                        command = input().upper()
                        
                        if command not in ["E", "X"]:
                            # Repeat options
                            continue
                        
                        elif command == "X":
                            # Exit to main screen
                            break
                        
                        elif command == "E":
                            while True:
                                exit_to_main = False
                                # Give export options
                                print("Select an option to export to .csv:\n-> 'A' = export all detected HSK hanzi (excludes outliers)\n-> 'C' = export custom HSK hanzi selection\n-> 'F' = export full HSK hanzi list\n-> 'O' = export detected outliers (non-HSK hanzi)\n-> 'S' = export stats\n-> 'X' = exit to main screen")
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
                                    outliers_pinyin = get_pinyin(outliers, pinyin_map)
                                    # Create DataFrame of outlier hanzi, unicode, and pinyin
                                    outliers_df = pd.DataFrame({
                                        "Hanzi": outliers, 
                                        "Unicode": [ord(hanzi) for hanzi in outliers],
                                        "Pinyin": outliers_pinyin
                                    })
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
                                            assert all('1' <= char <= '7' for char in selection)
                                            sorted_selection = sorted([int(char) for char in selection])
                                            
                                            custom_grades = [f"[{i}]" for i in sorted_selection]
                                            custom_grades = list(set(["[7-9]" if x == "[7]" else x for x in custom_grades]))
                                            
                                            # Export unique HSK hanzi in text - filter hanzi_df with custom_grades
                                            hanzi_set = list(set(hanzi_list))
                                            
                                            if variant == "Simplified":
                                                filtered_df = hanzi_df[hanzi_df["Simplified"].isin(hanzi_set)]
                                            else:
                                                # If traditional or unknown character variant, export based on traditional
                                                filtered_df = hanzi_df[hanzi_df["Traditional"].isin(hanzi_set)]
                                            
                                            # Filter based on grade selection
                                            filtered_grades_df = filtered_df[filtered_df["HSK Grade"].isin(custom_grades)]
                                            
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
                            # exit to main screen
                            break
            
            # Continue to main screen loop - no file chosen at "S"
            continue
        
        # "U" = URL command
        elif command == "U":
            # Get text from user-provided URL
            print("Not yet! URL support coming soon.\n")
            # Continue to main screen loop
            continue


# Exit Tkinter
handle_quit(ROOT)
ROOT.mainloop()

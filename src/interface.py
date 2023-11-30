# -*- coding: utf-8 -*-
import pandas as pd
import pprint
import random
import time
import tkinter as tk
from utils.hanzi_funcs import filter_text, partition_hanzi, identify, get_stats
from utils.save_data import save_csv

##########################################################################
# Prepare files
##########################################################################

ENCODING = "utf-8"
DATA_IN = "./data/input/"
DATA_OUT = "./data/output/"
TEST_FILES = "./data/test_files/"
# Load HSK Hanzi database (unigrams only)
HSK_HANZI = pd.read_csv(DATA_OUT + "hsk_hanzi.csv")
HSK_SIMP = list(HSK_HANZI["Simplified"])
HSK_TRAD = list(HSK_HANZI["Traditional"])
# Test case (simplified hanzi)
BJZD = TEST_FILES + "beijingzhedie.txt"
# Test case (traditional hanzi)
DDJ = TEST_FILES + "daodejing.txt"

##########################################################################
# Process data
##########################################################################

def process_data(location: str, hsk_simp: list, hsk_trad: list, enc: str="utf-8") -> tuple[list]:
    """
    Searches for and extracts Chinese characters (hanzi) from a text file
    according to whether they are simplified or traditional characters
    within the HSK1 to HSK6 vocabulary range, or other characters of either variant
    
    Args:
        - location, str, filepath of the text file
        - enc, str, encoding to use
    Returns:
        NOTE: all lists below include duplicates
        - hanzi_list, list, full list of hanzi found
        - simplified, list, full list of simplified hanzi found belonging to HSK1 to HSK6
        - traditional, list, full list of traditional hanzi found equivalent to HSK1 to HSK6
            simplified hanzi
        - neutral, list, subset of hanzi common to both simplified and traditional
        - outliers, list, all hanzi found that don't belong to the above lists
    """
    with open(location, "r", encoding=enc) as f:
        text = f.read()
    # Extract hanzi from text (with duplicates)
    hanzi_list = filter_text(text)
    # Divide into groups (with duplicates)
    simplified, traditional, neutral, outliers = partition_hanzi(hsk_simp, hsk_trad, hanzi_list)
    
    return hanzi_list, simplified, traditional, neutral, outliers


##########################################################################
# Analyse content
##########################################################################

def analyse_content(df: pd.DataFrame, hl: list, simplified: list, traditional: list, neutral: list) -> tuple[str|pd.DataFrame]:
    """
    Receives the output of process_data
    Gets the character variant and statistical breakdowns
        - number of unique characters and number of total characters
            by grade, and cumulative figures for the entire content
    Args:
        - df, Pandas DataFrame, HSK character list
        - hl, list, all hanzi in the entire content
        - simplified, list, simplified HSK hanzi in hl
        - traditional, list, traditional HSK hanzi in hl
        - neutral, list, hanzi common to simplified and traditional lists
    Returns:
        - variant, str, hanzi variant of the content
        - stats_dataframe, Pandas DataFrame, stats for the content
        - hanzi_dataframe, Pandas DataFrame, df with counts added
    """
    # Query character variant
    variant = identify(simplified, traditional, neutral)
    # Create mapping for analysis
    variants = {
        "Simplified": simplified, 
        "Traditional": traditional, 
        "Unknown": (simplified, traditional)
    }
    # Use copy of HSK_HANZI DataFrame for analysis
    hanzi_df = df.copy()
    # Get statistical breakdown of hanzi content
    stats_dataframe, hanzi_dataframe = get_stats(hanzi_df, hl, variants[variant], variant)
    
    return variant, stats_dataframe, hanzi_dataframe


##########################################################################
# Landing screen
##########################################################################

print("Welcome to Xiwen 析文\n")
time.sleep(1)
print("Xiwen scans for Chinese text in either traditional 繁體 or simplified 简体 form...\n")

print("...to compare against HSK grades 1 to 6.\n")

print("Load a file (.txt for now)...\n")
print("...and Xiwen will output a grade-by-grade breakdown of the hanzi in the text.\n")

print("Export the hanzi you need for further use - including hanzi not in the HSK.\n")
time.sleep(3)

##########################################################################
# Interface
##########################################################################

while True:
    
    # Main menu - get user command
    print("Select an option:\n-> 'D' = demo\n-> 'T' = scan .txt\n-> 'U' = scan URL (coming soon)\n-> 'Q' = quit\n")
    command = input().upper()
    
    if command not in ["D", "T", "U", "Q"]:
        # Repeat options
        continue
    
    elif command == "Q":
        # Quit
        break
    
    else:
        if command == "D":
            # Demo random choice of beijingzhedie.txt or daodejing.txt
            content = random.choice([BJZD, DDJ])
            # Get hanzi lists
            hanzi_list, simp, trad, neut, outl = process_data(content, HSK_SIMP, HSK_TRAD, ENCODING)
            # Get hanzi stats
            variant, stats_df, hanzi_df = analyse_content(HSK_HANZI, hanzi_list, simp, trad, neut)
            
            print(f"Loaded {variant.upper()} demo:\n")
            
            print(stats_df.to_markdown(index=False), "\n")
            
            print("-> '7+' under 'HSK Grade' captures any hanzi found beyond HSK6.\n")
            print("-> 'Unique' columns capture the number of unique hanzi in the text per grade.\n")
            print("-> 'Count' columns capture the total number of hanzi per grade, duplicates included.")
            print("---> So, '今天天氣很好' = 5 unique hanzi, 6 total hanzi.\n")
            print("-> '% of Total' gives the % of the figure on the left relative to all hanzi found in the text..\n")
            print("-> 'Cumul No.' gives the running totals per grade.")
            print("---> So, the first 'Cumul. No.' column at the HSK3 row gives the sum of unique characters found that belong to HSK1, HSK2, and HSK3.\n")
            
            continue
    
        elif command == "T":
            # Get text from file
            continue
        
        elif command == "U":
            # Get text from user-provided URL
            print("Not yet! URL scanning coming soon.\n")
            continue
    
    
    hanzi_list, simp, trad, neut, outl = process_data(content, HSK_SIMP, HSK_TRAD, ENCODING)

    variant, stats_df, hanzi_df = analyse_content(HSK_HANZI, hanzi_list, simp, trad, neut)

# -*- coding: utf-8 -*-
import pandas as pd
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
# Interface
##########################################################################

content = DDJ  # BJZD
# Process data for current file
hanzi_list, simp, trad, neut, outl = process_data(content, HSK_SIMP, HSK_TRAD, ENCODING)

variant, stats_df, hanzi_df = analyse_content(HSK_HANZI, hanzi_list, simp, trad, neut)

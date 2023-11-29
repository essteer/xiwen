# -*- coding: utf-8 -*-
import pandas as pd
from tqdm import tqdm
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

with open(BJZD, "r", encoding=ENCODING) as f:
    text = f.read()
# Extract hanzi from text (with duplicates)
hanzi_list = filter_text(text)
# Divide into groups (with duplicates)
simp, trad, neutral, outliers = partition_hanzi(HSK_SIMP, HSK_TRAD, hanzi_list)

##########################################################################
# Analyse content
##########################################################################

# Query character variant
variant = identify(simp, trad, neutral)
# Create mapping for analysis
variants = {
    "Simplified": simp, 
    "Traditional": trad, 
    "Unknown": (simp, trad)
}
# Use copy of HSK_HANZI DataFrame for analysis
hanzi_df = HSK_HANZI.copy()
# Get statistical breakdown of hanzi content
stats, hanzi_df = get_stats(hanzi_df, hanzi_list, variants[variant], variant)

print(stats)

# print(f"{num_hanzi:,} Chinese character{'s' if num_hanzi != 1 else ''} found,\nof which:")
# print(f"-> {len(simp):,} ({len(simp)/num_hanzi:.2%}) ∈ [HSK1, HSK6]")
# print(f"-> {len(neutral):,} ({len(neutral)/num_hanzi:.2%}) common to simp. and trad.")

# print(f"{num_unique:,} unique characters,\nof which:")
# unique_simp = set(simp)
# print(f"-> {len(unique_simp):,} ({len(unique_simp)/num_unique:.2%}) ∈ [HSK1, HSK6]")
# unique_outliers = set(outliers)

# print(f"-> {num_unique - len(unique_simp):,} ({len(unique_outliers)/num_unique:.2%}) > HSK6")

hsk_grade = HSK_HANZI[HSK_HANZI["Simplified"] == "爸"]["HSK Grade"].values[0]

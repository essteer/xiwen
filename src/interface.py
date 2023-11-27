# -*- coding: utf-8 -*-
import pandas as pd
from tqdm import tqdm
from utils.hanzi_funcs import filter_text, partition_hanzi, identify
from utils.save_data import save_csv

##########################################################################
# Prepare files
##########################################################################

ENCODING = "utf-8"
DATA_IN = "./data/input/"
DATA_OUT = "./data/output/"
# Load HSK Hanzi database (unigrams only)
HSK_HANZI = pd.read_csv(DATA_OUT + "hsk_hanzi.csv")
HSK_SIMP = list(HSK_HANZI["Simplified"])
HSK_TRAD = list(HSK_HANZI["Traditional"])
# Test case (simplified characters)
BEIJINGZHE = DATA_IN + "beijingzhe.txt"

##########################################################################
# Process data
##########################################################################

with open(BEIJINGZHE, "r", encoding=ENCODING) as f:
    text = f.read()

# Extract hanzi from text (with duplicates)
hanzi_list = filter_text(text)
# Divide into groups (with duplicates)
simp, trad, neutral, outliers = partition_hanzi(HSK_SIMP, HSK_TRAD, hanzi_list)

##########################################################################
# Analyse content
##########################################################################

num_hanzi = len(hanzi_list)
num_unique = len(set(hanzi_list))
# Query character variant
variant = identify(simp, trad, neutral)

print(f"=== Variant: {variant.title()} Chinese ===")

print(f"{num_hanzi:,} Chinese character{'s' if num_hanzi != 1 else ''} found,\nof which:")
print(f"-> {len(simp):,} ({len(simp)/num_hanzi:.2%}) ∈ [HSK1, HSK6]")
print(f"-> {len(neutral):,} ({len(neutral)/num_hanzi:.2%}) common to simp. and trad.")

print(f"{num_unique:,} unique characters,\nof which:")
unique_simp = set(simp)
print(f"-> {len(unique_simp):,} ({len(unique_simp)/num_unique:.2%}) ∈ [HSK1, HSK6]")
unique_others = set(outliers)

print(f"-> {num_unique - len(unique_simp):,} ({len(unique_others)/num_unique:.2%}) > HSK6")


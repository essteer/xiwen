# -*- coding: utf-8 -*-
import pandas as pd
from tqdm import tqdm
from utils.hanzi_funcs import filter_hanzi, partition_hanzi
from utils.save_data import save_csv

##########################################################################
# Prepare files and data
##########################################################################

ENCODING = "utf-8"
DATA_IN = "./data/input/"
DATA_OUT = "./data/output/"
# Load HSK Hanzi database (multi-character vocab removed)
HSK_HANZI = pd.read_csv(DATA_OUT + "hsk_hanzi.csv")
HSK_SIMP = list(HSK_HANZI["Simplified"])
HSK_TRAD = list(HSK_HANZI["Traditional"])
# Test case for simplified characters
BEIJINGZHE = DATA_IN + "beijingzhe.txt"

##########################################################################
# Analyse content
##########################################################################

with open(BEIJINGZHE, "r", encoding=ENCODING) as f:
    text = f.read()

hanzi_list = []
for char in text:
    if filter_hanzi(char):
        hanzi_list.append(char)

num_chars = len(hanzi_list)
num_unique = len(set(hanzi_list))

simp, trad, both, extra = partition_hanzi(HSK_SIMP, HSK_TRAD, hanzi_list)

##########################################################################
# Analyse content
##########################################################################

if set(trad) == set(both) and set(simp) > set(both):
    
    print("== Simplified Chinese dataset ==")

print(f"{num_chars:,} Chinese character{'s' if num_chars != 1 else ''} found,\nof which:")
print(f"-> {len(simp):,} ({len(simp)/num_chars:.2%}) ∈ [HSK1, HSK6]")
print(f"-> {len(both):,} ({len(both)/num_chars:.2%}) common to simp. and trad.")

print(f"{num_unique:,} unique characters,\nof which:")
unique_simp = set(simp)
print(f"-> {len(unique_simp):,} ({len(unique_simp)/num_unique:.2%}) ∈ [HSK1, HSK6]")
unique_others = set(extra)
assert len(unique_others) == num_unique - len(unique_simp)
print(f"-> {num_unique - len(unique_simp):,} ({len(unique_others)/num_unique:.2%}) > HSK6")


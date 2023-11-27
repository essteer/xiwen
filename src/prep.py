# -*- coding: utf-8 -*-
import pandas as pd
from tqdm import tqdm
from utils.save_data import save_csv

##########################################################################
# Prepare files
##########################################################################

ENCODING = "utf-8"
DATA_IN = "./data/input/"
DATA_OUT = "./data/output/"
HSK_PATH = DATA_IN + "HSK 2013 Pleco.txt"
FREQ_PATH = DATA_IN + "CharFreq-Modern-utf8.csv"

##########################################################################
# Initialise variables
##########################################################################

grade, counter = 0, 0
vocab_dict = {}
simp_chars, trad_chars = set(), set()

##########################################################################
# Extract HSK dataset to DataFrame
##########################################################################

with open(HSK_PATH, "r", encoding=ENCODING) as f:
    lines = f.readlines()
    for line in tqdm(lines, desc="Processing"):
        
        if "Level" in line:
            grade += 1
            continue
        
        try:
            chars, pinyin = line.split(maxsplit=1)
            pinyin = pinyin.strip().lower()
            # Split simplified and traditional
            simp, trad = chars.split("[")
            trad = trad.rstrip("]")
            vocab_dict[counter] = simp, trad, pinyin, grade
            
            # Add unique characters to sets
            s = [simp[i] for i in range(len(simp))]
            t = [trad[i] for i in range(len(trad))]
            for i in range(len(s)):
                simp_chars.add(s[i])
                trad_chars.add(t[i])
            
            counter += 1
            
        except ValueError:
            # Skip blank lines
            continue


cols = ["Simplified", "Traditional", "Pinyin", "HSK Grade"]
df = pd.DataFrame.from_dict(vocab_dict, orient="index", columns=cols)

##########################################################################
# Extract Jun Da MTSU character frequencies
##########################################################################

junda_freqs = []

with open(FREQ_PATH, "r", encoding=ENCODING) as f:
    lines = f.readlines()
    for line in tqdm(lines[6:], desc="Processing"):
        
        data = line.split(",")
        
        codepoint = ord(data[1])
        
        junda_freqs.append([data[1], int(data[0]), int(data[2]), float(data[3]), codepoint])
        

cols = ["Simplified", "JD Rank (2004)", "JD Frequency", "JD Percentile", "Unicode"]
junda_df = pd.DataFrame(junda_freqs, columns=cols)        

##########################################################################
# Map frequencies to HSK set
##########################################################################

hskhanzi_df = df.merge(junda_df[junda_df["Simplified"].isin(df["Simplified"])], on="Simplified")

##########################################################################
# Save files
##########################################################################

# save_csv(df,          DATA_OUT, "hsk_vocab",         ENCODING)
# save_csv(junda_df,    DATA_OUT, "junda_frequencies", ENCODING)
# save_csv(hskhanzi_df, DATA_OUT, "hsk_hanzi",         ENCODING)
# save_csv(simp_chars,  DATA_OUT, "hsk_simp_chars",    ENCODING)
# save_csv(trad_chars,  DATA_OUT, "hsk_trad_chars",    ENCODING)

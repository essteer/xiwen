# -*- coding: utf-8 -*-
import pandas as pd
from tqdm import tqdm
from utils.pinyin_funcs import map_pinyin, get_pinyin
from utils.save_data import save_csv

##########################################################################
# Prepare files
##########################################################################

ENCODING = "utf-8"
DATA_IN = "./data/input/"
DATA_OUT = "./data/output/"
HSK_PATH = DATA_IN + "HSK 2013 Pleco.txt"
FREQ_PATH = DATA_IN + "CharFreq-Modern-utf8.csv"
PINYIN_PATH = DATA_IN + "hanzi_pinyin_characters.tsv.txt"

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

# Get mapping of characters to accented pinyin
pinyin_map = map_pinyin(PINYIN_PATH, ENCODING)

for line in tqdm(lines, desc="Processing"):
# for line in lines:
    
    if "Level" in line:
        grade += 1
        continue
    try:
        # Split hanzi from pinyin
        chars, pinyin = line.split(maxsplit=1)
        pinyin = pinyin.strip().lower()
        # Split simplified and traditional
        simp, trad = chars.split("[")
        trad = trad.rstrip("]")
        
        # Add n-gram to vocab dict
        vocab_dict[counter] = simp, trad, pinyin, grade
        
        # Add unigrams directly
        if len(list(simp)) == 1 and len(list(trad)) == 1:
            simp_chars.add(simp)
            trad_chars.add(trad)
        
        else:
            assert len(simp) > 1 and len(simp) == len(trad)
            # Check for new component hanzi
            simp = list(simp)
            trad = list(trad)
            
            # Process pinyin
            pinyin = get_pinyin(trad, pinyin_map)
            
            for i in range(len(simp)):
                # Add new simp and trad hanzi
                if simp[i] not in simp_chars or trad[i] not in trad_chars:
                    counter += 1
                    
                    try:
                        vocab_dict[counter] = simp[i], trad[i], pinyin[i], grade
                        simp_chars.add(simp[i])
                        trad_chars.add(trad[i])
                    except IndexError:
                        print(f"pinyin list for {simp[i]}: {pinyin}")
                        break
                
        counter += 1
        
    except ValueError:
        # Skip blank lines
        continue


# DataFrame of full vocab list (unigrams, bigrams, n-grams)
cols = ["Simplified", "Traditional", "Pinyin", "HSK Grade"]
df = pd.DataFrame.from_dict(vocab_dict, orient="index", columns=cols)
# Drop duplicates - keep first instance
df.drop_duplicates(subset="Traditional", keep="first", inplace=True)

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

# DataFrame of Jun Da character frequencies
cols = ["Simplified", "JD Rank (2004)", "JD Frequency", "JD Percentile", "Unicode"]
junda_df = pd.DataFrame(junda_freqs, columns=cols)        

##########################################################################
# Map frequencies to HSK set
##########################################################################

# DataFrame of unique unigrams
hskhanzi_df = df.merge(junda_df[junda_df["Simplified"].isin(df["Simplified"])], on="Simplified")

##########################################################################
# Save files
##########################################################################

# save_csv(df,          DATA_OUT, "hsk_vocab",         ENCODING)
# save_csv(junda_df,    DATA_OUT, "junda_frequencies", ENCODING)
# save_csv(hskhanzi_df, DATA_OUT, "hsk_hanzi",         ENCODING)
# save_csv(simp_chars,  DATA_OUT, "hsk_simp_chars",    ENCODING)
# save_csv(trad_chars,  DATA_OUT, "hsk_trad_chars",    ENCODING)

# -*- coding: utf-8 -*-
import pandas as pd
from tqdm import tqdm

##########################################################################
# Prepare files
##########################################################################

ENCODING = "utf-8"
FILEPATH = "./data/HSK 2013 Pleco.txt"

##########################################################################
# Initialise variables
##########################################################################

grade, counter = 0, 0
vocab_dict = {}
simp_chars, trad_chars = set(), set()

##########################################################################
# Extract data
##########################################################################

with open(FILEPATH, "r", encoding=ENCODING) as f:
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

##########################################################################
# Extract data
##########################################################################

columns = ["Simplified", "Traditional", "Pinyin", "HSK Grade"]
df = pd.DataFrame.from_dict(vocab_dict, orient="index", columns=columns)

df.head()

        
        


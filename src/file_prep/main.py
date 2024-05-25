import pandas as pd
from tqdm import tqdm
from src.config import (
    ENCODING,
    ENCODING_HANZI,
    DATA_OUT,
    FREQ_PATH,
    HSK_PATH,
    PINYIN_PATH,
)
from src.xiwen.utils.pinyin import map_pinyin, get_pinyin
from utils.save_data import save_csv


##########################################################################
# Initialise variables
##########################################################################

grade, counter = 0, 0
vocab_dict = {}
simp_chars, trad_chars = set(), set()

##########################################################################
# Pinyin dataset
##########################################################################

# Get mapping of characters to accented pinyin
pinyin_map = map_pinyin(PINYIN_PATH, ENCODING)

##########################################################################
# Extract HSK dataset to DataFrame
##########################################################################

# Read ./data/hsk30-chars-ext.csv
df = pd.read_csv(HSK_PATH)
# Extract character columns and HSK grades
df = df[["Hanzi", "Traditional", "Level"]]
# Rename columns
df = df.rename(
    columns={"Hanzi": "Simplified", "Traditional": "Traditional", "Level": "HSK Grade"}
)
# Get pinyin based on traditional characters
trad_hanzi = df["Traditional"].tolist()
# pinyin_df = pd.DataFrame("Pinyin": get_pinyin(trad_hanzi, pinyin_map))
df["Pinyin"] = pd.DataFrame({"Pinyin": get_pinyin(trad_hanzi, pinyin_map)})

##########################################################################
# Add unicode for simplified and traditional hanzi
##########################################################################

df["Unicode (Simp.)"] = [ord(hanzi) for hanzi in df["Simplified"]]
df["Unicode (Trad.)"] = [ord(hanzi) for hanzi in df["Traditional"]]
# Reorder columns
cols = [
    "Simplified",
    "Unicode (Simp.)",
    "Traditional",
    "Unicode (Trad.)",
    "Pinyin",
    "HSK Grade",
]
df = df[cols]

##########################################################################
# Extract Jun Da MTSU character frequencies
##########################################################################

junda_freqs = []
# Read ./data/input/CharFreq-Modern-utf8.csv
with open(FREQ_PATH, "r", encoding=ENCODING) as f:
    lines = f.readlines()
    for line in tqdm(lines[6:], desc="Processing"):
        data = line.split(",")
        junda_freqs.append([data[1], int(data[0]), int(data[2]), float(data[3])])

# DataFrame of Jun Da character frequencies
cols = ["Simplified", "JD Rank", "JD Frequency", "JD Percentile"]
junda_df = pd.DataFrame(junda_freqs, columns=cols)

##########################################################################
# Map frequencies to HSK set
##########################################################################

# DataFrame of unique unigrams
hsk_hanzi_df = df.merge(
    junda_df[junda_df["Simplified"].isin(df["Simplified"])], on="Simplified"
)

##########################################################################
# Save files
##########################################################################

save_csv(junda_df, DATA_OUT, "junda_frequencies", ENCODING_HANZI)
save_csv(hsk_hanzi_df, DATA_OUT, "hsk30_hanzi", ENCODING_HANZI)

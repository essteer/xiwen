import os
import polars as pl
import sys

sys.path.append("..")
from xiwen.utils.pinyin import map_pinyin, get_pinyin


ENCODING = "utf-8"
RES_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
print(RES_ASSETS)

HSK_PATH = os.path.join(RES_ASSETS, "hsk30-chars-ext.csv")
FREQ_PATH = os.path.join(RES_ASSETS, "CharFreq-Modern-utf8.csv")


def load_HSK_dataset() -> pl.DataFrame:
    """
    Loads hsk30-chars-ext.csv
    Selects and renames columns
    Adds column for pinyin and unicode
    """
    # Read hsk30-chars-ext.csv
    frame = pl.read_csv(HSK_PATH)
    # Extract character columns and HSK grades
    frame = frame.select(["Hanzi", "Traditional", "Level"])
    # Rename columns
    frame = frame.rename(
        {"Hanzi": "Simplified", "Traditional": "Traditional", "Level": "HSK Grade"}
    )

    # Get pinyin based on traditional characters
    trad_hanzi = list(frame.select(["Traditional"]).to_series())
    # Get mapping of characters to accented pinyin
    pinyin_map = map_pinyin()
    pinyin = get_pinyin(trad_hanzi, pinyin_map)

    # Get unicode for simplified and traditional characters
    unicode_simp = [
        ord(hanzi) for hanzi in list(frame.select("Simplified").to_series())
    ]
    unicode_trad = [ord(hanzi) for hanzi in trad_hanzi]

    # Add new columns to the frame
    frame = frame.with_columns(
        [
            pl.Series("Pinyin", pinyin[1]),
            pl.Series("Unicode (Simp.)", unicode_simp),
            pl.Series("Unicode (Trad.)", unicode_trad),
        ]
    )
    # Reorder columns
    cols = [
        "Simplified",
        "Unicode (Simp.)",
        "Traditional",
        "Unicode (Trad.)",
        "Pinyin",
        "HSK Grade",
    ]
    frame = frame.select(cols)

    return frame


def load_junda_dataset() -> pl.DataFrame:
    """
    Loads junda_frequencies.csv
    Creates dataframe of Jun Da MTSU character frequencies
    """
    junda_freqs = []
    # Read CharFreq-Modern-utf8.csv
    with open(FREQ_PATH, "r", encoding=ENCODING) as f:
        lines = f.readlines()
        for line in lines[6:]:
            data = line.strip().split(",")
            junda_freqs.append([data[1], int(data[0]), int(data[2]), float(data[3])])

    # Define column names and create the DataFrame
    cols = ["Simplified", "JD Rank", "JD Frequency", "JD Percentile"]
    junda_df = pl.DataFrame(data=junda_freqs, schema=cols)

    return junda_df


# Extract HSK dataset
df = load_HSK_dataset()
# Extract Jun Da dataset
junda_df = load_junda_dataset()

# Map frequencies to HSK set with dataframe of unique unigrams
# Filter junda_df to include only rows where 'Simplified' is in df.select(['Simplified'])
filtered_junda_df = junda_df.filter(
    pl.col("Simplified").is_in(df.select(["Simplified"]))
)
# Join the filtered junda_df with df on the 'Simplified' column
hsk_hanzi_df = df.join(filtered_junda_df, on="Simplified", how="inner")

# Save files
# junda_df.write_csv(os.path.join(RES_ASSETS, "junda_frequencies.csv"))
# hsk_hanzi_df.write_csv(os.path.join(RES_ASSETS, "hsk30_hanzi.csv"))
hsk_hanzi_df.write_parquet(os.path.join(RES_ASSETS, "hsk30_hanzi.parquet"))

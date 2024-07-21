import os
import polars as pl


ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
PINYIN_PATH = os.path.join(ASSETS_DIR, "hanzi_pinyin_characters.tsv.txt")

# Test case (simplified hanzi)
DEMO1 = "https://www.xuan-zang.com/bjzd"
# Test case (traditional hanzi)
DEMO2 = "https://www.xuan-zang.com/ttc"
ENCODING = "utf-8"
HSK_GRADES = 7

HSK30_HANZI_SCHEMA = {
    "Simplified": pl.Utf8,
    "Unicode (Simp.)": pl.Int32,
    "Traditional": pl.Utf8,
    "Unicode (Trad.)": pl.Int32,
    "Pinyin": pl.Utf8,
    "HSK Grade": pl.Int8,
    "JD Rank": pl.Int16,
    "JD Frequency": pl.Int32,
    "JD Percentile": pl.Float64,
}

STATS_COLUMNS = {
    "HSK\nGrade": pl.Int8,
    "No. Hanzi\n(Unique)": pl.Int32,
    "% of\nTotal\nUnique": pl.Float64,
    "Cumul.\nUnique": pl.Int32,
    "% of\nCumul.\nUnique": pl.Float64,
    "No. Hanzi\n(Count)": pl.Int32,
    "% of\nTotal": pl.Float64,
    "Cumul.\nCount": pl.Int32,
    "% of\nCumul.\nCount": pl.Float64,
}

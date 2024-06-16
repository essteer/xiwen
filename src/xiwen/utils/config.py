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

WELCOME_MESSAGE = """
Welcome to Xiwen 析文
Xiwen scans text for traditional 繁體 and simplified 简体
Chinese characters (hanzi) to compare against HSK grades 1 to 9.
Load a file or choose a URL, and Xiwen will output a grade-by-grade
breakdown of the hanzi in the text.
Export hanzi for further use — including hanzi not in the HSK.
"""

MAIN_MENU_OPTIONS = "Enter URL (q: quit, blank: demo): "

DEMO_MESSAGE = """
-> '10' under 'HSK Grade' refers to hanzi beyond the HSK7-9 band.
-> 'Unique' cols capture no. unique hanzi found per grade.
-> 'Count' cols capture total no. hanzi found per grade.
    '今天天氣很好' = 5 unique hanzi, 6 total hanzi.
-> '% of Total' gives the % relative to all hanzi found.
-> 'Cumul' cols give the cumulative totals per grade
   'Cumul. Unique' col, HSK3 row gives the sum of unique hanzi found for HSK1, HSK2 and HSK3.
"""

EXPORT_OPTIONS = """
CSV export options
-> 'a' = all detected HSK hanzi (excludes outliers)
-> 'c' = custom HSK hanzi selection
-> 'f' = full HSK hanzi list
-> 'o' = outliers (non-HSK hanzi)
-> 's' = stats
-> 'x' = exit to main screen
"""

CUSTOM_EXPORT = """
Custom export:
Enter the HSK grade(s) to export in any order
-> e.g. to export HSK2 and HSK5 enter '25' or '52'
"""

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

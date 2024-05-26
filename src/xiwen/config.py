ENCODING = "utf-8"
# Encoding used to force .csv files to adopt utf-8 from Pandas DataFrame
ENCODING_HANZI = "utf_8_sig"
HSK_GRADES = 7

ASSETS_DIR = "./assets/"
# Test case (simplified hanzi)
BJZD = ASSETS_DIR + "beijingzhedie.txt"
# Test case (traditional hanzi)
TTC = ASSETS_DIR, +"taoteching.txt"

RAW_DATA = "file_prep/assets/"
HSK_PATH = RAW_DATA + "hsk30-chars-ext.csv"
FREQ_PATH = RAW_DATA + "CharFreq-Modern-utf8.csv"
PINYIN_PATH = RAW_DATA + "hanzi_pinyin_characters.tsv.txt"

WELCOME_MESSAGE = """
Welcome to Xiwen 析文
Xiwen scans text for traditional 繁體 and simplified 简体
Chinese characters (hanzi) to compare against HSK grades 1 to 9.
Load a file or choose a URL, and Xiwen will output a grade-by-grade
breakdown of the hanzi in the text.
Export hanzi for further use - including hanzi not in the HSK.
"""

MENU_OPTIONS = """
Select option:
-> 'd' = demo
-> 's' = scan file [.csv, .pdf, .tsv, .txt]
-> 'u' = scan URL
-> 'q' = quit
"""

DEMO_MESSAGE = """
-> '10+' under 'HSK Grade' refers to hanzi beyond the HSK7-9 band.
-> 'Unique' columns capture the no. unique hanzi in the text per grade.
-> 'Count' columns capture the total no. hanzi per grade, duplicates included
    ('今天天氣很好' = 5 unique hanzi, 6 total hanzi).")
-> '% of Total' gives the % of the left-hand value relative to all hanzi in the text.
-> 'Cumul No.' columns give the running totals per grade")
    (1st 'Cumul. No.' column, HSK3 row gives the sum of unique characters found that belong to HSK1, HSK2, and HSK3).
"""

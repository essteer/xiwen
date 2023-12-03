# -*- coding: utf-8 -*-
import os
import sys
sys.path.append('..')  # Add parent directory to path
import pandas as pd
from utils.hanzi_funcs import filter_text, partition_hanzi, identify

##########################################################################
# Prepare files
##########################################################################

# Absolute path to directory containing this script
TEST_DIR = os.path.dirname(os.path.abspath(__file__))

ENCODING = "utf-8"
# DATA_OUT = "./data/output/"
DATA_OUT = os.path.abspath("../data/output/")
# TEST_FILES = "./data/test_files/"
TEST_FILES = os.path.abspath("../data/test_files") + "/"

# Combine script directory with relative path to the file
filepath = os.path.join(DATA_OUT, "hsk30_hanzi.csv")
# Load HSK Hanzi database (unigrams only)
HSK_HANZI = pd.read_csv(filepath)
HSK_SIMP = list(HSK_HANZI["Simplified"])
HSK_TRAD = list(HSK_HANZI["Traditional"])

##########################################################################
# Test cases
##########################################################################

TEST_CASES = {
    # Simplified only
    "beijingzhedie.txt":    ["Simplified", 18896, 1751, 18647, 13477, 249], 
    # Traditional only
    "taoteching.txt":        ["Traditional", 5686, 810, 4390, 5466, 206], 
    # Latin alphabet (no hanzi)
    "iliad.txt":            ["Unknown", 0, 0, 0, 0, 0],
    # Unknown - 50:50 simplified : traditional 
    "ping50.txt":           ["Unknown", 360, 2, 180, 180, 0],
    # Unknown - 50:50 simplified : traditional
    "mix50.txt":            ["Unknown", 40, 40, 20, 20, 0],
    # Simplified - 90:10 simplified : traditional
    "mix90.txt":            ["Simplified", 20, 20, 18, 1, 1], 
    # Traditional - 10:90 simplified : traditional
    "mix10.txt":            ["Traditional", 20, 20, 1, 18, 1]
}

##########################################################################
# Test utils.hanzi_funcs.filter_text()
##########################################################################

print("=== TEST: utils.hanzi_funcs.filter_text() ===")
counter = 0

for test_case in TEST_CASES.keys():
    
    # Combine script directory with relative path to the file
    filepath = os.path.join(TEST_DIR, TEST_FILES + test_case)
    
    with open(filepath, "r", encoding=ENCODING) as f:
        text = f.read()
    
    # Extract hanzi from text (with duplicates)
    hanzi_list = filter_text(text)
    
    try:
        assert len(hanzi_list) == TEST_CASES[test_case][1]
        print(f"PASS: len({test_case +'))':<24} == {len(hanzi_list):,}")
        counter += 1
    
    except AssertionError:
        print(f"FAIL: len({test_case +'))':<25} != {len(hanzi_list)}")
    
    try:
        assert len(set(hanzi_list)) == TEST_CASES[test_case][2]
        print(f"PASS: len(set({test_case +'))':<20} == {len(set(hanzi_list)):,}")
        counter += 1
    
    except AssertionError:
        print(f"FAIL: len(set({test_case +'))':<20} != {len(set(hanzi_list)):,}")

print(f"utils.hanzi_funcs.filter_text(): {counter}/{len(TEST_CASES.keys())*2} PASSED\n")

##########################################################################
# Test utils.hanzi_funcs.partition_hanzi()
##########################################################################

print("=== TEST: utils.hanzi_funcs.partition_hanzi() ===")
counter = 0

for test_case in TEST_CASES.keys():
    
    # Combine script directory with relative path to the file
    filepath = os.path.join(TEST_DIR, TEST_FILES + test_case)
    
    with open(filepath, "r", encoding=ENCODING) as f:
        text = f.read()
    
    # Extract hanzi from text (with duplicates)
    hanzi_list = filter_text(text)
    # Divide into groups (with duplicates)
    simp, trad, neutral, outliers = partition_hanzi(HSK_SIMP, HSK_TRAD, hanzi_list)

    try:
        assert len(simp) == TEST_CASES[test_case][3]
        print(f"PASS: {test_case:<20} len(simp) == {TEST_CASES[test_case][3]:,}")
        counter += 1
    
    except AssertionError:
        print(f"FAIL: {test_case:<20} len(simp) != {TEST_CASES[test_case][3]:,}")
    
    try:
        assert len(trad) == TEST_CASES[test_case][4]
        print(f"PASS: {test_case:<20} len(trad) == {TEST_CASES[test_case][4]:,}")
        counter += 1
    
    except AssertionError:
        print(f"FAIL: {test_case:<20} len(trad) != {TEST_CASES[test_case][4]:,}")
        
    try:
        assert len(outliers) == TEST_CASES[test_case][5]
        print(f"PASS: {test_case:<20} len(outliers) == {TEST_CASES[test_case][5]:,}")
        counter += 1
    
    except AssertionError:
        print(f"FAIL: {test_case:<20} len(outliers) != {TEST_CASES[test_case][5]:,}")

print(f"utils.hanzi_funcs.partition_hanzi(): {counter}/{len(TEST_CASES.keys())*3} PASSED\n")

##########################################################################
# Test utils.hanzi_funcs.identify()
##########################################################################

print("=== TEST: utils.hanzi_funcs.identify() ===")
counter = 0

for test_case in TEST_CASES.keys():
    
    # Combine script directory with relative path to the file
    filepath = os.path.join(TEST_DIR, TEST_FILES + test_case)
    
    with open(filepath, "r", encoding=ENCODING) as f:
        text = f.read()
    
    # Extract hanzi from text (with duplicates)
    hanzi_list = filter_text(text)
    # Divide into groups (with duplicates)
    simp, trad, neutral, outliers = partition_hanzi(HSK_SIMP, HSK_TRAD, hanzi_list)
    
    # Query character variant
    variant = identify(simp, trad, neutral)
    
    try:
        assert variant == TEST_CASES[test_case][0]
        print(f"PASS: {test_case:<25} == {variant}")
        counter += 1
    
    except AssertionError:
        print(f"FAIL: {test_case:<25} != {variant}")

print(f"utils.hanzi_funcs.identify(): {counter}/{len(TEST_CASES.keys())} PASSED\n")

##########################################################################
# Test utils.hanzi_funcs.get_counts()
##########################################################################

# df_data = {"Simplified": ["爱", "八", "爸", "杯", "子"], "Traditional": ["愛", "八", "爸", "杯", "子"]}
# hanzi_simplified_data = ["爱", "八", "爸", "杯", "子"]
# hanzi_traditional_data = ["愛", "八", "爸", "杯", "子"]

# df = pd.DataFrame(df_data)
# result_df = get_counts(df, (hanzi_simplified_data, hanzi_traditional_data), "Undefined")
# print(result_df)

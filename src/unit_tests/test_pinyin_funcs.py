# -*- coding: utf-8 -*-
import os
import sys
sys.path.append('..')  # Add parent directory to path
from utils.pinyin_funcs import get_pinyin

##########################################################################
# Test cases
##########################################################################

PINYIN_DICT = {
            "你": "nǐ",
            "好": "hǎo",
            "吗": "ma",
            "不": "bù", 
            "茶": "chá", 
            "出": "chū", 
            "租": "zū", 
            "車": "chē"
}

SAMPLES = ["茶", "出", "租", "車", "你", "好", "吗", "不"]

##########################################################################
# Test utils.pinyin_funcs.get_pinyin()
##########################################################################

print("=== TEST: utils.pinyin_funcs.get_pinyin() ===")
counter = 0


pinyin = (get_pinyin(SAMPLES, PINYIN_DICT))

for i in range(len(pinyin)):
    
    try:
        assert pinyin[i] == PINYIN_DICT[SAMPLES[i]]
        print(f"PASS: {SAMPLES[i]} -> {pinyin[i]}")
        counter += 1
    except AssertionError:
        print(f"FAIL: {SAMPLES[i]} != {pinyin[i]}")
    
print(f"utils.pinyin_funcs.get_pinyin(): {counter}/{len(SAMPLES)} PASSED\n")



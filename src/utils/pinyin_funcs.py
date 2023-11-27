# -*- coding: utf-8 -*-

# DATA_IN = "../data/input/"
# PINYIN_PATH = DATA_IN + "hanzi_pinyin_characters.tsv.txt"

def map_pinyin(filepath: str, enc: str) -> dict:
    """
    Returns a dictionary mapping Chinese characters
    to pinyin
    """
    hanzi_pinyin_dict = {}
    
    with open(filepath, "r", encoding=enc) as f:
        
        for line in f:
            key, value = line.strip().split()
            hanzi_pinyin_dict[key] = value
    
    return hanzi_pinyin_dict


def special_cases(hanzi: str):
    """
    Polytonal characters
    Convention is to record these as main tone
    """
    exceptions = {"一": "yī", "不": "bù"} 
    try:
        return exceptions[hanzi]
    except KeyError:
        return False


def get_pinyin(hanzi: list[str], hanzi_pinyin_dict: dict[str: str]) -> list[str]:
    """
    Takes traditional characters from n-grams
    Gets the accented pinyin for each character
    Args:
        - hanzi, list of character strings
        - hanzi_pinyin_dict, dict mapping hanzi to pinyin
    Returns:
        - pinyin_list, list of pinyin mapped from each hanzi
    """
    pinyin_list = []
    
    for zi in hanzi:
        try:
            pinyin_list.append(hanzi_pinyin_dict[zi])
            
        except KeyError:
            print(f"{zi} not found in pinyin dict")
        
    return pinyin_list
    
    
##########################################################################
# split_pinyin unit tests
##########################################################################

# trad = ["茶"]
# pi = "chá"
# print(split_pinyin(trad, pi))

# trads = ["出", "租", "車"]
# pin = "chūzūchē"
# print(split_pinyin(trads, pin))

# -*- coding: utf-8 -*-

def filter_hanzi(char: str) -> bool:
    """
    Checks whether a character is a (possible)
    Chinese character against three Unicode sets:
        - Common        ["\u4E00", "\u9FFF"]
        - Extended-A    ["\u3400", "\u4DBF"]
        - Extended-B    ["\u20000", "\u2A6DF"]
    Args:
        - char, str (single character)
    Returns:
        - bool, True if char in Common | Extended-A | Extended-B
                False otherwise
    """
    exceptions = ["—", "‘", "’", "“", "”", "…"]
    
    if char in exceptions:
        return False
    
    common = char >= "\u4E00" and char <= "\u9FFF"
    ext_a = char >= "\u3400" and char <= "\u4DBF"
    ext_b = char >= "\u20000" and char <= "\u2A6DF"
    
    return True if common or ext_a or ext_b else False


def filter_text(text):
    """
    Passes text to filter_hanzi
    Returns list of hanzi in text
    """
    return [zi for zi in text if filter_hanzi(zi)]


def partition_hanzi(hsk_simp: list, hsk_trad: list, hanzi_list: list) -> tuple[list]:
    """
    Separates hanzi into lists based on whether
    they are HSK simplified or traditional characters
    Args:
        - hsk_simp, list, simplified characters in HSK1 to HSK6
        - hsk_trad, list, traditional equivalents to hsk_simp
        - hanzi_list, list, characters to partition
    Returns:
        - simp, list, simplified HSK characters in hanzi_list
        - trad, list, traditional HSK equivalents in hanzi_list
        - neutral, list, characters common to simp and trad
        - outliers, list, characters not in above lists
    """
    simp      = [zi for zi in hanzi_list if zi in hsk_simp]
    trad      = [zi for zi in hanzi_list if zi in hsk_trad]
    neutral   = [zi for zi in hanzi_list if zi in simp and zi in trad]
    outliers  = [zi for zi in hanzi_list if zi not in simp and zi not in trad]
    
    return simp, trad, neutral, outliers


def identify(hsk_simp: list, hsk_trad: list, neutral: list) -> tuple[str, float]:
    """
    Identifies text as either simp, trad, or undefined
    Args:
        - hsk_simp, list, simplified characters in HSK1 to HSK6
        - hsk_trad, list, traditional equivalents to hsk_simp
        - neutral, list, characters common to simp and trad
    Returns:
        - str, text character variant
    """
    threshold = 0.8
    simp_set = set(hsk_simp) - set(neutral)
    trad_set = set(hsk_trad) - set(neutral)
    
    try:
        ratio = len(simp_set) / (len(simp_set) + len(trad_set))
        if ratio >= threshold:
            return "simplified"
        elif ratio <= 1 - threshold:
            return "traditional"
        else:
            return "undefined"
        
    except ZeroDivisionError:
        return "undefined"
    
    
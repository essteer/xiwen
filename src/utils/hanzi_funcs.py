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
                else False
    """
    exceptions = ["—", "‘", "’", "“", "”", "…"]
    
    if char in exceptions:
        return False
    
    common = char >= "\u4E00" and char <= "\u9FFF"
    ext_a = char >= "\u3400" and char <= "\u4DBF"
    ext_b = char >= "\u20000" and char <= "\u2A6DF"
    
    
    return True if common or ext_a or ext_b else False


def partition_hanzi(hsk_simp: list, hsk_trad: list, hanzi_list: list) -> tuple[list]:
    """
    Separates hanzi into lists based on whether
    they are HSK simplified or traditional characters
    Args:
        - hsk_simp, list, simplified characters in HSK1 to HSK6
        - hsk_trad, list, traditional equivalents to hsk_simp
        - hsk_both, list, HSK characters with no simplified version
        - hanzi_list, list, characters to partition
    Returns:
        - simp, list, simplified HSK characters in hanzi_list
        - trad, list, traditional HSK equivalents in hanzi_list
        - both, list, characters common to simp and trad
        - extra, list, characters not in HSK1 to HSK6
    """
    simp   = [hanzi for hanzi in hanzi_list if hanzi in hsk_simp]
    trad   = [hanzi for hanzi in hanzi_list if hanzi in hsk_trad]
    both   = [hanzi for hanzi in hanzi_list if hanzi in simp and hanzi in trad]
    extra  = [hanzi for hanzi in hanzi_list if hanzi not in simp and hanzi not in trad]
    
    return simp, trad, both, extra
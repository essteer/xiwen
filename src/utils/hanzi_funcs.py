# -*- coding: utf-8 -*-

def hanzi_filter(char: str) -> bool:
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
    common = char >= "\u4E00" and char <= "\u9FFF"
    ext_a = char >= "\u3400" and char <= "\u4DBF"
    ext_b = char >= "\u20000" and char <= "\u2A6DF"
    
    return True if common or ext_a or ext_b else False

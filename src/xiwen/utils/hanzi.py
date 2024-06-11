import sys


def _filter_hanzi(char: str) -> bool:
    """
    Checks whether a character is a (possible)
    Chinese character against three Unicode sets:
        - Common        ["\u4e00", "\u9fff"]
        - Extended-A    ["\u3400", "\u4dbf"]
        - Extended-B    ["\u20000", "\u2a6dF"]

    Parameters
    ----------
    char : str
        a single character

    Returns
    -------
    bool
        True if char in Common | Extended-A | Extended-B
        False otherwise
    """
    symbols = ["–", "—", "‘", "’", "“", "”", "…", "⊼", "⁆", "∕", "。"]
    # Unrecognised hanzi with no matching pinyin
    exceptions = ["㤙"]

    if ord(char) in range(8206, 8287):
        return False

    if char in symbols or char in exceptions:
        return False

    common = char >= "\u4e00" and char <= "\u9fff"
    ext_a = char >= "\u3400" and char <= "\u4dbf"
    ext_b = char >= "\u20000" and char <= "\u2a6dF"

    return True if common or ext_a or ext_b else False


def filter_text(html: str) -> list[str]:
    """
    Passes text to _filter_hanzi
    Returns list of hanzi in text

    Parameters
    ----------
    html : str
        HTML extracted from URL
    """
    return [zi for zi in html if _filter_hanzi(zi)]


def identify(hsk_simp: list, hsk_trad: list) -> str:
    """
    Identifies text as Simplified or Traditional based on character ratio

    Parameters
    ----------
    hsk_simp : list
        simplified characters in HSK1 to HSK7-9

    hsk_trad : list
        traditional equivalents to hsk_simp

    Returns
    -------
    str
        text character variant
    """
    # Threshold beyond which to decide that text belongs to one variant
    epsilon = sys.float_info.epsilon
    threshold = 0.90
    simp_set = set(hsk_simp) - set(hsk_trad)
    trad_set = set(hsk_trad) - set(hsk_simp)

    if len(simp_set) + len(trad_set) == 0:
        return "Unknown"

    ratio = len(simp_set) / (len(simp_set) + len(trad_set))
    if ratio >= threshold - epsilon:
        return "Simplified"

    elif ratio <= 1 - threshold + epsilon:
        return "Traditional"

    return "Unknown"


def partition_hanzi(hsk_simp: list, hsk_trad: list, hanzi_list: list) -> tuple[list]:
    """
    Separates hanzi list into sublists based on whether
    they are HSK simplified characters or traditional character equivalents
    or outliers (both simplified and traditional) not in the HSK lists

    Parameters
    ----------
    hsk_simp : list
        simplified characters in HSK1 to HSK7-9

    hsk_trad : list
        traditional equivalents to hsk_simp

    hanzi_list : list
        characters to partition

    Returns
    -------
    simp : list
        simplified HSK characters in hanzi_list

    trad : list
        traditional HSK equivalents in hanzi_list

    outliers : list
        characters not in above lists
    """
    simp = [zi for zi in hanzi_list if zi in hsk_simp]
    trad = [zi for zi in hanzi_list if zi in hsk_trad]
    outliers = [zi for zi in hanzi_list if zi not in simp and zi not in trad]

    return simp, trad, outliers

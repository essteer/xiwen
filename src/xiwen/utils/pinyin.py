def map_pinyin(filepath: str, enc: str) -> dict:
    """
    Returns a dictionary mapping Chinese characters to pinyin
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


def get_pinyin(hanzi: list[str], hanzi_pinyin_dict: dict[str:str]) -> tuple[list[str]]:
    """
    Takes traditional characters from n-grams
    Gets the accented pinyin for each character

    Parameters
    ----------
    hanzi : list
        character strings

    hanzi_pinyin_dict : dict
        map of hanzi to pinyin

    Returns
    -------
    matched_hanzi : list
        hanzi for which pinyin matches were found in hanzi_pinyin_dict

    pinyin_list : list
        pinyin mapped from each hanzi
    """
    pinyin_list = []
    # Return an updated list to ignore hanzi without pinyin
    matched_hanzi = []

    for zi in hanzi:
        try:
            pinyin_list.append(hanzi_pinyin_dict[zi])
            matched_hanzi.append(zi)

        except KeyError:
            print(f"{zi} not found in pinyin dict")

    return matched_hanzi, pinyin_list

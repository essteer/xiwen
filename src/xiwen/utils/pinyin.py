from .config import ENCODING, PINYIN_PATH


def map_pinyin() -> dict:
    """
    Returns a dictionary mapping Chinese characters to pinyin
    """
    hanzi_pinyin_dict = dict()

    with open(PINYIN_PATH, "r", encoding=ENCODING) as f:
        for line in f:
            key, value = line.strip().split()
            hanzi_pinyin_dict[key] = value

    return hanzi_pinyin_dict


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
        if zi in hanzi_pinyin_dict:
            pinyin_list.append(hanzi_pinyin_dict[zi])
            matched_hanzi.append(zi)

    return matched_hanzi, pinyin_list

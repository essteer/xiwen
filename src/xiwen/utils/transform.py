from .hanzi import get_HSKHanzi_instance


def partition_hanzi(hanzi_list: list) -> tuple[list]:
    """
    Separates hanzi list into sublists based on whether
    they are HSK simplified characters or traditional character equivalents
    or outliers (both simplified and traditional) not in the HSK lists

    Parameters
    ----------
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
    hsk_simp = get_HSKHanzi_instance().HSK_SIMP
    hsk_trad = get_HSKHanzi_instance().HSK_TRAD

    simp = [zi for zi in hanzi_list if zi in hsk_simp]
    trad = [zi for zi in hanzi_list if zi in hsk_trad]
    outliers = [zi for zi in hanzi_list if zi not in simp and zi not in trad]

    return simp, trad, outliers

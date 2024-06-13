def partition_hanzi(hanzi_list: list, hsk_simp: list, hsk_trad: list) -> tuple[list]:
    """
    Separates hanzi list into sublists based on whether
    they are HSK simplified characters or traditional character equivalents
    or outliers (both simplified and traditional) not in the HSK lists

    Parameters
    ----------
    hanzi_list : list
        characters to partition

    hsk_simp : list
        all simplified characters in HSK

    hsk_trad : list
        traditional character equivalents to HSK characters

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

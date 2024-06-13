import os
import pandas as pd
from .config import ASSETS_DIR

# Load HSK Hanzi database (unigrams only)
HSK_HANZI = pd.read_csv(os.path.join(ASSETS_DIR, "hsk30_hanzi.csv"))
# Replace HSK7-9 with 7 and convert grades to ints for iteration
HSK_HANZI["HSK Grade"] = HSK_HANZI["HSK Grade"].replace("7-9", 7)
HSK_HANZI["HSK Grade"] = HSK_HANZI["HSK Grade"].astype(int)
HSK_SIMP = list(HSK_HANZI["Simplified"])
HSK_TRAD = list(HSK_HANZI["Traditional"])


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
    simp = [zi for zi in hanzi_list if zi in HSK_SIMP]
    trad = [zi for zi in hanzi_list if zi in HSK_TRAD]
    outliers = [zi for zi in hanzi_list if zi not in simp and zi not in trad]

    return simp, trad, outliers

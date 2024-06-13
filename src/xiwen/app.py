import os
import pandas as pd
from utils.analysis import analyse
from utils.config import ASSETS_DIR
from utils.extract import get_hanzi
from utils.transform import partition_hanzi

# Load HSK Hanzi database (unigrams only)
HSK_HANZI = pd.read_parquet(os.path.join(ASSETS_DIR, "hsk30_hanzi.parquet"))
# Replace HSK7-9 with 7 and convert grades to ints for iteration
HSK_HANZI["HSK Grade"] = HSK_HANZI["HSK Grade"].replace("7-9", 7)
HSK_HANZI["HSK Grade"] = HSK_HANZI["HSK Grade"].astype(int)
HSK_SIMP = list(HSK_HANZI["Simplified"])
HSK_TRAD = list(HSK_HANZI["Traditional"])


def coordinator(target: str, terminal: bool = False):
    """
    Handles calls throughout pipeline

    Parameters
    ----------
    target : str
        URL to extract HTML from
    """
    # Run URL
    hanzi_list = get_hanzi(target)

    if hanzi_list:
        # Divide into groups (with duplicates)
        simp, trad, outl = partition_hanzi(hanzi_list, HSK_SIMP, HSK_TRAD)

        if simp or trad or outl:
            # Get info about character set
            variant, stats_df, hanzi_df = analyse(hanzi_list, simp, trad, HSK_HANZI)

            if terminal and variant:
                return hanzi_df, stats_df, hanzi_list, outl, variant

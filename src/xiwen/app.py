from .utils.analyse import analyse
from .utils.extract import get_hanzi
from .utils.transform import partition_hanzi


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
        simp, trad, outl = partition_hanzi(hanzi_list)

        if simp or trad or outl:
            # Get info about character set
            variant, stats_df, hanzi_df = analyse(hanzi_list, simp, trad)

            if terminal and variant:
                return hanzi_df, stats_df, hanzi_list, outl, variant

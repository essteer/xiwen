from .utils.analyse import analyse_hanzi
from .utils.extract import get_hanzi_from_url
from .utils.transform import partition_hanzi


def coordinator(target: str, terminal: bool = False):
    """
    Handles calls throughout pipeline

    Parameters
    ----------
    target : str
        URL to extract HTML from
    """
    hanzi_list = get_hanzi_from_url(target)

    if hanzi_list:
        simp_chars, trad_chars, outlier_chars = partition_hanzi(hanzi_list)

        if simp_chars or trad_chars or outlier_chars:
            # Get info about character set
            variant, stats_df, hanzi_df = analyse_hanzi(
                hanzi_list, simp_chars, trad_chars
            )

            if terminal and variant:
                return hanzi_df, stats_df, hanzi_list, outlier_chars, variant

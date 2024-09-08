from .utils.analyse import analyse_hanzi
from .utils.extract import get_hanzi_from_url
from .utils.transform import partition_hanzi


def coordinator(target_url: str):
    """
    Handles calls throughout pipeline

    Parameters
    ----------
    target_url : str
        URL to extract HTML from
    """
    hanzi_list = get_hanzi_from_url(target_url)

    if hanzi_list:
        simplified, traditional, outliers = partition_hanzi(hanzi_list)

        if simplified or traditional:
            hanzi_df, stats_df, variant = analyse_hanzi(
                hanzi_list, simplified, traditional
            )

            return hanzi_df, stats_df, hanzi_list, outliers, variant

import pandas as pd
from utils.hanzi import filter_text, partition_hanzi, identify
from utils.stats import get_stats


def process_data(html: str, hsk_simp: list, hsk_trad: list) -> tuple[list]:
    """
    Searches for and extracts Chinese characters (hanzi) from html
    according to whether they are simplified or traditional characters
    within the HSK1 to HSK6 vocabulary range, or other characters of either variant

    Parameters
    ----------
    html : str
        HTML extracted from URL

    hsk_simp : list
        all simplified hanzi from HSK1 to HSK9

    hsk_trad : list
        all traditional hanzi equivalents to hsk_simp

    Returns
    -------  NOTE: all lists below include duplicates
    hanzi_list : list
        full list of hanzi found

    simplified : list
        full list of simplified hanzi found belonging to HSK1 to HSK9

    traditional : list
        full list of traditional hanzi found equivalent to HSK1 to HSK9 simplified hanzi

    outliers : list
        all hanzi found that don't belong to the above lists
    """
    # Extract hanzi from HTML (with duplicates)
    hanzi_list = filter_text(html)
    # Divide into groups (with duplicates)
    simplified, traditional, outliers = partition_hanzi(hsk_simp, hsk_trad, hanzi_list)

    return hanzi_list, simplified, traditional, outliers


def analyse_data(
    df: pd.DataFrame, hl: list, simplified: list, traditional: list
) -> tuple[str | pd.DataFrame]:
    """
    Receives output of process_data
    Gets character variant and statistical breakdowns
        - number of unique characters and number of total characters
          by grade, and cumulative figures for the entire content

    Parameters
    ----------
    df : pd.DataFrame
        HSK character list

    hl : list
        all hanzi in the entire content

    simplified : list
        simplified HSK hanzi in hl

    traditional : list
        traditional HSK hanzi in hl

    Returns
    -------
    variant : str
        hanzi variant of the content

    stats_dataframe : pd.DataFrame
        stats for the content

    hanzi_dataframe : pd.DataFrame
        df with counts added
    """
    # Query character variant
    variant = identify(simplified, traditional)
    # Create mapping for analysis
    variants = {
        "Simplified": simplified,
        "Traditional": traditional,
        "Unknown": (simplified, traditional),
    }
    # Use copy of HSK_HANZI DataFrame for analysis
    hanzi_df = df.copy()
    # Get statistical breakdown of hanzi content
    stats_dataframe, hanzi_dataframe = get_stats(
        hanzi_df, hl, variants[variant], variant
    )

    return variant, stats_dataframe, hanzi_dataframe

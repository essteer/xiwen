import polars as pl
from .hsk_hanzi import get_HSKHanzi_instance


def filter_dataframe_by_hanzi_variant(df: pl.DataFrame, variant: str):
    """
    Breaks down counts by HSK grades

    Parameters
    ----------
    df : pl.DataFrame
        all unique hanzi in HSK1 to HSK7-9 with counts column

    variant : str
        variant of the character set (Simplified|Traditional|Unknown)

    Returns
    -------
    filtered_df : pl.DataFrame
        df after filtering for appropriate character variant
    """
    if variant in ("Simplified", "Traditional"):
        """
        Drop duplicate entries - cases where:
        - if Simplified: 1 simplified hanzi maps to >= 2 traditional hanzi
            example: "为": ["為", "爲"]
        - if Traditional: 1 traditional hanzi maps to >= 2 simplified hanzi
            example: "蘋": ["苹", "𬞟"]
        Keep only the first instance in either case to avoid double-counting
        """
        filtered_df = df.unique(subset=[variant], keep="first", maintain_order=True)
    else:
        """
        If the variant is unknown:
        - assume the broadest range of hanzi (Traditional)
        - drop duplicate Simplified hanzi only when the counts are identical
        """
        filtered_df = df.unique(
            subset=["Simplified", "Count"], keep="first", maintain_order=True
        )
    return filtered_df


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
    simplified : list
        simplified HSK characters in hanzi_list

    traditional : list
        traditional HSK equivalents in hanzi_list

    outliers : list
        characters not in above lists
    """
    hsk_simplified = get_HSKHanzi_instance().HSK_SIMP
    hsk_traditional = get_HSKHanzi_instance().HSK_TRAD

    simplified = [zi for zi in hanzi_list if zi in hsk_simplified]
    traditional = [zi for zi in hanzi_list if zi in hsk_traditional]
    outliers = [
        zi for zi in hanzi_list if zi not in simplified and zi not in traditional
    ]

    return simplified, traditional, outliers

# -*- coding: utf-8 -*-
import pandas as pd
import sys

def _filter_hanzi(char: str) -> bool:
    """
    Checks whether a character is a (possible)
    Chinese character against three Unicode sets:
        - Common        ["\u4E00", "\u9FFF"]
        - Extended-A    ["\u3400", "\u4DBF"]
        - Extended-B    ["\u20000", "\u2A6DF"]
    Args:
        - char, str (single character)
    Returns:
        - bool, True if char in Common | Extended-A | Extended-B
                False otherwise
    """
    symbols = ["。", "—", "‘", "’", "“", "”", "…"]
    
    if char in symbols:
        return False
    
    common = char >= "\u4E00" and char <= "\u9FFF"
    ext_a = char >= "\u3400" and char <= "\u4DBF"
    ext_b = char >= "\u20000" and char <= "\u2A6DF"
    
    return True if common or ext_a or ext_b else False


def filter_text(text):
    """
    Passes text to _filter_hanzi
    Returns list of hanzi in text
    """
    return [zi for zi in text if _filter_hanzi(zi)]


def partition_hanzi(hsk_simp: list, hsk_trad: list, hanzi_list: list) -> tuple[list]:
    """
    Separates hanzi list into sublists based on whether
    they are HSK simplified characters or traditional character equivalents,
    neutral characters found in both the HSK simplified and traditional lists,
    or outliers (both simplified and traditional) not in the HSK lists
    
    Args:
        - hsk_simp, list, simplified characters in HSK1 to HSK6
        - hsk_trad, list, traditional equivalents to hsk_simp
        - hanzi_list, list, characters to partition
    Returns:
        - simp, list, simplified HSK characters in hanzi_list
        - trad, list, traditional HSK equivalents in hanzi_list
        - neutral, list, characters common to simp and trad
        - outliers, list, characters not in above lists
    """
    simp      = [zi for zi in hanzi_list if zi in hsk_simp]
    trad      = [zi for zi in hanzi_list if zi in hsk_trad]
    neutral   = [zi for zi in hanzi_list if zi in simp and zi in trad]
    outliers  = [zi for zi in hanzi_list if zi not in simp and zi not in trad]
    
    return simp, trad, neutral, outliers


def identify(hsk_simp: list, hsk_trad: list, neutral: list) -> tuple[str, float]:
    """
    Identifies text as either simplified or traditional Chinese, 
        or unknown if the variant is uncertain
    Args:
        - hsk_simp, list, simplified characters in HSK1 to HSK6
        - hsk_trad, list, traditional equivalents to hsk_simp
        - neutral, list, characters common to simp and trad
    Returns:
        - str, text character variant
    """
    # Threshold beyond which to decide that text belongs to one variant
    epsilon = sys.float_info.epsilon
    threshold = 0.90
    simp_set = set(hsk_simp) - set(neutral)
    trad_set = set(hsk_trad) - set(neutral)
    
    try:
        ratio = len(simp_set) / (len(simp_set) + len(trad_set))
        if ratio >= threshold - epsilon:
            return "Simplified"
        elif ratio <= 1 - threshold + epsilon:
            return "Traditional"
        else:
            return "Unknown"
        
    except ZeroDivisionError:
        return "Unknown"


def _counts(hanzi: list) -> dict:
    """
    Counts occurrences of each character in hanzi
    in list passed by get_counts()
    Args:
        - hanzi, list, characters to count
    Returns:
        - counts, dict, counts of each character
    """
    counts = {}
    for zi in hanzi:
            counts[zi] = counts.get(zi, 0) + 1
    return counts


def _granular_counts(df: pd.DataFrame, hanzi_all: list, variant: str) -> list:
    """
    Breaks down counts according to HSK grades for
    Pandas DataFrame passed by get_counts()
    Args:
        - df, Pandas DataFrame, all unique hanzi in HSK1 to HSK6
            with counts column
        - hanzi_all, list, all hanzi (with duplicates) found in text being analysed
        - variant, str, the variant of the character set (Simplified|Traditional|Unknown)
    Returns:
        - dict, counts for hanzi per HSK grade
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
        df.drop_duplicates(subset=variant, keep="first", inplace=True)
    
    else:
        """
        If the variant is unknown:
        - assume the broadest range of hanzi (Traditional)
        - drop duplicate Simplified hanzi only when the counts are identical
        """
        df.drop_duplicates(subset=["Simplified", "Count"], keep="first", inplace=True)
    
    # Dict to store stats
    grade_stats = {}
    
    # Get stats for full text including non-HSK characters (outliers)
    num_total_hanzi = len(hanzi_all)
    num_total_unique_hanzi = len(set(hanzi_all))
    # Reserve key "0" for full figures
    grade_stats[0] = num_total_hanzi, num_total_unique_hanzi
    
    # Get counts for each grade HSK1 to HSK6 and store in grade_stats
    for i in range(1, 7):
        grade_count  = df.loc[df["HSK Grade"] == i, "Count"].sum()
        grade_unique = (df.loc[df["HSK Grade"] == i, "Count"] != 0).sum()
        grade_stats[i] = grade_count, grade_unique
        
    return grade_stats


def _get_counts(df: pd.DataFrame, hanzi_all: list, hanzi_sub: list|tuple[list], variant: str):
    """
    Passes hanzi_sub to _counts to count occurrences of each Chinese character
    Passes updated df and hanzi_all to _granular_counts for grade-by-grade breakdown
    
    Args:
        - df, Pandas DataFrame, all unique characters in HSK1 to HSK6
        - hanzi_all, list, all characters (with duplicates) found in text being analysed
        - hanzi_sub, list | tuple, the character subset(s) to be analysed
            single list if variant defined as either simplified or traditional
            tuple of simplified and traditional lists if variant unknown
        - variant, str, the variant of the character set (Simplified|Traditional|Unknown)
    Returns:
        - counts, dict, aggregate and grade-based character counts
        - merged_df, Pandas DataFrame, df with counts applied
    """
    # hanzi_sub = single list if variant defined (Simplified|Traditional)
    if isinstance(hanzi_sub, list):
        # Count occurrences of each character in hanzi_sub
        counts = _counts(hanzi_sub)
        # Create DataFrame from counts dictionary
        counts_df = pd.DataFrame(list(counts.items()), columns=[variant, "Count"])
        # Merge on variant column
        merged_df = pd.merge(df, counts_df, on=variant, how="left")
    
    # hanzi_sub = tuple of (Simplified, Traditional) characters if variant unknown
    else:        
        simp = hanzi_sub[0]
        # Avoid double-counting characters common to both variants
        trad = [zi for zi in hanzi_sub[1] if zi not in simp]
        # Count occurrences of each character
        s_counts = _counts(simp)
        t_counts = _counts(trad)
        
        # Count both character variants for undefined cases
        simp_counts_df = pd.DataFrame(list(s_counts.items()), columns=["Simplified", "Count"])
        trad_counts_df = pd.DataFrame(list(t_counts.items()), columns=["Traditional", "Count"])
        
        # Merge variant counts separately
        merged_df = pd.merge(df, simp_counts_df, on="Simplified", how="left")
        merged_df = pd.merge(merged_df, trad_counts_df, on="Traditional", how="left")
        
        # Create mask for rows with identical variants
        identical_mask = merged_df["Simplified"] == merged_df["Traditional"]
        
        # Sum counts for rows with different variants (not identical_mask)
        merged_df.loc[~identical_mask, "Count"] = (
            merged_df["Count_x"].fillna(0) + merged_df["Count_y"].fillna(0)
        )
        # Take either count for rows with identical variants
        merged_df.loc[identical_mask, "Count"] = merged_df["Count_x"].fillna(0)
        
        # Drop unnecessary columns
        merged_df.drop(columns=["Count_x", "Count_y"], inplace=True)
    
    # Fill NaN as 0 and convert counts to integers
    merged_df["Count"] = merged_df["Count"].fillna(0).astype(int)
    
    counts = _granular_counts(merged_df, hanzi_all, variant)
    
    return counts, merged_df


def get_stats(df: pd.DataFrame, hanzi_all: list, hanzi_sub: list|tuple[list], variant: str):
    """
    Passes params to _get_counts() for hanzi counts and
        merged_df with counts applied
    Computes cumulative counts per grade and total
    
    Args:
        - df, Pandas DataFrame, all unique characters in HSK1 to HSK6
        - hanzi_all, list, all characters (with duplicates) found in text being analysed
        - hanzi_sub, list | tuple, the character subset(s) to be analysed
            single list if variant defined as either simplified or traditional
            tuple of simplified and traditional lists if variant unknown
        - variant, str, the variant of the character set (Simplified|Traditional|Unknown)
    Returns:
        - stats, dict, aggregate and cumulative grade-based character counts
        - hanzi_df, Pandas DataFrame, df with counts applied by _get_counts()
    """
    
    # Get count breakdown of hanzi content
    counts, hanzi_df = _get_counts(df, hanzi_all, hanzi_sub, variant)
    
    # No need to process manually - for planning only
    # all_hanzi,  all_unique  = counts[0][0], counts[0][1]
    # hsk1_hanzi, hsk1_unique = counts[1][0], counts[1][1]
    # hsk2_hanzi, hsk2_unique = counts[2][0], counts[2][1]
    # hsk3_hanzi, hsk3_unique = counts[3][0], counts[3][1]
    # hsk4_hanzi, hsk4_unique = counts[4][0], counts[4][1]
    # hsk5_hanzi, hsk5_unique = counts[5][0], counts[5][1]
    # hsk6_hanzi, hsk6_unique = counts[6][0], counts[6][1]
    
    # Cumulative figures = HSK1 figures for HSK1
    cumulative_stats = [(counts[1][0], counts[1][1])]
    # Iterate through remaining levels to get iterative figures
    for i in range(2, 7):
        grade_hanzi = counts[i][0]
        grade_unique = counts[i][1]
        cumulative_hanzi = grade_hanzi + cumulative_stats[i-2][0]
        cumulative_unique = grade_unique + cumulative_stats[i-2][1]
        cumulative_stats.append((cumulative_hanzi, cumulative_unique))
    
    # Create columns for output DataFrame
    cols = [
        "HSK Grade", 
        "No. Hanzi (Unique)", 
        "% of Total", 
        "Cumulative No. Hanzi (Unique)", 
        "% of Total", 
        "No. Hanzi (Count)", 
        "% of Total", 
        "Cunulative No. Hanzi (Count)", 
        "% of Total"
    ]
    
    return cumulative_stats, hanzi_df
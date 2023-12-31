# -*- coding: utf-8 -*-
import numpy as np
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
    symbols = ["–", "—", "‘", "’", "“", "”", "…", "⊼", "⁆", "∕", "。"]
    # Unrecognised hanzi with no matching pinyin
    exceptions = ["㤙"]
    
    if ord(char) in range(8206, 8287):
        return False
    
    if char in symbols or char in exceptions:
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
        - hsk_simp, list, simplified characters in HSK1 to HSK7-9
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
        - hsk_simp, list, simplified characters in HSK1 to HSK7-9
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
        - df, Pandas DataFrame, all unique hanzi in HSK1 to HSK7-9
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
    num_total_unique_hanzi = len(set(hanzi_all))
    num_total_hanzi = len(hanzi_all)
    # Reserve key "0" for full figures
    grade_stats[0] = num_total_unique_hanzi, num_total_hanzi
    
    # Get counts for each grade HSK1 to HSK7-9 and store in grade_stats
    for i in range(1, 8):
        grade_unique = (df.loc[df["HSK Grade"] == i, "Count"] != 0).sum()
        grade_count  = df.loc[df["HSK Grade"] == i, "Count"].sum()
        grade_stats[i] = [grade_unique, grade_count]
        
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


def _cumulative_counts(raw_counts: list[list[int]], grades: int) -> list[list[int]]:
    """
    Computes grade-level and cumulative statistics for hanzi occurrences
    
    Args:
        - raw_counts, list, hanzi counts by grade
        - grades, int, number of HSK grades being checked against
    Returns:
        - cumulative_counts, list, cumulative hanzi counts by grade
    """
    # Cumulative figures = HSK1 figures for HSK1
    cumulative_counts = [[raw_counts[0][0], raw_counts[0][1]], [raw_counts[1][0], raw_counts[1][1]]]
    # Iterate through remaining levels to get iterative figures
    for i in range(2, grades + 1):
        grade_unique = raw_counts[i][0]
        cumul_unique = grade_unique + cumulative_counts[i-1][0]
        
        grade_hanzi = raw_counts[i][1]
        cumul_hanzi = grade_hanzi + cumulative_counts[i-1][1]
        
        cumulative_counts.append([cumul_unique, cumul_hanzi])
    
    return cumulative_counts


def _compute_stats(raw_counts: list[list[int]], cumulative_counts: list[list[int]], grades: int) -> list[list]:
    """
    Computes grade-level and cumulative statistics for hanzi occurrences
    
    Args:
        - raw_counts, list, hanzi counts by grade
        - cumulative_counts, list, cumulative hanzi counts by grade
        - grades, int, number of HSK grades being checked against
    Returns:
        - statistics, list, aggregate and cumulative grade-based hanzi counts
            with percentages
    """
    statistics = []
    # [grade, grade_unique, %, cum_unique, %, grade_count, %, cum_count, %]
    for i in range(1, grades + 1):
        
        grade = str(i)
        
        grade_unique = raw_counts[i][0]
        grade_unique_percent = np.int32((grade_unique / raw_counts[0][0]) * 100)
        
        cumulative_unique = cumulative_counts[i][0]
        cumulative_unique_percent = np.int32((cumulative_unique / cumulative_counts[0][0]) * 100)
        
        grade_count = raw_counts[i][1]
        grade_count_percent = np.int32((grade_count / raw_counts[0][1]) * 100)
        
        cumulative_count = cumulative_counts[i][1]
        cumulative_count_percent = np.int32((cumulative_count / cumulative_counts[0][1]) * 100)
        
        statistics.append([
            grade, 
            grade_unique, grade_unique_percent, 
            cumulative_unique, cumulative_unique_percent, 
            grade_count, grade_count_percent, 
            cumulative_count, cumulative_count_percent
        ])
    
    # Handle outliers from beyond HSK7-9
    grade = "10+"
    # Number of outliers is total minus HSK7-9 cumulative total
    grade_unique = raw_counts[0][0] - statistics[6][3]
    grade_unique_percent = np.int32((grade_unique / raw_counts[0][0]) * 100)
    cumulative_unique = raw_counts[0][0] 
    cumulative_unique_percent = np.int32((cumulative_unique / cumulative_counts[0][0]) * 100)
    # Number of outliers is total minus HSK7-9 cumulative total
    grade_count = raw_counts[0][1] - statistics[6][7]
    grade_count_percent = np.int32((grade_count / raw_counts[0][1]) * 100)
    cumulative_count = cumulative_counts[0][1]
    cumulative_count_percent = np.int32((cumulative_count / cumulative_counts[0][1]) * 100)
    
    statistics.append([
            grade, 
            grade_unique, grade_unique_percent, 
            cumulative_unique, cumulative_unique_percent, 
            grade_count, grade_count_percent, 
            cumulative_count, cumulative_count_percent
        ])
    
    return statistics


def get_stats(df: pd.DataFrame, hanzi_all: list, hanzi_sub: list|tuple[list], variant: str):
    """
    Passes params to _get_counts() for grade_counts and
        merged_df with counts applied
    Passes grade_counts to _cumulative_counts() for cumulative_counts
    Passes grade_counts and cumulative_counts to _compute_stats()
        for statistical breakdown
    Returns Pandas DataFrame of statistics and of original df with counts applied
    
    Args:
        - df, Pandas DataFrame, all unique characters in HSK1 to HSK6
        - hanzi_all, list, all characters (with duplicates) found in text being analysed
        - hanzi_sub, list | tuple, the character subset(s) to be analysed
            single list if variant defined as either simplified or traditional
            tuple of simplified and traditional lists if variant unknown
        - variant, str, the variant of the character set (Simplified|Traditional|Unknown)
    Returns:
        - stats_df, Pandas DataFrame, aggregate and cumulative grade-based character counts
        - hanzi_df, Pandas DataFrame, df with counts applied by _get_counts()
    """
    HSK_GRADES = 7
    # Get count breakdown of hanzi content
    grade_counts, hanzi_df = _get_counts(df, hanzi_all, hanzi_sub, variant)
    # Get cumulative counts ascending from HSK1 to HSK7-9
    cumul_counts = _cumulative_counts(grade_counts, HSK_GRADES)
    # Compute stats for grade counts and cumulative counts
    stats = _compute_stats(grade_counts, cumul_counts, HSK_GRADES)
    # Create columns for output DataFrame
    cols = [
        "HSK\nGrade", 
        "No.\nHanzi\n(Unique)", "% of\nTotal\nUnique", 
        "Cumul.\nUnique", "% of\nCumul.\nUnique", 
        "No.\nHanzi\n(Count)", "% of\nTotal", 
        "Cumul.\nCount", "% of\nCumul\nCount"
    ]
    # Create stats DataFrame
    stats_df = pd.DataFrame(stats, columns=cols)
    
    # Format HSK Grade column for export
    stats_df["HSK\nGrade"] = stats_df["HSK\nGrade"].astype(str)
    hanzi_df["HSK Grade"] = hanzi_df["HSK Grade"].astype(str)
    
    for i in range(1, 7):
        stats_df["HSK\nGrade"] = stats_df["HSK\nGrade"].replace(f"{i}", f"[{i}]")
        hanzi_df["HSK Grade"] = hanzi_df["HSK Grade"].replace(f"{i}", f"[{i}]")
    
    stats_df["HSK\nGrade"] = stats_df["HSK\nGrade"].replace("7", "[7-9]")
    hanzi_df["HSK Grade"] = hanzi_df["HSK Grade"].replace("7", "[7-9]")
    stats_df["HSK\nGrade"] = stats_df["HSK\nGrade"].replace("10+", "[10+]")
    hanzi_df["HSK Grade"] = hanzi_df["HSK Grade"].replace("10+", "[10+]")
    
    return stats_df, hanzi_df

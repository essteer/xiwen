# -*- coding: utf-8 -*-
import pandas as pd

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
    exceptions = ["—", "‘", "’", "“", "”", "…"]
    
    if char in exceptions:
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
    Separates hanzi into lists based on whether
    they are HSK simplified or traditional characters
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
    threshold = 0.8
    simp_set = set(hsk_simp) - set(neutral)
    trad_set = set(hsk_trad) - set(neutral)
    
    try:
        ratio = len(simp_set) / (len(simp_set) + len(trad_set))
        if ratio >= threshold:
            return "Simplified"
        elif ratio <= 1 - threshold:
            return "Traditional"
        else:
            return "Unknown"
        
    except ZeroDivisionError:
        return "Unknown"


def _counts(hanzi: list) -> dict:
    """
    Counts occurrences of each character in hanzi
    Args:
        - hanzi, list, characters to count
    Returns:
        - counts, dict, counts of each character
    """
    counts = {}
    for zi in hanzi:
            counts[zi] = counts.get(zi, 0) + 1
    return counts


def _granular_counts(df: pd.DataFrame, variant: str) -> list:
    """
    Breaks down counts according to HSK grades
    Args:
        - df, Pandas DataFrame, all unique characters in HSK1 to HSK6
            with counts column
        - variant, str, the variant of the character set (Simplified|Traditional|Unknown)
    Returns:
        - dict, counts for characters per HSK grade
    """
    # TODO: add code for count breakdowns
    pass


def get_counts(df: pd.DataFrame, hanzi: list|tuple[list], variant: str):
    """
    Passes hanzi to _counts to count occurrences of each Chinese character
    Passes updated df to _granular_counts for grade-by-grade breakdown
    
    Args:
        - df, Pandas DataFrame, all unique characters in HSK1 to HSK6
        - hanzi, list | tuple, the characters to be analysed
            list if variant defined as either simplified or traditional
            tuple of simplified and traditional lists if unknown
        - variant, str, the variant of the character set (Simplified|Traditional|Unknown)
    Returns:
        - dict, stats for aggregate and grade-based character counts
    """
    # hanzi = single list if variant defined (Simplified|Traditional)
    if isinstance(hanzi, list):
        # Count occurrences of each character in hanzi
        counts = _counts(hanzi)
        # Create DataFrame from counts dictionary
        counts_df = pd.DataFrame(list(counts.items()), columns=[variant, "Count"])
        # Merge on variant column
        merged_df = pd.merge(df, counts_df, on=variant, how="left")
    
    # hanzi = tuple of (Simplified, Traditional) characters if variant unknown
    else:        
        simp = hanzi[0]
        # Avoid double-counting characters common to both variants
        trad = [zi for zi in hanzi[1] if zi not in simp]
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
        
        # Sum counts for rows with different variants
        merged_df.loc[~identical_mask, "Count"] = (
            merged_df["Count_x"].fillna(0) + merged_df["Count_y"].fillna(0)
        )
        # Take either count for rows with identical variants
        merged_df.loc[identical_mask, "Count"] = merged_df["Count_x"].fillna(0)
        
        # Drop unnecessary columns
        merged_df.drop(columns=["Count_x", "Count_y"], inplace=True)
    
    # Fill NaN as 0 and convert counts to integers
    merged_df["Count"] = merged_df["Count"].fillna(0).astype(int)
    
    # TODO: pass merged_df to _granular_counts() for breakdowns
    
    return merged_df
    
    
##########################################################################
# Unit test for get_counts()
##########################################################################

# df_data = {"Simplified": ["爱", "八", "爸", "杯", "子"], "Traditional": ["愛", "八", "爸", "杯", "子"]}
# hanzi_simplified_data = ["爱", "八", "爸", "杯", "子"]
# hanzi_traditional_data = ["愛", "八", "爸", "杯", "子"]

# df = pd.DataFrame(df_data)
# result_df = get_counts(df, (hanzi_simplified_data, hanzi_traditional_data), "Undefined")
# print(result_df)
    
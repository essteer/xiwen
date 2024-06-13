import pandas as pd
from .config import HSK_GRADES


def unit_counts(hanzi: list) -> dict:
    """
    Counts occurrences of each character in list

    Parameters
    ----------
    hanzi : list
        characters to count

    Returns
    -------
    counts : dict
        counts of each character
    """
    counts = {}
    for zi in hanzi:
        counts[zi] = counts.get(zi, 0) + 1
    return counts


def granular_counts(df: pd.DataFrame, hanzi_all: list, variant: str) -> list:
    """
    Breaks down counts by HSK grades

    Parameters
    ----------
    df : pd.DataFrame
        all unique hanzi in HSK1 to HSK7-9 with counts column

    hanzi_all : list
        all hanzi (with duplicates) found in text being analysed

    variant : str
        variant of the character set (Simplified|Traditional|Unknown)

    Returns
    -------
    grade_stats : dict
        counts for hanzi per HSK grade
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
        grade_count = df.loc[df["HSK Grade"] == i, "Count"].sum()
        grade_stats[i] = [grade_unique, grade_count]

    return grade_stats


def get_counts(hanzi_all: list, hanzi_subset: list, variant: str, hsk_hanzi: list):
    """
    Gets count of occurrences of each Chinese character
    Gets grade-by-grade breakdown

    Parameters
    ----------
    hanzi_all : list
        all characters (with duplicates) found in text being analysed

    hanzi_subset : list
        character subset to be analysed (simplified or traditional)

    variant : str
        variant of the character set (Simplified|Traditional|Unknown)

    hsk_hanzi : list
        all characters in HSK

    Returns
    -------
    counts : dict
        aggregate and grade-based character counts

    merged_df : pd.DataFrame
        df with counts applied
    """
    # Count occurrences of each character in hanzi_subset
    counts = unit_counts(hanzi_subset)
    # Create DataFrame from counts dictionary
    counts_df = pd.DataFrame(list(counts.items()), columns=[variant, "Count"])
    # Merge on variant column
    merged_df = pd.merge(hsk_hanzi, counts_df, on=variant, how="left")

    # Fill NaN as 0 and convert counts to integers
    merged_df["Count"] = merged_df["Count"].fillna(0).astype(int)

    counts = granular_counts(merged_df, hanzi_all, variant)

    return counts, merged_df


def cumulative_counts(raw_counts: list[list[int]]) -> list[list[int]]:
    """
    Computes grade-level and cumulative statistics for hanzi occurrences

    Parameters
    ----------
    raw_counts : list
        hanzi counts by grade

    Returns
    -------
    cumulative_counts : list
        cumulative hanzi counts by grade
    """
    # Cumulative figures = HSK1 figures only for HSK1
    cumulative_counts = [
        [raw_counts[0][0], raw_counts[0][1]],
        [raw_counts[1][0], raw_counts[1][1]],
    ]
    # Iterate through remaining levels to get iterative figures
    for i in range(2, HSK_GRADES + 1):
        grade_unique = raw_counts[i][0]
        cumul_unique = grade_unique + cumulative_counts[i - 1][0]

        grade_hanzi = raw_counts[i][1]
        cumul_hanzi = grade_hanzi + cumulative_counts[i - 1][1]

        cumulative_counts.append([cumul_unique, cumul_hanzi])

    return cumulative_counts

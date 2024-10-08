import polars as pl
from .config import HSK_GRADES
from .hsk_hanzi import HSKHanzi


def unit_counts_per_hanzi(hanzi: list) -> dict:
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
    counts = dict()
    for zi in hanzi:
        counts[zi] = counts.get(zi, 0) + 1

    return counts


def get_counts_per_hanzi(hanzi_subset: list, variant: str) -> pl.DataFrame:
    """
    Gets count of occurrences of each Chinese character

    Parameters
    ----------
    hanzi_subset : list
        character subset to be analysed (simplified or traditional)

    variant : str
        variant of the character set (Simplified|Traditional|Unknown)

    Returns
    -------
    merged_df : pl.DataFrame
        DataFrame of hsk_hanzi with counts applied
    """
    hsk_hanzi = HSKHanzi().get_all_HSK_hanzi()
    counts = unit_counts_per_hanzi(hanzi_subset)

    if variant == "Unknown":
        variant = "Traditional"

    counts_df = pl.DataFrame(
        list(counts.items()), schema={variant: pl.String, "Count": pl.Int32}
    )
    merged_df = hsk_hanzi.join(counts_df, on=variant, coalesce=True, how="left")
    merged_df = merged_df.fill_null(0).with_columns(pl.col("Count").cast(pl.Int32))

    return merged_df


def get_counts_per_hanzi_per_hsk_grade(df: pl.DataFrame, hanzi_all: list) -> dict:
    """
    Breaks down counts by HSK grades

    Parameters
    ----------
    df : pl.DataFrame
        all unique hanzi in HSK1 to HSK7-9 with counts column

    hanzi_all : list
        all hanzi (with duplicates including non-HSK) found in text being analysed

    Returns
    -------
    grade_stats : dict
        counts for hanzi per HSK grade
    """
    grade_stats = dict()
    num_unique_hanzi = len(set(hanzi_all))
    num_total_hanzi = len(hanzi_all)
    grade_stats[0] = num_unique_hanzi, num_total_hanzi  # Reserve key "0" for totals

    for i in range(1, 8):
        grade_df = df.filter(pl.col("HSK Grade") == i)
        grade_unique = (grade_df["Count"] != 0).sum()
        grade_count = grade_df["Count"].sum()
        grade_stats[i] = [grade_unique, grade_count]

    return grade_stats


def get_cumulative_counts_per_hsk_grade(
    raw_counts: dict[int : list[int]],
) -> list[list[int]]:
    """
    Computes grade-level and cumulative statistics for hanzi occurrences

    Parameters
    ----------
    raw_counts : dict
        hanzi counts by grade

    Returns
    -------
    cumulative_counts : list
        cumulative hanzi counts by grade
    """
    cumulative_counts = [
        [raw_counts[0][0], raw_counts[0][1]],  # Total counts are at key 0
        [raw_counts[1][0], raw_counts[1][1]],  # HSK1 figures only for HSK1
    ]
    for i in range(2, HSK_GRADES + 1):
        grade_unique = raw_counts[i][0]
        cumul_unique = grade_unique + cumulative_counts[i - 1][0]

        grade_hanzi = raw_counts[i][1]
        cumul_hanzi = grade_hanzi + cumulative_counts[i - 1][1]

        cumulative_counts.append([cumul_unique, cumul_hanzi])

    return cumulative_counts

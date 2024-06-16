import polars as pl
from .config import HSK_GRADES
from .hanzi import get_HSKHanzi_instance


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


def granular_counts(df: pl.DataFrame, hanzi_all: list, variant: str) -> dict:
    """
    Breaks down counts by HSK grades

    Parameters
    ----------
    df : pl.DataFrame
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
        df = df.unique(subset=[variant], keep="first", maintain_order=True)

    else:
        """
        If the variant is unknown:
        - assume the broadest range of hanzi (Traditional)
        - drop duplicate Simplified hanzi only when the counts are identical
        """
        df = df.unique(
            subset=["Simplified", "Count"], keep="first", maintain_order=True
        )

    # Dict to store stats
    grade_stats = dict()

    # Get stats for full text including non-HSK characters (outliers)
    num_total_unique_hanzi = len(set(hanzi_all))
    num_total_hanzi = len(hanzi_all)
    # Reserve key "0" for full figures
    grade_stats[0] = num_total_unique_hanzi, num_total_hanzi

    for i in range(1, 8):
        grade_df = df.filter(pl.col("HSK Grade") == i)
        grade_unique = (grade_df["Count"] != 0).sum()
        grade_count = grade_df["Count"].sum()
        grade_stats[i] = [grade_unique, grade_count]

    return grade_stats


def get_counts(hanzi_subset: list, variant: str) -> pl.DataFrame:
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
        DataFrame of HSK_HANZI with counts applied
    """
    # Get DataFrame of full HSK character liss
    hsk_hanzi = get_HSKHanzi_instance().HSK_HANZI
    # Count occurrences of each character in hanzi_subset
    counts = unit_counts(hanzi_subset)

    # Merge on variant column
    if variant == "Unknown":
        variant = "Traditional"
    # Create DataFrame from counts dictionary
    counts_df = pl.DataFrame(
        list(counts.items()), schema={variant: pl.String, "Count": pl.Int32}
    )
    merged_df = hsk_hanzi.join(counts_df, on=variant, coalesce=True, how="left")
    # Fill null values and convert counts to integers
    merged_df = merged_df.fill_null(0).with_columns(pl.col("Count").cast(pl.Int32))

    return merged_df


def cumulative_counts(raw_counts: dict[int : list[int]]) -> list[list[int]]:
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
    # Cumulative figures =
    cumulative_counts = [
        # Total counts are at key 0
        [raw_counts[0][0], raw_counts[0][1]],
        # HSK1 figures only for HSK1
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

import polars as pl
from .config import HSK_GRADES, STATS_COLUMNS
from .count import cumulative_counts, get_counts, granular_counts


def identify_variant(hsk_simp: list, hsk_trad: list) -> str:
    """
    Identifies text as Simplified or Traditional based on character ratio

    Parameters
    ----------
    hsk_simp : list
        simplified characters in HSK1 to HSK7-9 found in content

    hsk_trad : list
        traditional equivalents to hsk_simp found in content

    Returns
    -------
    str
        text character variant
    """
    # Use epsilon to mitigate float rounding errors
    epsilon = 0.0000000001
    # Threshold beyond which to decide that text belongs to one variant
    threshold = 0.90
    simp_set = set(hsk_simp) - set(hsk_trad)
    trad_set = set(hsk_trad) - set(hsk_simp)

    if not simp_set and not trad_set:
        return "Unknown"

    ratio = len(simp_set) / (len(simp_set) + len(trad_set))
    if ratio >= threshold - epsilon:
        return "Simplified"
    elif ratio <= 1 - threshold + epsilon:
        return "Traditional"
    return "Unknown"


def compute_stats(
    raw_counts: list[list[int]], cumulative_counts: list[list[int]]
) -> list[list]:
    """
    Computes grade-level and cumulative statistics for hanzi occurrences

    Parameters
    ----------
    raw_counts : list
        hanzi counts by grade

    cumulative_counts : list
        cumulative hanzi counts by grade

    Returns
    -------
    statistics : pl.DataFrame
        aggregate and cumulative grade-based hanzi counts with percentages
    """
    grade_range = [i for i in range(1, HSK_GRADES + 1)]
    grades = grade_range + [10]

    statistics = pl.DataFrame(
        {
            "HSK\nGrade": [i for i in grades],
            "No. Hanzi\n(Unique)": [raw_counts[i][0] for i in grade_range]
            + [raw_counts[0][0] - cumulative_counts[7][0]],
            "% of\nTotal\nUnique": [
                round((raw_counts[i][0] / raw_counts[0][0]), 4) * 100
                for i in grade_range
            ]
            + [
                round(
                    (raw_counts[0][0] - cumulative_counts[7][0]) / raw_counts[0][0], 4
                )
                * 100
            ],
            "Cumul.\nUnique": [cumulative_counts[i][0] for i in grade_range]
            + [raw_counts[0][0]],
            "% of\nCumul.\nUnique": [
                round((cumulative_counts[i][0] / cumulative_counts[0][0]), 4) * 100
                for i in grade_range
            ]
            + [round((cumulative_counts[0][0]) / cumulative_counts[0][0], 4) * 100],
            "No. Hanzi\n(Count)": [raw_counts[i][1] for i in grade_range]
            + [raw_counts[0][1] - cumulative_counts[7][1]],
            "% of\nTotal": [
                round((raw_counts[i][1] / raw_counts[0][1]), 4) * 100
                for i in grade_range
            ]
            + [
                round(
                    (raw_counts[0][1] - cumulative_counts[7][1]) / raw_counts[0][1], 4
                )
                * 100
            ],
            "Cumul.\nCount": [cumulative_counts[i][1] for i in grade_range]
            + [cumulative_counts[0][1]],
            "% of\nCumul.\nCount": [
                round((cumulative_counts[i][1] / cumulative_counts[0][1]), 4) * 100
                for i in grade_range
            ]
            + [round((cumulative_counts[0][1]) / cumulative_counts[0][1], 4) * 100],
        },
        schema=STATS_COLUMNS,
    )

    return statistics


def analyse(
    hanzi_list: list, simp_list: list, trad_list: list
) -> tuple[str, pl.DataFrame]:
    """
    Gets character variant and statistical breakdowns
      - number of unique characters and number of total characters
        by grade, and cumulative figures for the entire content

    Parameters
    ----------
    hanzi_list : list
        all characters (with duplicates) found in target content

    simplified : list
        simplified HSK hanzi in hanzi_list

    traditional : list
        traditional HSK equivalents in hanzi_list

    Returns
    -------
    variant : str
        hanzi variant of the content

    stats_df : pl.DataFrame
        stats for the content

    hanzi_df : pl.DataFrame
        df of hanzi_list with counts added
    """
    # Query character variant
    variant = identify_variant(simp_list, trad_list)
    # Create mapping for analysis
    variants = {
        "Simplified": simp_list,
        "Traditional": trad_list,
        "Unknown": trad_list,
    }
    # Get counts of each hanzi
    hanzi_df = get_counts(variants[variant], variant)
    # Get counts of hanzi by grade
    grade_counts = granular_counts(hanzi_df, hanzi_list, variant)
    # Get cumulative counts ascending from HSK1 to HSK7-9
    cumul_counts = cumulative_counts(grade_counts)
    # Compute stats for grade counts and cumulative counts
    stats_df = compute_stats(grade_counts, cumul_counts)

    return variant, stats_df, hanzi_df

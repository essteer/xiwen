import numpy as np
import pandas as pd
import sys
from .config import HSK_GRADES, STATS_COLUMNS
from .counters import get_counts, cumulative_counts


def identify_variant(hsk_simp: list, hsk_trad: list) -> str:
    """
    Identifies text as Simplified or Traditional based on character ratio

    Parameters
    ----------
    hsk_simp : list
        simplified characters in HSK1 to HSK7-9

    hsk_trad : list
        traditional equivalents to hsk_simp

    Returns
    -------
    str
        text character variant
    """
    # Threshold beyond which to decide that text belongs to one variant
    epsilon = sys.float_info.epsilon
    threshold = 0.90
    simp_set = set(hsk_simp) - set(hsk_trad)
    trad_set = set(hsk_trad) - set(hsk_simp)

    if len(simp_set) + len(trad_set) == 0:
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
    statistics : list
        aggregate and cumulative grade-based hanzi counts with percentages
    """
    statistics = []
    # [grade, grade_unique, %, cum_unique, %, grade_count, %, cum_count, %]
    for i in range(1, HSK_GRADES + 1):
        grade = str(i)

        grade_unique = raw_counts[i][0]
        grade_unique_percent = np.int32((grade_unique / raw_counts[0][0]) * 100)

        cumulative_unique = cumulative_counts[i][0]
        cumulative_unique_percent = np.int32(
            (cumulative_unique / cumulative_counts[0][0]) * 100
        )

        grade_count = raw_counts[i][1]
        grade_count_percent = np.int32((grade_count / raw_counts[0][1]) * 100)

        cumulative_count = cumulative_counts[i][1]
        cumulative_count_percent = np.int32(
            (cumulative_count / cumulative_counts[0][1]) * 100
        )

        statistics.append(
            [
                grade,
                grade_unique,
                grade_unique_percent,
                cumulative_unique,
                cumulative_unique_percent,
                grade_count,
                grade_count_percent,
                cumulative_count,
                cumulative_count_percent,
            ]
        )
    # Handle outliers from beyond HSK7-9
    grade = "10+"
    # Number of outliers is total minus HSK7-9 cumulative total
    grade_unique = raw_counts[0][0] - statistics[6][3]
    grade_unique_percent = np.int32((grade_unique / raw_counts[0][0]) * 100)
    cumulative_unique = raw_counts[0][0]
    cumulative_unique_percent = np.int32(
        (cumulative_unique / cumulative_counts[0][0]) * 100
    )
    # Number of outliers is total minus HSK7-9 cumulative total
    grade_count = raw_counts[0][1] - statistics[6][7]
    grade_count_percent = np.int32((grade_count / raw_counts[0][1]) * 100)
    cumulative_count = cumulative_counts[0][1]
    cumulative_count_percent = np.int32(
        (cumulative_count / cumulative_counts[0][1]) * 100
    )

    statistics.append(
        [
            grade,
            grade_unique,
            grade_unique_percent,
            cumulative_unique,
            cumulative_unique_percent,
            grade_count,
            grade_count_percent,
            cumulative_count,
            cumulative_count_percent,
        ]
    )

    return statistics


def create_stats_dataframe(stats: list, hanzi_df: pd.DataFrame):
    """
    Creates new dataframe of statistics
    Updates hanzi dataframe with counts

    Parameters
    ----------
    statistics : list
        aggregate and cumulative grade-based hanzi counts with percentages

    Returns
    -------
    stats_df : pd.DataFrame
        aggregate and cumulative grade-based character counts

    hanzi_df : pd.DataFrame
        df with counts applied
    """
    # Create stats DataFrame
    stats_df = pd.DataFrame(stats, columns=STATS_COLUMNS)

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


def analyse(
    hanzi_list: list, simp_list: list, trad_list: list, hsk_hanzi: list
) -> tuple[str | pd.DataFrame]:
    """
    Gets character variant and statistical breakdowns
      - number of unique characters and number of total characters
        by grade, and cumulative figures for the entire content

    Parameters
    ----------
    hanzi_list : list
        all hanzi found in target content

    simplified : list
        simplified HSK hanzi in hanzi_list

    traditional : list
        traditional HSK equivalents in hanzi_list

    hsk_hanzi : list
        all characters in HSK

    Returns
    -------
    variant : str
        hanzi variant of the content

    stats_df : pd.DataFrame
        stats for the content

    hanzi_df : pd.DataFrame
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
    # Get count breakdown of hanzi content
    grade_counts, hanzi_df = get_counts(
        hanzi_list, variants[variant], variant, hsk_hanzi
    )
    # Get cumulative counts ascending from HSK1 to HSK7-9
    cumul_counts = cumulative_counts(grade_counts)
    # Compute stats for grade counts and cumulative counts
    stats = compute_stats(grade_counts, cumul_counts)
    # Get dataframes of stats and hanzi_list with counts added
    stats_df, hanzi_df = create_stats_dataframe(stats, hanzi_df)

    return variant, stats_df, hanzi_df

import polars as pl
from .config import HSK_GRADES, STATS_COLUMNS
from .count import (
    get_cumulative_counts_per_hsk_grade,
    get_counts_per_hanzi,
    get_counts_per_hanzi_per_hsk_grade,
)
from .transform import filter_dataframe_by_hanzi_variant


def identify_variant(simplified: list, traditional: list) -> str:
    """
    Identifies text as Simplified or Traditional based on character ratio

    Parameters
    ----------
    simplified : list
        simplified characters in HSK1 to HSK7-9 found in content

    traditional : list
        traditional equivalents to simplified found in content

    Returns
    -------
    _ : str
        text character variant
    """
    epsilon = 0.0000000001  # mitigate float rounding errors
    threshold = 0.90  # to decide which variant text belongs to
    simplified_set = set(simplified) - set(traditional)
    traditional_set = set(traditional) - set(simplified)

    if not simplified_set and not traditional_set:
        return "Unknown"

    ratio = len(simplified_set) / (len(simplified_set) + len(traditional_set))
    if ratio >= threshold - epsilon:
        return "Simplified"
    elif ratio <= 1 - threshold + epsilon:
        return "Traditional"
    return "Unknown"


def compute_stats(
    raw_counts: list[list[int]], get_cumulative_counts_per_hsk_grade: list[list[int]]
) -> list[list]:
    """
    Computes grade-level and cumulative statistics for hanzi occurrences

    Parameters
    ----------
    raw_counts : list
        hanzi counts by grade

    get_cumulative_counts_per_hsk_grade : list
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
            + [raw_counts[0][0] - get_cumulative_counts_per_hsk_grade[7][0]],
            "% of\nTotal\nUnique": [
                round((raw_counts[i][0] / raw_counts[0][0]), 4) * 100
                for i in grade_range
            ]
            + [
                round(
                    (raw_counts[0][0] - get_cumulative_counts_per_hsk_grade[7][0])
                    / raw_counts[0][0],
                    4,
                )
                * 100
            ],
            "Cumul.\nUnique": [
                get_cumulative_counts_per_hsk_grade[i][0] for i in grade_range
            ]
            + [raw_counts[0][0]],
            "% of\nCumul.\nUnique": [
                round(
                    (
                        get_cumulative_counts_per_hsk_grade[i][0]
                        / get_cumulative_counts_per_hsk_grade[0][0]
                    ),
                    4,
                )
                * 100
                for i in grade_range
            ]
            + [
                round(
                    (get_cumulative_counts_per_hsk_grade[0][0])
                    / get_cumulative_counts_per_hsk_grade[0][0],
                    4,
                )
                * 100
            ],
            "No. Hanzi\n(Count)": [raw_counts[i][1] for i in grade_range]
            + [raw_counts[0][1] - get_cumulative_counts_per_hsk_grade[7][1]],
            "% of\nTotal": [
                round((raw_counts[i][1] / raw_counts[0][1]), 4) * 100
                for i in grade_range
            ]
            + [
                round(
                    (raw_counts[0][1] - get_cumulative_counts_per_hsk_grade[7][1])
                    / raw_counts[0][1],
                    4,
                )
                * 100
            ],
            "Cumul.\nCount": [
                get_cumulative_counts_per_hsk_grade[i][1] for i in grade_range
            ]
            + [get_cumulative_counts_per_hsk_grade[0][1]],
            "% of\nCumul.\nCount": [
                round(
                    (
                        get_cumulative_counts_per_hsk_grade[i][1]
                        / get_cumulative_counts_per_hsk_grade[0][1]
                    ),
                    4,
                )
                * 100
                for i in grade_range
            ]
            + [
                round(
                    (get_cumulative_counts_per_hsk_grade[0][1])
                    / get_cumulative_counts_per_hsk_grade[0][1],
                    4,
                )
                * 100
            ],
        },
        schema=STATS_COLUMNS,
    )

    return statistics


def analyse_hanzi(
    hanzi_list: list, simplified: list, traditional: list
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
    hanzi_df : pl.DataFrame
        df of hanzi_list with counts added

    stats_df : pl.DataFrame
        stats for the content

    variant : str
        hanzi variant of the content
    """
    variant = identify_variant(simplified, traditional)
    variants = {
        "Simplified": simplified,
        "Traditional": traditional,
        "Unknown": traditional,
    }
    hanzi_df = get_counts_per_hanzi(variants[variant], variant)
    filtered_hanzi_df = filter_dataframe_by_hanzi_variant(hanzi_df, variant)
    grade_counts = get_counts_per_hanzi_per_hsk_grade(filtered_hanzi_df, hanzi_list)
    cumul_counts = get_cumulative_counts_per_hsk_grade(grade_counts)
    stats_df = compute_stats(grade_counts, cumul_counts)

    return hanzi_df, stats_df, variant

import os
import polars as pl
import sys
import unittest
from polars.testing import assert_frame_equal
from src.xiwen.utils.config import HSK_GRADES
from src.xiwen.utils.count import (
    get_counts_per_hanzi,
    get_counts_per_hanzi_per_hsk_grade,
    get_cumulative_counts_per_hsk_grade,
    unit_counts,
)
from src.xiwen.utils.extract import filter_hanzi_from_html
from src.xiwen.utils.hsk_hanzi import get_HSKHanzi_instance
from src.xiwen.utils.transform import filter_dataframe_by_hanzi_variant, partition_hanzi


TEST_ASSETS = os.path.abspath(os.path.join("tests", "assets"))

TEST_CASES = {
    # Simplified only
    "bjzd.txt": {
        "Simplified": {
            0: (1751, 18896),
            1: [281, 11145],
            2: [271, 3269],
            3: [259, 1809],
            4: [217, 981],
            5: [185, 472],
            6: [133, 325],
            7: [314, 646],
        },
        "Traditional": {
            0: (1751, 18896),
            1: [191, 8432],
            2: [179, 2263],
            3: [163, 1255],
            4: [139, 625],
            5: [113, 285],
            6: [88, 225],
            7: [196, 392],
        },
        "Unknown": {
            0: (1751, 18896),
            1: [191, 8432],
            2: [179, 2263],
            3: [163, 1255],
            4: [139, 625],
            5: [113, 285],
            6: [88, 225],
            7: [196, 392],
        },
    },
    # Traditional only
    "ttc.txt": {
        "Simplified": {
            0: (810, 5686),
            1: [96, 1765],
            2: [82, 1075],
            3: [75, 532],
            4: [51, 438],
            5: [34, 124],
            6: [40, 148],
            7: [106, 308],
        },
        "Traditional": {
            0: (810, 5686),
            1: [134, 1926],
            2: [118, 1357],
            3: [112, 688],
            4: [88, 712],
            5: [52, 189],
            6: [63, 221],
            7: [146, 373],
        },
        "Unknown": {
            0: (810, 5686),
            1: [134, 1926],
            2: [118, 1357],
            3: [111, 687],
            4: [88, 712],
            5: [52, 189],
            6: [63, 221],
            7: [146, 373],
        },
    },
    # Latin alphabet (no hanzi)
    "iliad.txt": {
        "Simplified": {
            0: (0, 0),
            1: [0, 0],
            2: [0, 0],
            3: [0, 0],
            4: [0, 0],
            5: [0, 0],
            6: [0, 0],
            7: [0, 0],
        },
        "Traditional": {
            0: (0, 0),
            1: [0, 0],
            2: [0, 0],
            3: [0, 0],
            4: [0, 0],
            5: [0, 0],
            6: [0, 0],
            7: [0, 0],
        },
        "Unknown": {
            0: (0, 0),
            1: [0, 0],
            2: [0, 0],
            3: [0, 0],
            4: [0, 0],
            5: [0, 0],
            6: [0, 0],
            7: [0, 0],
        },
    },
}


class TestUnitCounts(unittest.TestCase):
    def test_counts(self):
        """Test counts match across character variants"""
        hanzi = []
        test = dict()
        self.assertEqual(unit_counts(hanzi), test)
        hanzi = ["爱", "气", "爱", "气", "车", "爱", "气", "车", "愛", "氣", "車"]
        test = {"爱": 3, "气": 3, "车": 2, "愛": 1, "氣": 1, "車": 1}
        self.assertEqual(unit_counts(hanzi), test)


class TestCumulativeCounts(unittest.TestCase):
    @unittest.skipIf(
        sys.platform.startswith("win"), "Skip on Windows: test case decode issue"
    )
    def test_simplified_set(self):
        """Test counts match for simplified character set"""
        variant = "Simplified"
        for test_case in TEST_CASES.keys():
            with open(os.path.join(TEST_ASSETS, test_case), "r") as f:
                text = f.read()
            # Extract hanzi from text (with duplicates)
            hanzi_list = filter_hanzi_from_html(text)
            simp, _, _ = partition_hanzi(hanzi_list)
            # Get counts of each hanzi
            hanzi_df = get_counts_per_hanzi(simp, variant)
            # Filter on identified variant
            filtered_hanzi_df = filter_dataframe_by_hanzi_variant(hanzi_df, variant)
            # Get counts by grade (test case)
            counts = get_counts_per_hanzi_per_hsk_grade(filtered_hanzi_df, hanzi_list)

            cumulative_num_unique = 0
            cumulative_num_grade = 0
            for i in range(1, HSK_GRADES + 1):
                cumulative_num_unique += counts[i][0]
                cumulative_num_grade += counts[i][1]
                self.assertEqual(
                    get_cumulative_counts_per_hsk_grade(counts)[i][1],
                    cumulative_num_grade,
                )

                self.assertEqual(
                    get_cumulative_counts_per_hsk_grade(counts)[i][0],
                    cumulative_num_unique,
                )

    @unittest.skipIf(
        sys.platform.startswith("win"), "Skip on Windows: test case decode issue"
    )
    def test_traditional_set(self):
        """Test counts match for traditional character set"""
        variant = "Traditional"
        for test_case in TEST_CASES.keys():
            with open(os.path.join(TEST_ASSETS, test_case), "r") as f:
                text = f.read()
            # Extract hanzi from text (with duplicates)
            hanzi_list = filter_hanzi_from_html(text)
            simp, _, _ = partition_hanzi(hanzi_list)
            # Get counts of each hanzi
            hanzi_df = get_counts_per_hanzi(simp, variant)
            # Filter on identified variant
            filtered_hanzi_df = filter_dataframe_by_hanzi_variant(hanzi_df, variant)
            # Get counts by grade (test case)
            counts = get_counts_per_hanzi_per_hsk_grade(filtered_hanzi_df, hanzi_list)

            cumulative_num_unique = 0
            cumulative_num_grade = 0
            for i in range(1, HSK_GRADES + 1):
                cumulative_num_unique += counts[i][0]
                cumulative_num_grade += counts[i][1]
                self.assertEqual(
                    get_cumulative_counts_per_hsk_grade(counts)[i][1],
                    cumulative_num_grade,
                )

                self.assertEqual(
                    get_cumulative_counts_per_hsk_grade(counts)[i][0],
                    cumulative_num_unique,
                )


class TestGetCounts(unittest.TestCase):
    @unittest.skipIf(
        sys.platform.startswith("win"), "Skip on Windows: test case decode issue"
    )
    def test_simplified_set(self):
        """Test counts correct for simplified characters"""
        variant = "Simplified"
        # Get DataFrame of full HSK character liss
        hsk_hanzi = get_HSKHanzi_instance().HSK_HANZI
        for test_case in TEST_CASES.keys():
            with open(os.path.join(TEST_ASSETS, test_case), "r") as f:
                text = f.read()
            # Extract hanzi from text (with duplicates)
            hanzi_list = filter_hanzi_from_html(text)
            simp, _, _ = partition_hanzi(hanzi_list)
            counts = unit_counts(simp)
            # Create DataFrame from counts dictionary
            counts_df = pl.DataFrame(
                list(counts.items()), schema={variant: pl.String, "Count": pl.Int32}
            )
            merged_df = hsk_hanzi.join(counts_df, on=variant, coalesce=True, how="left")
            # Fill null values and convert counts to integers
            merged_df = merged_df.fill_null(0).with_columns(
                pl.col("Count").cast(pl.Int32)
            )
            self.assertIsNone(
                assert_frame_equal(get_counts_per_hanzi(simp, variant), merged_df)
            )

    @unittest.skipIf(
        sys.platform.startswith("win"), "Skip on Windows: test case decode issue"
    )
    def test_traditional_set(self):
        """Test counts correct for traditional characters"""
        variant = "Traditional"
        # Get DataFrame of full HSK character liss
        hsk_hanzi = get_HSKHanzi_instance().HSK_HANZI
        for test_case in TEST_CASES.keys():
            with open(os.path.join(TEST_ASSETS, test_case), "r") as f:
                text = f.read()
            # Extract hanzi from text (with duplicates)
            hanzi_list = filter_hanzi_from_html(text)
            simp, _, _ = partition_hanzi(hanzi_list)
            counts = unit_counts(simp)
            # Create DataFrame from counts dictionary
            counts_df = pl.DataFrame(
                list(counts.items()), schema={variant: pl.String, "Count": pl.Int32}
            )
            merged_df = hsk_hanzi.join(counts_df, on=variant, coalesce=True, how="left")
            # Fill null values and convert counts to integers
            merged_df = merged_df.fill_null(0).with_columns(
                pl.col("Count").cast(pl.Int32)
            )
            self.assertIsNone(
                assert_frame_equal(get_counts_per_hanzi(simp, variant), merged_df)
            )


class TestGranularCounts(unittest.TestCase):
    @unittest.skipIf(
        sys.platform.startswith("win"), "Skip on Windows: test case decode issue"
    )
    def test_simplified_set(self):
        """Test correct breakdown for simplified character set"""
        variant = "Simplified"
        for test_case in TEST_CASES.keys():
            with open(os.path.join(TEST_ASSETS, test_case), "r") as f:
                text = f.read()
            # Extract hanzi from text (with duplicates)
            hanzi_list = filter_hanzi_from_html(text)
            simp, _, _ = partition_hanzi(hanzi_list)
            # Get counts of each hanzi
            hanzi_df = get_counts_per_hanzi(simp, variant)
            # Filter on identified variant
            filtered_hanzi_df = filter_dataframe_by_hanzi_variant(hanzi_df, variant)
            # Get counts by grade (test case)
            counts = get_counts_per_hanzi_per_hsk_grade(filtered_hanzi_df, hanzi_list)
            self.assertEqual(TEST_CASES[test_case][variant], counts)

    @unittest.skipIf(
        sys.platform.startswith("win"), "Skip on Windows: test case decode issue"
    )
    def test_traditional_set(self):
        """Test correct breakdown for traditional character set"""
        variant = "Traditional"
        for test_case in TEST_CASES.keys():
            with open(os.path.join(TEST_ASSETS, test_case), "r") as f:
                text = f.read()
            # Extract hanzi from text (with duplicates)
            hanzi_list = filter_hanzi_from_html(text)
            _, trad, _ = partition_hanzi(hanzi_list)
            # Get counts of each hanzi
            hanzi_df = get_counts_per_hanzi(trad, variant)
            # Filter on identified variant
            filtered_hanzi_df = filter_dataframe_by_hanzi_variant(hanzi_df, variant)
            # Get counts by grade (test case)
            counts = get_counts_per_hanzi_per_hsk_grade(filtered_hanzi_df, hanzi_list)
            self.assertEqual(TEST_CASES[test_case][variant], counts)

    @unittest.skipIf(
        sys.platform.startswith("win"), "Skip on Windows: test case decode issue"
    )
    def test_unknown_set(self):
        """Test correct breakdown for unknown character set"""
        variant = "Unknown"
        for test_case in TEST_CASES.keys():
            with open(os.path.join(TEST_ASSETS, test_case), "r") as f:
                text = f.read()
            # Extract hanzi from text (with duplicates)
            hanzi_list = filter_hanzi_from_html(text)
            _, trad, _ = partition_hanzi(hanzi_list)
            # Get counts of each hanzi
            hanzi_df = get_counts_per_hanzi(trad, variant)
            # Filter on identified variant
            filtered_hanzi_df = filter_dataframe_by_hanzi_variant(hanzi_df, variant)
            # Get counts by grade (test case)
            counts = get_counts_per_hanzi_per_hsk_grade(filtered_hanzi_df, hanzi_list)
            # Figures should match traditional counts
            self.assertEqual(TEST_CASES[test_case][variant], counts)


if __name__ == "__main__":
    unittest.main()

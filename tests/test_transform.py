import os
import unittest
from src.xiwen.utils.config import ENCODING
from src.xiwen.utils.extract import filter_hanzi_from_html
from src.xiwen.utils.transform import partition_hanzi


TEST_ASSETS = os.path.abspath(os.path.join("tests", "assets"))

TEST_CASES = {
    # Simplified only
    "bjzd.txt": ["Simplified", 18896, 1751, 18647, 13477, 249],
    # Traditional only
    "ttc.txt": ["Traditional", 5686, 810, 4390, 5466, 206],
    # Latin alphabet (no hanzi)
    "iliad.txt": ["Unknown", 0, 0, 0, 0, 0],
    # Unknown - 50:50 simplified : traditional
    "ping50.txt": ["Unknown", 360, 2, 180, 180, 0],
    # Unknown - 50:50 simplified : traditional
    "mix50.txt": ["Unknown", 40, 40, 20, 20, 0],
    # Simplified - 90:10 simplified : traditional
    "mix90.txt": ["Simplified", 20, 20, 18, 1, 1],
    # Traditional - 10:90 simplified : traditional
    "mix10.txt": ["Traditional", 20, 20, 1, 18, 1],
}


class TestPartitionHanzi(unittest.TestCase):
    def test_partition(self):
        """Test characters are separated appropriately"""
        simp = ["爱", "气", "车", "电", "话", "点", "脑", "视", "东", "不", "了"]
        trad = ["愛", "氣", "車", "電", "話", "點", "腦", "視", "東", "不", "了"]
        test = [
            "爱",
            "气",
            "车",
            "电",
            "话",
            "点",
            "脑",
            "视",
            "东",
            "愛",
            "氣",
            "車",
            "電",
            "話",
            "點",
            "腦",
            "視",
            "東",
            "不",
            "了",
        ]
        self.assertEqual(partition_hanzi(test), (simp, trad, []))
        self.assertEqual(partition_hanzi(simp), (simp, ["不", "了"], []))
        self.assertEqual(partition_hanzi(trad), (["不", "了"], trad, []))
        test = [
            "爱",
            "气",
            "车",
            "电",
            "话",
            "点",
            "脑",
            "视",
            "东",
            "愛",
            "氣",
            "車",
            "電",
            "話",
            "點",
            "腦",
            "視",
            "東",
            "不",
            "了",
            "朕",
        ]
        self.assertEqual(partition_hanzi(test), (simp, trad, ["朕"]))

    def test_known_figures(self):
        """Test figures match for known quantities"""
        for test_case in TEST_CASES.keys():
            with open(
                os.path.join(TEST_ASSETS, test_case), "r", encoding=ENCODING
            ) as f:
                text = f.read()
            # Extract hanzi from text (with duplicates)
            hanzi = filter_hanzi_from_html(text)
            # Divide into groups (with duplicates)
            simp, trad, outliers = partition_hanzi(hanzi)
            self.assertEqual(len(simp), TEST_CASES[test_case][3])
            self.assertEqual(len(trad), TEST_CASES[test_case][4])
            self.assertEqual(len(outliers), TEST_CASES[test_case][5])


if __name__ == "__main__":
    unittest.main()

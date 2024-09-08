import os
import polars as pl
import unittest
from polars.testing import assert_frame_equal
from src.xiwen.utils.config import ASSETS_DIR, HSK30_HANZI_SCHEMA
from src.xiwen.utils.hsk_hanzi import HSKHanzi


class TestHSKHanzi(unittest.TestCase):
    def test_HSKHanzi_attributes_exist(self):
        """Test HSKHanzi has expected attributes"""
        A = HSKHanzi()
        self.assertTrue(hasattr(A, "HSK_hanzi"))
        self.assertTrue(hasattr(A, "HSK_hanzi_sublist"))

    def test_HSKHanzi_attributes_correct(self):
        """Test class attributes match expected dataframes and lists"""
        hsk_hanzi = pl.read_parquet(
            os.path.join(ASSETS_DIR, "hsk30_hanzi.parquet"),
            hive_schema=HSK30_HANZI_SCHEMA,
        )
        A = HSKHanzi().HSK_hanzi
        self.assertIsNone(assert_frame_equal(hsk_hanzi, A))

    def test_HSKHanzi_creates_Simplified_list(self):
        """Test Simplified list created when Simplified passed in"""
        hsk_hanzi = pl.read_parquet(
            os.path.join(ASSETS_DIR, "hsk30_hanzi.parquet"),
            hive_schema=HSK30_HANZI_SCHEMA,
        )
        hsk_simplified_list = hsk_hanzi.select("Simplified").to_series().to_list()
        A = HSKHanzi("Simplified")
        self.assertEqual(hsk_simplified_list, A.HSK_hanzi_sublist)

    def test_HSKHanzi_creates_Traditional_list(self):
        """Test Traditional list created when Traditional passed in"""
        hsk_hanzi = pl.read_parquet(
            os.path.join(ASSETS_DIR, "hsk30_hanzi.parquet"),
            hive_schema=HSK30_HANZI_SCHEMA,
        )
        hsk_traditional_list = hsk_hanzi.select("Traditional").to_series().to_list()
        A = HSKHanzi("Traditional")
        self.assertEqual(hsk_traditional_list, A.HSK_hanzi_sublist)

    def test_get_all_HSK_hanzi(self):
        """Test method return object matches HSK_hanzi attribute"""
        hsk_hanzi = HSKHanzi()
        self.assertIsNone(
            assert_frame_equal(hsk_hanzi.HSK_hanzi, hsk_hanzi.get_all_HSK_hanzi())
        )

    def test_get_HSK_hanzi_sublist(self):
        """Test method return object matches HSK_hanzi_sublist attribute"""
        hsk_hanzi = HSKHanzi("Simplified")
        self.assertEqual(hsk_hanzi.get_HSK_hanzi_sublist(), hsk_hanzi.HSK_hanzi_sublist)
        hsk_hanzi = HSKHanzi("Traditional")
        self.assertEqual(hsk_hanzi.get_HSK_hanzi_sublist(), hsk_hanzi.HSK_hanzi_sublist)


if __name__ == "__main__":
    unittest.main()

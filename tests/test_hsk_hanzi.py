import os
import polars as pl
import unittest
from polars.testing import assert_frame_equal
from src.xiwen.utils.config import ASSETS_DIR, HSK30_HANZI_SCHEMA
from src.xiwen.utils.hsk_hanzi import get_HSKHanzi_instance, HSKHanzi


class TestHSKHanzi(unittest.TestCase):
    def test_references_to_HSKHanzi(self):
        """Test separate references are equal"""
        A = HSKHanzi()
        B = HSKHanzi()
        self.assertEqual(A, B)

    def test_one_HSKHanzi_exists(self):
        """Test just one instance exists despite multiple calls"""
        A = HSKHanzi()
        B = HSKHanzi()
        self.assertIs(A, B._instance)

    def test_HSKHanzi_attributes_exist(self):
        """Test HSKHanzi has expected attributes"""
        A = HSKHanzi()
        self.assertTrue(hasattr(A, "HSK_HANZI"))
        self.assertTrue(hasattr(A, "HSK_SIMP"))
        self.assertTrue(hasattr(A, "HSK_TRAD"))

    def test_HSKHanzi_attributes_correct(self):
        """Test class attributes match expected dataframes and lists"""
        HSK_HANZI = pl.read_parquet(
            os.path.join(ASSETS_DIR, "hsk30_hanzi.parquet"),
            hive_schema=HSK30_HANZI_SCHEMA,
        )
        A = HSKHanzi().HSK_HANZI
        self.assertIsNone(assert_frame_equal(HSK_HANZI, A))
        HSK_SIMP = HSK_HANZI.select("Simplified").to_series().to_list()
        B = HSKHanzi().HSK_SIMP
        self.assertEqual(HSK_SIMP, B)
        HSK_TRAD = HSK_HANZI.select("Traditional").to_series().to_list()
        C = HSKHanzi().HSK_TRAD
        self.assertEqual(HSK_TRAD, C)


class TestGetHSKHanziInstance(unittest.TestCase):
    def test_instance_returned(self):
        """Test function returns an HSKHanzi instance"""
        A = get_HSKHanzi_instance()
        self.assertTrue(isinstance(A, HSKHanzi))

    def test_returns_same_instance(self):
        """Test multiple calls return same HSKHanzi instance"""
        A = get_HSKHanzi_instance()
        B = get_HSKHanzi_instance()
        self.assertIs(A, B._instance)


if __name__ == "__main__":
    unittest.main()

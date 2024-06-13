import os
import unittest
from src.xiwen.utils.counters import unit_counts


TEST_ASSETS = os.path.abspath(os.path.join("tests", "assets"))
# Combine script directory with relative path to the file


class TestUnitCounts(unittest.TestCase):
    def test_counts(self):
        """Test counts match across character variants"""
        hanzi = ["爱", "气", "爱", "气", "车", "爱", "气", "车", "愛", "氣", "車"]
        test = {"爱": 3, "气": 3, "车": 2, "愛": 1, "氣": 1, "車": 1}
        self.assertEqual(unit_counts(hanzi), test)


# class TestGetCounts(unittest.TestCase):
#     def test_get_counts(self):
#         """Test counts DataFrame"""
#         all = ["爱", "八", "爸", "杯", "子", "愛", "八", "爸", "杯", "子"]
#         simp = ["爱", "八", "爸", "杯", "子"]
#         trad = ["愛", "八", "爸", "杯", "子"]
#         df_data = {
#             "Simplified": ["爱", "八", "爸", "杯", "子"],
#             "Traditional": ["愛", "八", "爸", "杯", "子"],
#         }
#         df = pd.DataFrame(df_data)
#         results = _get_counts(df, all, (simp, trad), "Unknown")
#         print(results)

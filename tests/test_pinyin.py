import unittest
from src.xiwen.utils.pinyin import get_pinyin

PINYIN_DICT = {
    "你": "nǐ",
    "好": "hǎo",
    "吗": "ma",
    "不": "bù",
    "茶": "chá",
    "出": "chū",
    "租": "zū",
    "車": "chē",
}

SAMPLES = ["茶", "出", "租", "車", "你", "好", "吗", "不"]


class TestGetPinyin(unittest.TestCase):
    def test_get_pinyin(self):
        """Test pinyin matches"""
        pinyin = get_pinyin(SAMPLES, PINYIN_DICT)
        for i in range(len(pinyin)):
            self.assertEqual(pinyin[i], PINYIN_DICT[SAMPLES[i]])


class TestMapPinyin(unittest.TestCase):
    def test_map_pinyin(self):
        pass


class TestSpecialCases(unittest.TestCase):
    def test_special_cases(self):
        pass


if __name__ == "__main__":
    unittest.main()

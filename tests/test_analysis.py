import os
import pandas as pd
import unittest
from src.xiwen.utils.analysis import _counts, identify
from src.xiwen.utils.config import ENCODING
from src.xiwen.utils.extract import filter_text
from src.xiwen.utils.transform import partition_hanzi


TEST_ASSETS = os.path.abspath(os.path.join("tests", "assets"))
# Combine script directory with relative path to the file
filepath = os.path.join("src", "xiwen", "assets", "hsk30_hanzi.csv")
# Load HSK Hanzi database (unigrams only)
HSK_HANZI = pd.read_csv(filepath)
HSK_SIMP = list(HSK_HANZI["Simplified"])
HSK_TRAD = list(HSK_HANZI["Traditional"])

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


class TestCounts(unittest.TestCase):
    def test_counts(self):
        """Test counts match across character variants"""
        hanzi = ["爱", "气", "爱", "气", "车", "爱", "气", "车", "愛", "氣", "車"]
        test = {"爱": 3, "气": 3, "车": 2, "愛": 1, "氣": 1, "車": 1}
        self.assertEqual(_counts(hanzi), test)


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


class TestIdentify(unittest.TestCase):
    def test_on_threshold(self):
        """Test variants on 90% threshold"""
        # 90% simp, 5% trad, 5% neutral
        simp90neut05 = [
            "爱",
            "气",
            "车",
            "电",
            "话",
            "点",
            "脑",
            "视",
            "东",
            "读",
            "对",
            "儿",
            "饭",
            "飞",
            "机",
            "钟",
            "兴",
            "个",
            "燚",
        ]
        trad05neut05 = ["漢", "燚"]
        self.assertEqual(identify(simp90neut05, trad05neut05), "Simplified")
        # 90% trad, 5% simp, 5% neutral
        simp05neut05 = ["汉", "燚"]
        trad90neut05 = [
            "愛",
            "氣",
            "車",
            "電",
            "話",
            "點",
            "腦",
            "視",
            "東",
            "讀",
            "對",
            "兒",
            "飯",
            "飛",
            "機",
            "鐘",
            "興",
            "個",
            "燚",
        ]
        self.assertEqual(identify(simp05neut05, trad90neut05), "Traditional")
        # 90% simp, 10% trad
        simp90 = ["爱", "气", "车", "电", "话", "点", "脑", "视", "东"]
        trad10 = ["漢"]
        self.assertEqual(identify(simp90, trad10), "Simplified")
        # 90% trad, 10% simp
        simp10 = ["汉"]
        trad90 = ["愛", "氣", "車", "電", "話", "點", "腦", "視", "東"]
        self.assertEqual(identify(simp10, trad90), "Traditional")

    def test_below_threshold(self):
        """Test variants under 90% threshold"""
        # 11% simp, 89% trad
        simp11 = ["爱", "气", "车", "电", "话", "点", "脑", "视", "东", "读", "对"]
        trad89 = [
            "闆",
            "闢",
            "錶",
            "彆",
            "蔔",
            "佈",
            "纔",
            "綵",
            "蟲",
            "醜",
            "齣",
            "邨",
            "噹",
            "黨",
            "澱",
            "弔",
            "鼕",
            "髮",
            "範",
            "豐",
            "穀",
            "僱",
            "颳",
            "廣",
            "鬨",
            "後",
            "穫",
            "幾",
            "機",
            "饑",
            "姦",
            "薑",
            "藉",
            "捲",
            "剋",
            "睏",
            "誇",
            "囉",
            "纍",
            "釐",
            "灕",
            "樑",
            "瞭",
            "黴",
            "瀰",
            "衊",
            "麼",
            "麼",
            "蘋",
            "僕",
            "舖",
            "樸",
            "籤",
            "捨",
            "瀋",
            "勝",
            "術",
            "鬆",
            "祂",
            "歎",
            "罈",
            "妳",
            "體",
            "衕",
            "塗",
            "糰",
            "餵",
            "爲",
            "縴",
            "鹹",
            "絃",
            "繡",
            "鬚",
            "燻",
            "醃",
            "葉",
            "傭",
            "湧",
            "遊",
            "於",
            "餘",
            "籲",
            "鬱",
            "慾",
            "禦",
            "願",
            "嶽",
            "雲",
            "讚",
        ]
        self.assertEqual(identify(simp11, trad89), "Unknown")
        # 89% simp, 11% trad
        simp89 = [
            "当",
            "发",
            "获",
            "饥",
            "罗",
            "弥",
            "铺",
            "签",
            "叹",
            "坛",
            "团",
            "为",
            "纤",
            "绣",
            "须",
            "赞",
            "脏",
            "证",
            "钟",
            "涩",
            "卤",
            "恶",
            "线",
            "荡",
            "仑",
            "苏",
            "汇",
            "历",
            "尽",
            "复",
            "炉",
            "锐",
            "挣",
            "壶",
            "哑",
            "纷",
            "搅",
            "忆",
            "类",
            "绳",
            "谚",
            "凭",
            "榄",
            "烃",
            "剂",
            "睁",
            "谓",
            "轧",
            "旧",
            "滩",
            "犹",
            "卢",
            "选",
            "纠",
            "储",
            "蝉",
            "届",
            "腊",
            "双",
            "见",
            "键",
            "遥",
            "螨",
            "蛴",
            "质",
            "阎",
            "宾",
            "够",
            "饶",
            "烂",
            "乌",
            "剥",
            "评",
            "湾",
            "剑",
            "涨",
            "绩",
            "风",
            "渔",
            "项",
            "铝",
            "献",
            "厅",
            "滨",
            "蝼",
            "饲",
            "恋",
            "尘",
            "马",
        ]
        trad11 = ["愛", "氣", "車", "電", "話", "點", "腦", "視", "東", "讀", "對"]
        self.assertEqual(identify(simp89, trad11), "Unknown")

    def test_balanced(self):
        """Test balanced and empty text"""
        # 0% trad, 0% simp
        simp00 = []
        trad00 = []
        self.assertEqual(identify(simp00, trad00), "Unknown")
        # 50% trad,50% simp
        simp50 = [
            "愛",
            "气",
            "车",
            "电",
            "话",
            "点",
            "脑",
            "视",
            "东",
            "读",
            "对",
            "儿",
            "饭",
            "飞",
            "机",
            "钟",
            "兴",
            "个",
            "汉",
            "号",
        ]
        trad50 = [
            "爱",
            "氣",
            "車",
            "電",
            "話",
            "點",
            "腦",
            "視",
            "東",
            "讀",
            "對",
            "兒",
            "飯",
            "飛",
            "機",
            "鐘",
            "興",
            "個",
            "漢",
            "號",
        ]
        self.assertEqual(identify(simp50, trad50), "Unknown")

    def test_known_figures(self):
        """Test figures match for known quantities"""
        for test_case in TEST_CASES.keys():
            with open(
                os.path.join(TEST_ASSETS, test_case), "r", encoding=ENCODING
            ) as f:
                text = f.read()
            # Extract hanzi from text (with duplicates)
            hanzi = filter_text(text)
            # Test total character count
            self.assertEqual(len(hanzi), TEST_CASES[test_case][1])
            # Test unique character count
            self.assertEqual(len(set(hanzi)), TEST_CASES[test_case][2])
            # Divide into groups (with duplicates)
            simp, trad, outliers = partition_hanzi(hanzi)
            # Check identified character variant
            self.assertEqual(identify(simp, trad), TEST_CASES[test_case][0])

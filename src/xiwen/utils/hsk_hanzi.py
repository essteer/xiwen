import os
import polars as pl
from .config import ASSETS_DIR, HSK30_HANZI_SCHEMA


class HSKHanzi:
    """
    Loads and retains HSK character lists
    Singleton pattern -> only one instance exists

    Attributes
    ----------
    HSK_HANZI : pl.DataFrame
        DataFrame of all characters in HSK

    HSK_SIMP : list
        all simplified characters in HSK

    HSK_TRAD : list
        traditional character equivalents to HSK_SIMP
    """

    # Stores the sole instance after initialisation
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HSKHanzi, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.HSK_HANZI = pl.read_parquet(
            os.path.join(ASSETS_DIR, "hsk30_hanzi.parquet"),
            hive_schema=HSK30_HANZI_SCHEMA,
        )
        self.HSK_SIMP = self.HSK_HANZI.select("Simplified").to_series().to_list()
        self.HSK_TRAD = self.HSK_HANZI.select("Traditional").to_series().to_list()


def get_HSKHanzi_instance():
    """
    Gets and returns the HSKHanzi class
    """
    return HSKHanzi()

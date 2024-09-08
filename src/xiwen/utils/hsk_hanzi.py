import os
import polars as pl
from .config import ASSETS_DIR, HSK30_HANZI_SCHEMA


class HSKHanzi:
    """
    Loads and retains HSK character lists

    Attributes
    ----------
    HSK_hanzi : pl.DataFrame
        DataFrame of all characters in HSK

    HSK_hanzi_sublist : list
        simplified HSK characters or their traditional equivalents
        depending on the variant passed at initialisation
    """

    def __init__(self, variant=None):
        self.HSK_hanzi = pl.read_parquet(
            os.path.join(ASSETS_DIR, "hsk30_hanzi.parquet"),
            hive_schema=HSK30_HANZI_SCHEMA,
        )
        self.HSK_hanzi_sublist = self.HSK_hanzi.select(variant).to_series().to_list()

    def get_all_HSK_hanzi(self):
        return self.HSK_hanzi

    def get_HSK_hanzi_sublist(self):
        return self.HSK_hanzi_sublist

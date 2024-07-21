import textwrap


class TerminalDisplay:
    """
    Displays instructions for terminal programme
    Singleton pattern -> only one instance exists
    """

    # Stores the sole instance after initialisation
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TerminalDisplay, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.WELCOME_MESSAGE = textwrap.dedent("""
        Welcome to Xiwen 析文
        Xiwen scans text for traditional 繁體 and simplified 简体
        Chinese characters (hanzi) to compare against HSK grades 1 to 9.
        Load a file or choose a URL, and Xiwen will output a grade-by-grade
        breakdown of the hanzi in the text.
        Export hanzi for further use — including hanzi not in the HSK.
        """)
        self.MAIN_MENU_OPTIONS = "Enter URL (q: quit, blank: demo): "
        self.DEMO_MESSAGE = textwrap.dedent("""
        -> '10' under 'HSK Grade' refers to hanzi beyond the HSK7-9 band.
        -> 'Unique' cols capture no. unique hanzi found per grade.
        -> 'Count' cols capture total no. hanzi found per grade.
            '今天天氣很好' = 5 unique hanzi, 6 total hanzi.
        -> '% of Total' gives the % relative to all hanzi found.
        -> 'Cumul' cols give the cumulative totals per grade
           'Cumul. Unique' col, HSK3 row gives the sum of unique hanzi found for HSK1, HSK2 and HSK3.
        """)
        self.EXPORT_OPTIONS = textwrap.dedent("""
        CSV export options
        -> 'a' = all detected HSK hanzi (excludes outliers)
        -> 'c' = custom HSK hanzi selection
        -> 'f' = full HSK hanzi list
        -> 'o' = outliers (non-HSK hanzi)
        -> 's' = stats
        -> 'x' = exit to main screen
        """)
        self.EXPORT_OPTIONS_FOR_CUSTOM_GRADES = textwrap.dedent("""
        Custom export:
        Enter the HSK grade(s) to export in any order
        -> e.g. to export HSK2 and HSK5 enter '25' or '52'
        """)
        self.UNKNOWN_CHARACTER_VARIANT = (
            "Unknown character set - stats for reference only"
        )

    def get_welcome_message(self):
        return self.WELCOME_MESSAGE

    def get_main_menu_options(self):
        return self.MAIN_MENU_OPTIONS

    def get_demo_message(self):
        return self.DEMO_MESSAGE

    def get_export_options(self):
        return self.EXPORT_OPTIONS

    def get_export_options_for_custom_grades(self):
        return self.EXPORT_OPTIONS_FOR_CUSTOM_GRADES

    def get_unknown_character_variant_message(self):
        return self.UNKNOWN_CHARACTER_VARIANT


def get_TerminalDisplay_instance():
    """
    Gets and returns the TerminalDisplay class
    """
    return TerminalDisplay()

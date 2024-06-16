import polars as pl
import random
from .app import coordinator
from .utils.config import DEMO_MESSAGE, DEMO1, DEMO2, MAIN_MENU_OPTIONS, WELCOME_MESSAGE
from .utils.export import export_hanzi


def xw():
    """
    Main menu loop for CLI program
    Prompts user for URL to scan
    """
    print(WELCOME_MESSAGE)
    while True:
        # Main menu - get URL from user
        target = input(MAIN_MENU_OPTIONS)

        if target.upper() == "Q":  # Quit
            break

        if target == "":  # Demo simplified or traditional characters
            target = random.choice([DEMO1, DEMO2])
            print(DEMO_MESSAGE)  # Explainer

        if target:
            # Run program
            hanzi_df, stats_df, hanzi_list, outl, variant = coordinator(target, True)

            with pl.Config(
                tbl_formatting="ASCII_MARKDOWN",
                tbl_hide_column_data_types=True,
                tbl_hide_dataframe_shape=True,
                set_tbl_cols=9,
                set_tbl_cell_numeric_alignment="RIGHT",
            ):
                print(stats_df)

            if variant == "Unknown":
                print("Unknown character set - stats for reference only")
            else:
                print(f"{variant.title()} character set")

            while True:
                # Flag to break out of nested menus
                exit_to_main = export_hanzi(
                    hanzi_df, stats_df, hanzi_list, outl, variant
                )
                if exit_to_main:
                    break  # Exit to main loop


if __name__ == "__main__":
    xw()

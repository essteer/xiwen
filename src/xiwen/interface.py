import polars as pl
import random
from .app import coordinator
from .utils.config import DEMO1, DEMO2
from .utils.export import export_hanzi
from .utils.terminal_display import get_TerminalDisplay_instance


def xw():
    """
    Main menu loop for CLI program
    Prompts user for URL to scan
    """
    terminal_display = get_TerminalDisplay_instance()
    print(terminal_display.get_welcome_message())
    while True:
        # Main menu - get URL from user
        target = input(terminal_display.get_main_menu_options())

        if target.upper() == "Q":  # Quit
            break

        if target == "":
            target = random.choice([DEMO1, DEMO2])
            print(terminal_display.get_demo_message())

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
                print(terminal_display.get_unknown_character_variant_message())
            else:
                print(f"{variant.title()} character set")

            while True:
                exit_to_main_menu_loop = export_hanzi(
                    hanzi_df, stats_df, hanzi_list, outl, variant
                )
                if exit_to_main_menu_loop:
                    break


if __name__ == "__main__":
    xw()

import random
from app import coordinator
from utils.config import DEMO_MESSAGE, DEMO1, DEMO2, MAIN_MENU_OPTIONS, WELCOME_MESSAGE
from utils.export import export_hanzi


def xiwen():
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
            # Explainer
            print(DEMO_MESSAGE)

        if target:
            # Run program
            hanzi_df, stats_df, hanzi_list, outl, variant = coordinator(target, True)

            # Print stats to CLI
            print(stats_df.to_markdown(index=False))
            if variant == "Unknown":
                print("Character set undefined - stats for reference only")
            else:
                print(f"{variant.title()} character set detected")

            while True:
                # CSV export loop
                # Flag to break out of nested menus
                exit_to_main = export_hanzi(
                    hanzi_df, stats_df, hanzi_list, outl, variant
                )
                if exit_to_main:
                    break  # Exit to main loop


if __name__ == "__main__":
    xiwen()

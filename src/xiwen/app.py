import random
from utils.config import DEMO_MESSAGE, DEMO1, DEMO2, MAIN_MENU_OPTIONS, WELCOME_MESSAGE
from utils.extract import get_hanzi
from utils.transform import partition_hanzi
from utils.analysis import analyse


def xiwen():
    """
    Main menu loop
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

        # Run URL
        hanzi_list = get_hanzi(target)
        if hanzi_list:
            # Divide into groups (with duplicates)
            simplified, traditional, outliers = partition_hanzi(hanzi_list)

            if simplified or traditional or outliers:
                analyse(hanzi_list, simplified, traditional, outliers)


if __name__ == "__main__":
    xiwen()

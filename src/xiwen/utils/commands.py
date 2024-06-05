import random
from utils.html import get_html
from utils.extract import extract_hanzi

import sys

sys.path.append("..")
from config import DEMO1, DEMO2, DEMO_MESSAGE


def cmd_demo() -> None:
    """
    Demo command - shows example character analysis
    """
    # Demo random choice of either Simp or Trad text
    demo = random.choice([DEMO1, DEMO2])
    # Explainer
    print(DEMO_MESSAGE)
    # Run URL
    cmd_url(demo)


def cmd_url(target_url: str | None = None) -> None:
    """
    URL command - prompts user to provide URL

    Parameters
    ----------
    target_url : str | None
        demo URL or None
    """
    if target_url is None:
        # Get user-provided URL
        target_url = str(input("Enter target URL: "))

        if target_url is None:
            return  # Exit on empty user input

    print("Parsing HTML...")

    try:  # Scrape HTML
        raw_html = get_html(target_url)
        if raw_html:  # Read HTML and extract text
            extract_hanzi(str(raw_html))
        return

    except ZeroDivisionError:
        print(f"No hanzi found: possible issue reading '{target_url}'.")
        return

    except Exception as e:
        print(f"An error occurred: {e}")
        return

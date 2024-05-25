import pandas as pd
from pypdf import PdfReader
from utils.hanzi import filter_text, partition_hanzi, identify, get_stats

##########################################################################
# Set encoding
##########################################################################

ENCODING = "utf-8"
# Encoding used to force .csv files to adopt utf-8 from Pandas DataFrame
ENCODING_HANZI = "utf_8_sig"

##########################################################################
# Process data - called from extract_loop.py and interface.py
##########################################################################


def _extract_from_pdf(pdf_path):
    """
    Extracts text from a PDF
    Args:
        - pdf_path, str, filepath of the PDF
    Returns:
        - text, str, text extracted from the PDF
    """
    text = ""

    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)

        for page in reader.pages:
            text += page.extract_text()

    return text


def process_data(
    target: str, hsk_simp: list, hsk_trad: list, html: bool = False
) -> tuple[list]:
    """
    Searches for and extracts Chinese characters (hanzi) from a text file
    according to whether they are simplified or traditional characters
    within the HSK1 to HSK6 vocabulary range, or other characters of either variant

    Args:
        - html, bool, flag True if html else False
        - target, str:
            - if html=False: path to file on device
            - if html=True: HTML extracted from URL
        - hsk_simp, list, all simplified hanzi from HSK1 to HSK9
        - hsk_trad, list, all traditional hanzi equivalents to hsk_simp
    Returns:
        NOTE: all lists below include duplicates
        - hanzi_list, list, full list of hanzi found
        - simplified, list, full list of simplified hanzi found belonging to HSK1 to HSK9
        - traditional, list, full list of traditional hanzi found equivalent to HSK1 to HSK9
            simplified hanzi
        - neutral, list, subset of hanzi common to both simplified and traditional
        - outliers, list, all hanzi found that don't belong to the above lists
    """
    global ENCODING

    if not html:
        # Send PDFs to _extract_from_pdf
        if target[-3:] == "pdf":
            text = _extract_from_pdf(target)

        else:
            with open(target, "r", encoding=ENCODING) as f:
                text = f.read()

    # if url=True, target is HTML
    else:
        text = target

    # Extract hanzi from text (with duplicates)
    hanzi_list = filter_text(text)
    # Divide into groups (with duplicates)
    simplified, traditional, neutral, outliers = partition_hanzi(
        hsk_simp, hsk_trad, hanzi_list
    )

    return hanzi_list, simplified, traditional, neutral, outliers


##########################################################################
# Analyse data - called from interface.py and extract_loop.py
##########################################################################


def analyse_data(
    df: pd.DataFrame, hl: list, simplified: list, traditional: list, neutral: list
) -> tuple[str | pd.DataFrame]:
    """
    Receives the output of process_data
    Gets the character variant and statistical breakdowns
        - number of unique characters and number of total characters
            by grade, and cumulative figures for the entire content
    Args:
        - df, Pandas DataFrame, HSK character list
        - hl, list, all hanzi in the entire content
        - simplified, list, simplified HSK hanzi in hl
        - traditional, list, traditional HSK hanzi in hl
        - neutral, list, hanzi common to simplified and traditional lists
    Returns:
        - variant, str, hanzi variant of the content
        - stats_dataframe, Pandas DataFrame, stats for the content
        - hanzi_dataframe, Pandas DataFrame, df with counts added
    """
    # Query character variant
    variant = identify(simplified, traditional, neutral)
    # Create mapping for analysis
    variants = {
        "Simplified": simplified,
        "Traditional": traditional,
        "Unknown": (simplified, traditional),
    }
    # Use copy of HSK_HANZI DataFrame for analysis
    hanzi_df = df.copy()
    # Get statistical breakdown of hanzi content
    stats_dataframe, hanzi_dataframe = get_stats(
        hanzi_df, hl, variants[variant], variant
    )

    return variant, stats_dataframe, hanzi_dataframe

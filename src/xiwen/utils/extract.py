from .html import get_html


def filter_hanzi(char: str) -> bool:
    """
    Checks whether a character is a (possible)
    Chinese character against three Unicode sets:
        - Common        ["\u4e00", "\u9fff"]
        - Extended-A    ["\u3400", "\u4dbf"]
        - Extended-B    ["\u20000", "\u2a6dF"]

    Parameters
    ----------
    char : str
        a single character

    Returns
    -------
    bool
        True if char in Common | Extended-A | Extended-B
        False otherwise
    """
    symbols = ["–", "—", "‘", "’", "“", "”", "…", "⊼", "⁆", "∕", "。"]
    # Unrecognised hanzi with no matching pinyin
    exceptions = ["㤙"]

    if ord(char) in range(8206, 8287):
        return False

    if char in symbols or char in exceptions:
        return False

    common = char >= "\u4e00" and char <= "\u9fff"
    ext_a = char >= "\u3400" and char <= "\u4dbf"
    ext_b = char >= "\u20000" and char <= "\u2a6dF"

    return True if common or ext_a or ext_b else False


def filter_text(html: str) -> list[str]:
    """
    Passes text to filter_hanzi
    Returns all hanzi in text (duplicates included)

    Parameters
    ----------
    html : str
        HTML extracted from URL

    Returns
    -------
    result : list[str]
        full list of hanzi found
    """
    return [zi for zi in html if filter_hanzi(zi)]


def get_hanzi(target: str) -> list[str]:
    """
    Passes URL to retrieve HTML
    Extracts all Chinese characters from HTML

    Parameters
    ----------
    target : str
        URL to extract HTML from

    Returns
    -------
    hanzi_list : list
        full list of hanzi found
    """
    html = get_html(target)
    if not html:
        return []

    # Extract hanzi from HTML (with duplicates)
    hanzi = filter_text(str(html))

    return hanzi

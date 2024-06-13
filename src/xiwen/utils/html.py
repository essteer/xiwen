import requests
import time
from bs4 import BeautifulSoup
from masquer import masq


def get_html(url: str) -> BeautifulSoup:
    """
    Extracts HTML from a user-provided URL

    Parameters
    ----------
    url : str
        URL provided by user

    Returns
    -------
    html : BeautifulSoup
        HTML extracted from URL
    """
    # Make request and catch response errors and retry
    for i in range(3):
        try:
            # Get randomised user-agent and referer data
            header = masq(ua=True, rf=True)
            header["Accept-Language"] = "en-US,en;q=0.9;q=0.7,zh-CN;q=0.6,zh;q=0.5"
            # Get URL content
            response = requests.get(url, headers=header, timeout=10)
            # Catch errors
            response.raise_for_status()
            # Extract and parse HTML
            raw_html = BeautifulSoup(response.text, "html.parser")

            return raw_html

        except requests.exceptions.RequestException:
            time.sleep(2 ** (i + 1))

    return

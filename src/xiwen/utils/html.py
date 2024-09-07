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
    _ : BeautifulSoup
        HTML extracted from URL
    """
    max_retries = 3
    for i in range(max_retries):
        try:
            header = masq(
                ua=True, rf=True
            )  # Get weighted-random user-agent and referer
            header["Accept-Language"] = "en-US,en;q=0.9;q=0.7,zh-CN;q=0.6,zh;q=0.5"
            response = requests.get(url, headers=header, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")

        except requests.exceptions.RequestException:
            time.sleep(2**i)

import logging
import requests
import time
from bs4 import BeautifulSoup
from masquer import masq


logging.basicConfig(
    filename="./logs/error.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
)

# Response codes
GOOD_RESPONSES = [200]
RETRY_RESPONSES = [429]
BAD_RESPONSES = [400, 401, 403, 404, 500, 502, 504]


def extractor(url: str) -> str | bool:
    """
    Extracts HTML from a user-provided URL
    Args:
        - url, str, URL provided by user
    Returns:
        - html, str, HTML extracted from url, or
        - False, bool, if HTML extract fails
    """
    # Get randomised user-agent and referer data
    header = masq(ua=True, rf=True, hd=True)
    header["Accept-Language"] = ("en-US,en;q=0.9;q=0.7,zh-CN;q=0.6,zh;q=0.5",)

    # Make request and catch response errors and retry
    for i in range(3):
        target_html = requests.get(url, headers=header)

        if isinstance(target_html, requests.models.Response):
            if target_html.status_code not in RETRY_RESPONSES:
                break

            else:  # Exponential delay before each retry
                time.sleep(2 ** (i + 1))

    if isinstance(target_html, requests.models.Response):
        if target_html.status_code in BAD_RESPONSES:
            logging.error(f"{target_html.status_code} response; url: {url}")
            return False

        elif target_html.status_code not in GOOD_RESPONSES:
            logging.info(f"{target_html.status_code} response; url: {url}")
            return False

    # Extract and parse html source code
    target_URL_source_code = target_html.text
    raw_html = BeautifulSoup(target_URL_source_code, "html.parser")

    return raw_html

import logging
import random
import requests
import time
from bs4 import BeautifulSoup


logging.basicConfig(
    filename="./logs/error.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
)

# Response codes
GOOD_RESPONSES = [200]
RETRY_RESPONSES = [429]
BAD_RESPONSES = [400, 401, 403, 404, 500, 502, 504]

# ~~~ Header data ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

REFERERS = [
    "https://www.google.com/",
    "https://bing.com/",
    "https://search.yahoo.com/",
    "https://www.baidu.com/",
    "https://yandex.com/",
]

REFERER_PROBS = [0.88, 0.03, 0.03, 0.03, 0.03]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60",
    "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47",
]

USER_AGENT_PROBS = [
    0.205,
    0.14,
    0.13,
    0.105,
    0.055,
    0.055,
    0.05,
    0.045,
    0.04,
    0.03,
    0.025,
    0.02,
    0.015,
    0.015,
    0.015,
    0.0125,
    0.0125,
    0.012,
    0.01,
    0.008,
]

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9;q=0.7,zh-CN;q=0.6,zh;q=0.5",
    "Referer": "https://www.google.com/",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
}

##########################################################################
# Helper function
##########################################################################


def _weighted_random_selection(sample_space: list[str], probs: list[float]) -> str:
    """
    Args:
        sample_space: list of options to randomly select from
        probs: list of probabilites per sample in sample_space (sum == 1)
    Returns:
        weighted random selection from sample_space
    """
    weighted_random_selection = random.choices(sample_space, weights=probs, k=1)

    return weighted_random_selection[0]


##########################################################################
# HTML extraction
##########################################################################


def extractor(url: str) -> str | bool:
    """
    Extracts HTML from a user-provided URL
    Args:
        - url, str, URL provided by user
    Returns:
        - html, str, HTML extracted from url, or
        - False, bool, if HTML extract fails
    """
    # Assign weighted random referer and user-agent to header
    referer = _weighted_random_selection(REFERERS, REFERER_PROBS)
    user_agent = _weighted_random_selection(USER_AGENTS, USER_AGENT_PROBS)
    header["Referer"] = referer
    header["User-Agent"] = user_agent

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

import unittest
from bs4 import BeautifulSoup
from src.xiwen.utils.html import get_html


class TestGetHTML(unittest.TestCase):
    def test_invalid_urls(self):
        """Test with invalid URL input"""
        url = ""
        self.assertEqual(get_html(url), None)
        url = "Test with invalid URL input"
        self.assertEqual(get_html(url), None)

    def test_valid_urls(self):
        """Test with stable URLs"""
        url = "https://www.google.com"
        self.assertIsInstance(get_html(url), BeautifulSoup)
        url = "https://www.bing.com"
        self.assertIsInstance(get_html(url), BeautifulSoup)
        url = "https://www.scrapethissite.com/"
        self.assertIsInstance(get_html(url), BeautifulSoup)


if __name__ == "__main__":
    unittest.main()

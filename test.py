import unittest
from bs4 import BeautifulSoup
from unittest.mock import patch, MagicMock
import main


class TestWebScraper(unittest.TestCase):
    def test_request(self):
        
        soup = main.request("https://www.google.com/about/careers/applications/jobs/results?location=San%20Jose%2C%20CA%2C%20USA&page=1#!t=jo&jid=127025001&", "")

        # Check for the return data type
        self.assertIsInstance(soup, BeautifulSoup)
        # Check if required html tags are found
        self.assertIsNotNone(soup.find_all("div", {"class":"sMn82b"}))

    def test_parse(self):
        sample_html = """
        <div class="sMn82b">
            <h3 class="QJPWVe">Job Title1</h3>
            <span class="wVSTAb">Advanced</span>
            <a class="WpHeLc VfPpkd-mRLv6 VfPpkd-RLmnJb" href="/joblink1"></a>
        </div>
        <div class="sMn82b">
            <h3 class="QJPWVe">Job Title2</h3>
            <span class="wVSTAb">Mid</span>
            <a class="WpHeLc VfPpkd-mRLv6 VfPpkd-RLmnJb" href="/joblink2"></a>
        </div>
        """

        soup = BeautifulSoup(sample_html, "html.parser")

        # Call the parse function
        counter = 0
        data = []
        limit=-1
        is_parsing=True
        result, is_parsing = main.parse(soup, counter, data, limit, is_parsing)

        # Check if result is a list
        self.assertIsInstance(result, list)
        # Check if sample result and actuall result
        self.assertTrue(result, soup)


if __name__=="__main__":
    unittest.main()
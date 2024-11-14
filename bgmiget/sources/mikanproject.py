import os
from typing import List

import requests
from bs4 import BeautifulSoup

from ..result import Result

BASE_URL = "https://mikanani.me/"


class MiKanProject:

    def search(self, query: str) -> List[Result]:

        URL = BASE_URL + "Home/Search?searchstr=" + query

        page = requests.get(URL, proxies={
            'http': os.getenv("HTTP_PROXY"),
            'https': os.getenv("HTTPS_PROXY"),
        })
        soup = BeautifulSoup(page.content, "html.parser")

        results = []
        for i in soup.find_all("tr", class_="js-search-results-row"):
            title = i.find("a", class_="magnet-link-wrap").text
            url = i.find(
                "a", class_="js-magnet magnet-link")["data-clipboard-text"]
            result = Result(title, url)
            results.append(result)
        return results

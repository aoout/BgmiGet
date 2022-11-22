import requests
from bs4 import BeautifulSoup
from torrentp import TorrentDownloader

BASE_URL = "https://mikanani.me/"


class MiKanProject:
    def __init__(self) -> None:
        self.results = None

    def search(self, query):
        URL = "https://mikanani.me/Home/Search?searchstr=" + query
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        self.results = [(i.find("a", class_="magnet-link-wrap").text, i.find(
            "a", class_="js-magnet magnet-link")["data-clipboard-text"]) for i in soup.find_all("tr", class_="js-search-results-row")]
        self.show_results()

    def download(self, index):

        url = self.results[index][1]
        torrent_file = TorrentDownloader(url, ".")
        torrent_file.start_download()

    def show_results(self):
        for i, result in enumerate(self.results):
            print(str(i)+" -> "+result[0])
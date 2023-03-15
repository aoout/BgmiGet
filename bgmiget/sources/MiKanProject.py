import requests
from bs4 import BeautifulSoup
from torrentp import TorrentDownloader

BASE_URL = "https://mikanani.me/"


class MiKanProject:
    '''
    Search resources from https://mikanani.me/ and download.
    '''
    def __init__(self) -> None:
        self.results = None

    def search(self, query:str)->None:
        '''
        Search anime.
        '''
        URL = BASE_URL + "Home/Search?searchstr=" + query
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        self.results = [(i.find("a", class_="magnet-link-wrap").text, i.find(
            "a", class_="js-magnet magnet-link")["data-clipboard-text"]) for i in soup.find_all("tr", class_="js-search-results-row")]

    def download(self, path:str, index:int)->None:
        '''
        Download the file of the specified index to the specified path.
        '''
        if index != "all":
            url = self.results[index][1]
            torrent_file = TorrentDownloader(url, path)
            torrent_file.start_download()
        else:
            for i in range(len(self.results)):
                self.download(path, i)

    def show_results(self)->None:
        '''
        Show search results.
        '''
        for i, result in enumerate(self.results):
            print(f"{i:<4} -> {result[0]}")


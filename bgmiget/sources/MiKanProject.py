import re

import requests
from bs4 import BeautifulSoup
from torrentp import TorrentDownloader

BASE_URL = "https://mikanani.me/"


class MiKanProject:
    def __init__(self) -> None:
        self.results = None

    def search(self, query):
        URL = BASE_URL + "Home/Search?searchstr=" + query
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        self.results = [(i.find("a", class_="magnet-link-wrap").text, i.find(
            "a", class_="js-magnet magnet-link")["data-clipboard-text"]) for i in soup.find_all("tr", class_="js-search-results-row")]
        self.show_results()

    def download(self, path, index):
        if index != "all":
            url = self.results[index][1]
            torrent_file = TorrentDownloader(url, path)
            torrent_file.start_download()
        else:
            for i in range(len(self.results)):
                self.download(path, i)

    def show_results(self):
        for i, result in enumerate(self.results):
            print(str(i)+" -> "+self.more_useful_name(result[0]))

    def more_useful_name(self, name):
        # todo: 添加更多的正则规则
        # name = re.sub("\d{1,2}月新番", "", name)
        # name = re.sub("（急招翻译、校对）", "", name)
        # if simple_des:
        #   name = re.sub("[WEBrip]", "", name)
        # 这些规则不应该内置，而是有一个命令用于添加，而有一些默认的规则被写进了一个配置文件里,或者也可以是空的
        return name

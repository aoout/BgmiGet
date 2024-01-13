import hashlib
import logging
import os
import time

import fire
from torrentp import TorrentDownloader

from .persistentdict import PersistentDict
from .sources import MiKanProject

data = PersistentDict(os.path.expanduser("~//.bgmiget"))
logging.basicConfig(handlers=[logging.FileHandler('bgmiget.log','w','utf-8')], level=logging.DEBUG)


class BgmiGet:

    '''
    Used to build the main command-line program.
    '''

    def __init__(self, source) -> None:
        self.source = source()

    def search(self, query: str, episode: str = "", subtitleType: str = "", subtitleGroup: str = "",limit: int = 100) -> None:
        '''
        Search anime through various meta information.
        '''
        episode = str(episode)

        timestamp = int(time.time())
        hashString = "|".join([query, episode, subtitleType, subtitleGroup])
        searchHash = hashlib.sha256(hashString.encode('utf-8')).hexdigest()

        for key in list(data.keys()):
            if isinstance(data[key], dict) and "timestamp" in data[key]:
                    if timestamp - data[key]["timestamp"] > 300:
                        del data[key]


        if searchHash in data:
            logging.info(f"Found {query} in cache. Timestamp: {data[searchHash]['timestamp']}")
            results = data[searchHash]["results"]
        else:
            results = self.source.search(query)
            if episode or subtitleType or subtitleGroup:
                results = [r for r in results if (not episode or r.episode == episode)
                           and (not subtitleType or r.subtitleType == subtitleType)
                           and (not subtitleGroup or subtitleGroup in r.title)]
            data[searchHash] = {"results": results, "timestamp": timestamp}
            logging.info(f"Saved {query} to cache. Timestamp: {data[searchHash]['timestamp']}")

        data["results"] = results
        data.save()
        if(len(results)>limit):
            results = results[0:limit]
        for i, r in enumerate(results):
            print(f"{i:<4} -> {r.title}")

    def download(self, index: int) -> None:
        '''
        Download file by index.
        '''
        result = data["results"][index]
        torrent_file = TorrentDownloader(result.url, ".")
        torrent_file.start_download()

        subscribed_animes = data.get("subscribed_animes", [])
        anime = [i for i in subscribed_animes if i in result.title]

        if len(anime) > 1:
            logging.warning(
                "More than one result found. Defaulting to the first one.")
        if len(anime) == 0:
            logging.debug("No results found.")
        else:
            anime = anime[0]
            data["subscribed_animes"][anime]["max_episode"] = max(
                data["subscribed_animes"][anime]["max_episode"], int(result.episode))

    def subscribe(self, query: str) -> int:
        '''
        Subscribe to an anime.
        '''
        subscribed_animes = data.get("subscribed_animes", {})
        if query in subscribed_animes:
            print("Already subscribed.")
            return 0
        else:
            subscribed_animes[query] = {}
            subscribed_animes[query]["max_episode"] = 0
            data["subscribed_animes"] = subscribed_animes
            data.save()
            print("You have successfully subscribed.")
            return 1

    def upgrade(self) -> int:
        '''
        Check for updates for each subscribed anime.
        '''
        subscribed_animes = data.get("subscribed_animes", [])
        if not subscribed_animes:
            print("No subscribed anime found.")
            return 0

        for anime in subscribed_animes:

            max_episode = data["subscribed_animes"][anime]["max_episode"]
            results = self.source.search(anime)
            available_max_episode = 0
            for r in results:
                if r.episode and r.episode.isdigit() and int(r.episode) > available_max_episode:
                    available_max_episode = int(r.episode)
            if available_max_episode > max_episode:
                print(f"{anime} : {max_episode} -> {available_max_episode}")
        return 1

    def show_subscribed(self) -> int:
        '''
        Show all subscribed anime and their max_episode.
        '''
        subscribed_animes = data.get("subscribed_animes", [])
        if not subscribed_animes:
            print("No subscribed anime found.")
            return 0

        for anime in subscribed_animes:
            max_episode = data["subscribed_animes"][anime]["max_episode"]
            print(f"{anime} -> {max_episode}")
        return 1


def main():

    bgmiget = BgmiGet(source=MiKanProject)
    fire.Fire(bgmiget)

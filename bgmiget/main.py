import os
import pickle
from dataclasses import asdict, dataclass, field

import fire
from dacite import from_dict

from .sources import MiKanProject
from .result import Result

data_path = os.path.expanduser("~//.bgmiget")


@dataclass
class Data:
    results: list = field(default_factory=list)
    old_results: list = field(default_factory=list)


data = Data()
if os.path.exists(data_path):
    data = from_dict(data_class=Data, data=pickle.load(open(data_path, "rb")))


class BgmiGet:
    def __init__(self, source):
        self.source = source()

    def write_results(self):
        data.old_results = data.results
        data.results = self.source.results
        pickle.dump(asdict(data), open(data_path, "wb"))

    def search(self, query: str, episode: str = None, subtitleType: str = None, subtitleGroup: str = None):

        episode = str(episode)
        self.source.search(query)
        if episode or subtitleType or subtitleGroup:
            results = self.source.results.copy()
            for r in self.source.results:
                R = Result(r[0])
                if episode:
                    if R.episode != episode:
                        results.remove(r)
                        continue
                if subtitleType:
                    if R.subtitleType != subtitleType:
                        results.remove(r)
                        continue
                if subtitleGroup:
                    if subtitleGroup not in R.title:
                        results.remove(r)

            self.source.results = results
        self.write_results()
        self.source.show_results()


    def download(self, index="all"):
        self.source.results = data.results
        self.source.download(".", index)


def main():

    bgmiget = BgmiGet(source=MiKanProject)
    fire.Fire({
        "search": bgmiget.search,
        "download": bgmiget.download
    })

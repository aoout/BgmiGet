import os
import pickle
from dataclasses import asdict, dataclass, field

import fire
from dacite import from_dict

from .sources import MiKanProject

data_path = os.path.expanduser("~//.bgmiget")


@dataclass
class Data:
    results: list = field(default_factory=list)
    old_results: list = field(default_factory=list)
    save_path: str = ""


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

    def search(self, query):
        self.source.search(query)
        self.write_results()

    def set_save_path(self, path):
        data.save_path = path
        pickle.dump(asdict(data), open(data_path, "wb"))

    def download(self, index="all"):
        self.source.results = data.results
        self.source.download(data.save_path, index)

    def include(self, keyword):
        self.source.results = data.results
        self.source.results = [(text, url)
                               for text, url in self.source.results if keyword in text]
        self.source.show_results()
        self.write_results()

    def exclude(self, keyword):
        self.source.results = data.results
        self.source.results = [(text, url)
                               for text, url in self.source.results if keyword not in text]
        self.source.show_results()
        self.write_results()

    def undo(self):
        self.source.results = data.old_results
        self.source.show_results()
        self.write_results()


def main():

    bgmiget = BgmiGet(source=MiKanProject)
    fire.Fire({
        "search": bgmiget.search,
        "set_save_path": bgmiget.set_save_path,
        "download": bgmiget.download,
        "include": bgmiget.include,
        "exclude": bgmiget.exclude,
        "undo": bgmiget.undo
    })

import fire
from .sources import MiKanProject
import pickle
import os

folder_path = os.path.expanduser('~\\.bgmiget')
results_path = os.path.expanduser('~\\.bgmiget\\results.pickle')
old_results_path = os.path.expanduser('~\\.bgmiget\\old_results.pickle')
if not os.path.exists(folder_path):
    os.mkdir(folder_path)


class BgmiGet:
    def __init__(self, source):
        self.source = source()

    def read_data(self):
        self.source.results = pickle.load(open(results_path, "rb"))

    def write_data(self):
        if os.path.exists(old_results_path):
            os.remove(old_results_path)
        if os.path.exists(results_path):
            os.rename(results_path, old_results_path)

        pickle.dump(self.source.results, open(results_path, "wb"))

    def read_old_data(self):
        self.source.results = pickle.load(
            open(old_results_path, "rb"))

    def search(self, query):
        self.source.search(query)
        self.write_data()

    def download(self, index):
        self.read_data()
        self.source.download(index)

    def include(self, keyword):
        self.read_data()
        self.source.results = [(text, url)
                               for text, url in self.source.results if keyword in text]
        self.source.show_results()
        self.write_data()

    def exclude(self, keyword):
        self.read_data()
        self.source.results = [(text, url)
                               for text, url in self.source.results if keyword not in text]
        self.source.show_results()
        self.write_data()

    def undo(self):
        self.read_old_data()
        self.source.show_results()


def main():

    bgmiget = BgmiGet(source=MiKanProject)
    fire.Fire({
        "search": bgmiget.search,
        "download": bgmiget.download,
        "include": bgmiget.include,
        "exclude": bgmiget.exclude,
        "undo": bgmiget.undo
    })

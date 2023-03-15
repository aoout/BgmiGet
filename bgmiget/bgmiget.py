import fire

from .candle import candle
from .data import Data, data_path
from .result import Result
from .sources import MiKanProject


class BgmiGet:
    '''
    Used to build the main command-line program.
    '''
    def __init__(self, source):
        self.source = source()

    def search(self, query: str, episode: str = None, subtitleType: str = None, subtitleGroup: str = None):
        '''
        Search anime through various meta information.
        '''
        episode = str(episode)

        self.source.search(query)
        if episode or subtitleType or subtitleGroup:
            results = [r for r in self.source.results if (not episode or Result(r[0]).episode == episode)
                       and (not subtitleType or Result(r[0]).subtitleType == subtitleType)
                       and (not subtitleGroup or subtitleGroup in Result(r[0]).title)]
            self.source.results = results
        with candle(Data, data_path) as data:
            data.results = self.source.results
        self.source.show_results()

    def download(self, index="all"):
        '''
        Download file by index.
        '''
        with candle(Data, data_path) as data:
            self.source.results = data.results
        self.source.download(".", index)


def main():

    bgmiget = BgmiGet(source=MiKanProject)
    fire.Fire(bgmiget)

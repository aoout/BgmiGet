import re
import logging

class Result:
    '''
    Parse metadata to better display search results.
    '''
    def __init__(self, title: str) -> None:
        self.title = title
        self.parse()

    def parse(self) -> None:
        '''
        Parse meta information from title.
        '''
        self.subtitleType = self.parseSubtitle()
        self.episode = self.parseEpisode()

    def parseSubtitle(self) -> str:
        '''
        Parse subtitle language from title.
        '''
        return "tc" if ("繁" in self.title and "简" not in self.title) else "sc"

    def parseEpisode(self) -> str:
        '''
        Parse episode from title.
        '''
        if "NCOPED" in self.title:
            return "NCOPED"
        if "OVA" in self.title:
            return "OVA"
        pattern = re.compile(r'(?P<prefix>第|未删减)?(?P<episode>\d+)(?P<suffix>话|話|集|v2|先行版)?')
        match = pattern.search(self.title)
        try:
            return str(int(match.group(0))) if match.group(0).isdigit() else match.group(0)
        except:
            logging.warning(f"Failed to parse {self.title}. The value of match is {match}")
            return 0


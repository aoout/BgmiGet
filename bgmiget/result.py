import re
import logging
from functools import cached_property

logging.basicConfig(handlers=[logging.FileHandler('bgmiget.log','w','utf-8')], level=logging.DEBUG)

class Result:
    '''
    Parse metadata to better display search results.
    '''
    def __init__(self, title: str, url: str) -> None:
        self.title = title
        self.url = url

    @cached_property
    def subtitleType(self) -> str:
        '''
        Parse subtitle language from title.
        '''
        return "tc" if ("繁" in self.title and "简" not in self.title) else "sc"

    @cached_property
    def episode(self) -> str:
        '''
        Parse episode from title.
        '''
        if "NCOPED" in self.title:
            return "NCOPED"
        if "OVA" in self.title:
            return "OVA"
        pattern = re.compile(r'(?![^ \[]])(第|未删减|_)?(?P<episode>\d+)(话|話|集|v2|先行版)?(?![^ \]])')
        match = pattern.search(self.title)
        try:
            matched = match.group("episode")
            logging.debug(f"Successfully parsed episode {matched} from {self.title}")
            return str(int(matched)) if matched.isdigit() else matched
        except:
            logging.warning(f"Failed to parse {self.title}. The value of match is {match}")
            return 0

    def __str__(self):
        return f"Title: {self.title}, Subtitle: {self.subtitleType}, Episode: {self.episode}, URL: {self.url}"

    def __repr__(self):
        return f"Result(title={self.title}, subtitle={self.subtitleType}, episode={self.episode}, url={self.url})"

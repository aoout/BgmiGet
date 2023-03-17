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
        prefix = ["第","未删减"]
        suffix = ["話","话","集","v2","先行版"]
        prefixString = "".join([f"(?:{i})?" for i in prefix])
        suffixString = "".join([f"(?:{i})?" for i in suffix])

        pattern = re.compile(f"(?<![\dA-Za-z\u4e00-\u9fa5]){prefixString}(\d+){suffixString}(?![\dA-Za-z\u4e00-\u9fa5])")
        match = pattern.search(self.title)
        if match:
            return str(int(match.group(1))) if match.group(1).isdigit() else match.group(1)
        else:
            logging.warning(f"{self.title}")
            logging.warning(f"{match}")
import re
import logging

class Result:
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

        patternString = f"(?<![\dA-Za-z\u4e00-\u9fa5]){prefixString}(\d+){suffixString}(?![\dA-Za-z\u4e00-\u9fa5])"
        pattern = re.compile(patternString)
        try:
            _ = pattern.findall(self.title)[0]
            if _.isdigit():
                return str(int(_))
            return _
        except:
            logging.warning(f"{self.title}")
            logging.warning(f"{pattern.findall(self.title)}")

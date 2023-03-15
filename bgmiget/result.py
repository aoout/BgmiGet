import re
from typing import List, Union
FETCH_EPISODE_WITH_BRACKETS = re.compile(r"[【\[]E?(\d+)\s?(?:END)?[】\]]")

FETCH_EPISODE_ZH = re.compile(r"第?\s?(\d{1,3})\s?[話话集]")
FETCH_EPISODE_ALL_ZH = re.compile(r"第([^第]*?)[話话集]")
FETCH_EPISODE_ONLY_NUM = re.compile(r"^([\d]{2,})$")

FETCH_EPISODE_RANGE = re.compile(r"[^sS][\d]{2,}\s?-\s?([\d]{2,})")
FETCH_EPISODE_RANGE_ZH = re.compile(r"[第][\d]{2,}\s?-\s?([\d]{2,})\s?[話话集]")
FETCH_EPISODE_RANGE_ALL_ZH_1 = re.compile(r"[全]([\d-]*?)[話话集]")
FETCH_EPISODE_RANGE_ALL_ZH_2 = re.compile(r"第?(\d-\d)[話话集]")

FETCH_EPISODE_OVA_OAD = re.compile(r"([\d]{2,})\s?\((?:OVA|OAD)\)]")
FETCH_EPISODE_WITH_VERSION = re.compile(r"[【\[](\d+)\s? *v\d(?:END)?[】\]]")

FETCH_EPISODE = (
    FETCH_EPISODE_ZH,
    FETCH_EPISODE_ALL_ZH,
    FETCH_EPISODE_WITH_BRACKETS,
    FETCH_EPISODE_ONLY_NUM,
    FETCH_EPISODE_RANGE,
    FETCH_EPISODE_RANGE_ALL_ZH_1,
    FETCH_EPISODE_RANGE_ALL_ZH_2,
    FETCH_EPISODE_OVA_OAD,
    FETCH_EPISODE_WITH_VERSION,
)


def chinese_to_arabic(cn: str) -> int:
    """
    https://blog.csdn.net/hexrain/article/details/52790126
    :type cn: str
    :rtype: int
    """
    CN_NUM = {
        "〇": 0,
        "一": 1,
        "二": 2,
        "三": 3,
        "四": 4,
        "五": 5,
        "六": 6,
        "七": 7,
        "八": 8,
        "九": 9,
        "零": 0,
        "壹": 1,
        "贰": 2,
        "叁": 3,
        "肆": 4,
        "伍": 5,
        "陆": 6,
        "柒": 7,
        "捌": 8,
        "玖": 9,
        "貮": 2,
        "两": 2,
    }

    CN_UNIT = {
        "十": 10,
        "拾": 10,
        "百": 100,
        "佰": 100,
        "千": 1000,
        "仟": 1000,
        "万": 10000,
        "萬": 10000,
    }
    unit = 0  # current
    ldig = []  # digest
    for cndig in reversed(cn):
        if cndig in CN_UNIT:
            unit = CN_UNIT[cndig]
            if unit in (10000, 100000000):
                ldig.append(unit)
                unit = 1
        else:
            dig = CN_NUM[cndig]
            if unit:
                dig *= unit
                unit = 0
            ldig.append(dig)
    if unit == 10:
        ldig.append(10)
    val, tmp = 0, 0
    for x in reversed(ldig):
        if x in (10000, 100000000):
            val += tmp * x
            tmp = 0
        else:
            tmp += x
    val += tmp
    return val


class Result:
    def __init__(self, title: str) -> None:
        self.title = title
        self.parse()

    def parse(self) -> None:
        '''
        Parse meta information from title.
        '''
        self.parseSubtitle()
        self.episode = self.parse_episode(self.title)

    def parseSubtitle(self) -> None:
        '''
        Parse subtitle language from title.
        '''
        if "繁" not in self.title and "简" not in self.title:
            self.subtitleType = "sc"
        elif "简" in self.title:
            self.subtitleType = "sc"
        else:
            self.subtitleType = "tc"

    def parse_episode(self,episode_title: str) -> int:

        spare = None

        def get_real_episode(episode_list: Union[List[str], List[int]]) -> int:
            return min(int(x) for x in episode_list)

        for pattern in (FETCH_EPISODE_RANGE_ALL_ZH_1, FETCH_EPISODE_RANGE_ALL_ZH_2):
            _ = pattern.findall(episode_title)
            if _ and _[0]:
                return int(0)

        _ = FETCH_EPISODE_RANGE.findall(episode_title)
        if _ and _[0]:
            return int(0)

        _ = FETCH_EPISODE_RANGE_ZH.findall(episode_title)
        if _ and _[0]:
            return int(0)

        _ = FETCH_EPISODE_ZH.findall(episode_title)
        if _ and _[0].isdigit():
            return int(_[0])

        _ = FETCH_EPISODE_ALL_ZH.findall(episode_title)
        if _ and _[0]:
            try:
                e = chinese_to_arabic(_[0])
                return e
            except Exception:
                pass
        _ = FETCH_EPISODE_WITH_VERSION.findall(episode_title)
        if _ and _[0].isdigit():
            return int(_[0])

        _ = FETCH_EPISODE_WITH_BRACKETS.findall(episode_title)
        if _:
            return get_real_episode(_)

        rest: List[int] = []
        for i in episode_title.replace("[", " ").replace("【", ",").split(" "):
            for regexp in FETCH_EPISODE:
                match = regexp.findall(i)
                if match and match[0].isdigit():
                    m = int(match[0])
                    if m > 1000:
                        spare = m
                    else:
                        rest.append(m)

        if rest:
            return get_real_episode(rest)

        if spare:
            return spare

        return 0

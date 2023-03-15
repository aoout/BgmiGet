import os
from dataclasses import dataclass, field

data_path = os.path.expanduser("~//.bgmiget")


@dataclass
class Data:
    results: list = field(default_factory=list)

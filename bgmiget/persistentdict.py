import os
import pickle
from collections import UserDict

class PersistentDict(UserDict):
    def __init__(self, filename):
        self.filename = filename

        if os.path.exists(filename):
            with open(filename, "rb") as f:
                data = pickle.load(f)
                super().__init__(data)
        else:
            super().__init__()

    def save(self):
        with open(self.filename, "wb") as f:
            pickle.dump(self.data, f)
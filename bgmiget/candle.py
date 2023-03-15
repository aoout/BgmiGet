import pickle
from contextlib import contextmanager
from dataclasses import asdict
from typing import Type

from dacite import from_dict


@contextmanager
def candle(dataClass:Type,dataPath:str):
    '''
    Store data more safely with context managers.
    '''
    data = dataClass()
    data = from_dict(data_class=dataClass,data=pickle.load(open(dataPath,"rb")))
    yield data
    pickle.dump(asdict(data),open(dataPath,"wb"))
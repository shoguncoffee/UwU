"""

"""
import os, sys
import tqdm
import numpy, itertools
from datetime import datetime, date, time
from dataclasses import dataclass
from types import ModuleType
from typing import (
    ItemsView, 
    Any, 
    Callable, 
    Type, 
    TYPE_CHECKING, 
    Generator, 
    TypeVar, 
    Union, 
    Sequence, 
    Optional,
)
for func in vars(__import__('checking')).values():
    if callable(func) and (error := func()):
        raise Exception(error)
    
if TYPE_CHECKING:
    ...
    
def qwe():
    os
    

if __name__ == '__main__':
    print(__class__)
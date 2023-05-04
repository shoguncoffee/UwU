"""
necessary packages
"""
import os, sys
import csv, json, pickle
import datetime as dt

# import tqdm
# import numpy as np
# from moneyed import Money

from uuid import UUID, uuid4
from math import ceil, floor
from copy import deepcopy
from time import sleep
from random import sample, choice, randrange, random
from dataclasses import (
    dataclass, 
    field, 
    replace, 
    KW_ONLY
)
# to reduce verbose function and loop 
# https://docs.pythonorg/3/library/functools.html
# https://docs.python.org/3/library/itertools.html
import operator
from functools import reduce, partial 
from itertools import (
    product,
    repeat, 
    islice, 
    count, 
    cycle,
    combinations,
    compress,
    pairwise,
    takewhile,
    accumulate,
    chain,
)
# for type check and hinting
# https://docs.python.org/3/library/typing.html
from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import (
    Literal,
    overload,
    ItemsView, 
    Any, 
    Callable, 
    Type, 
    TYPE_CHECKING, 
    Generator, 
    TypeVar, 
    Sequence, 
    Optional,
    ClassVar,
    Self,
    Collection,
    Iterable,
    Annotated,
    Literal,
    Iterator,
)
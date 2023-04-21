"""
necessary packages
"""
import os, sys
import numpy
import csv, json
import datetime as dt
# import tqdm

from uuid import UUID, uuid4
# from moneyed import Money
from math import ceil, floor
from copy import deepcopy
from dataclasses import (
    dataclass, 
    field, 
    replace, 
    KW_ONLY
)
from itertools import (
    product,
    repeat, 
    islice, 
    count, 
    cycle
)
from abc import ABC, abstractmethod
from types import ModuleType
from typing import (
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
)
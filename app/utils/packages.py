"""
necessary packages
"""
import os, sys
import numpy
import csv, json
import datetime as dt
# import tqdm

from dataclasses import dataclass, field, replace, KW_ONLY, asdict
from uuid import UUID, uuid4

# from moneyed import Money
from math import ceil, floor
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
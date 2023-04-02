"""
necessary packages
"""
import os, sys
import numpy
import csv, json
import asyncio
# import tqdm

from datetime import datetime, date, time, timedelta
from dataclasses import dataclass, field, replace, KW_ONLY
from uuid import UUID, uuid4

# from moneyed import Money
from math import ceil, floor
from random import randint
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
)
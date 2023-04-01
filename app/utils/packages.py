"""
necessary packages
"""
import os, sys
# import tqdm
import numpy, itertools, random
import asyncio
import csv, json
# from moneyed import Money
from datetime import datetime, date, time, timedelta
from math import ceil, floor
from dataclasses import dataclass, field, KW_ONLY, replace
from uuid import UUID, uuid4
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
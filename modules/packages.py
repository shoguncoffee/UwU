"""
necessary packages
"""
import os, sys
import tqdm
import numpy, itertools
import asyncio
import csv, json
from moneyed import Money
from enum import Enum
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
    Sequence, 
    Optional,
    ClassVar
)
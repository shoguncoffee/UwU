"""
necessary packages
"""
import os, sys
#import tqdm
import numpy, itertools
import asyncio
import rapidfuzz
import csv, json
#from moneyed import Money
from datetime import datetime, date, time, timedelta
from dataclasses import dataclass, field
from types import ModuleType
from uuid import UUID, uuid4
from abc import ABC, abstractmethod
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
    Collection
)
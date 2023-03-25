"""
"""
from __future__ import annotations
from base import *

class Infomations:
    def __init__(self, *info: str):
        self.__info = info
    
    def add(self, *info: str):
        self.__info = *self.__info, *info
        
    def __str__(self):
        return '\n'.join(self.__info)
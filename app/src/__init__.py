r"""
all object templates in \src, though everything in python is already an object
"""
from typing import TYPE_CHECKING
if not TYPE_CHECKING:
    from os import listdir, path
    dir = listdir(
        path.dirname(__file__)
    )
    __all__ = [
        f.removesuffix('.py') for f in dir 
        if f.endswith('.py') and not f.startswith('_')
    ]
else:
    __all__ = ['a', 'b', 'c', 'flightsystem', 'constants', 'info']
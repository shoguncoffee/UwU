from os import listdir, path
from typing import TYPE_CHECKING

dir = listdir(path.dirname(__file__))
file = [
    f.removesuffix('.py') for f in dir 
    if f.endswith('.py') and not f.startswith('_')
]
if not TYPE_CHECKING:
    __all__ = file
else: 
    __all__ = [
        'aircraft'
    ]

if __name__ == '__main__':
    print(__all__)
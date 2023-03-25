"""
fancy variables and functions
"""
from __future__ import annotations
#from utils.checking import *
from utils.packages import *

if TYPE_CHECKING:
    ...
else:
    dataclass = dataclass(slots=True)


if __name__ == '__main__':
    print()
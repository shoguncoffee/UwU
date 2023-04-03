r"""
interface of main package (UwU/app)

for this package:
- `\UwU> python -m app`


for individual submodule in this package:
- ``\UwU> python -m app.<module>`
"""

import pickle
from .system import *


path = 'app/data/...'

with open(path, 'rb') as f:
    airline = pickle.load(f)

# 
from app import api
    
with open(path, 'wb') as f:
    pickle.dump(airline, f)
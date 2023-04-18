r"""
interface of main package (UwU/app)

for this package:
- `\UwU> python -m app`


for individual submodule in this package:
- `\UwU> python -m app.<module>`
"""

from multiprocessing import Process
from .system import *
import uvicorn
import pickle


if 0:
    path = 'app/data/...'

    with open(path, 'rb') as f:
        airline = pickle.load(f)


    with open(path, 'wb') as f:
        pickle.dump(airline, f)
        
    # python -m uvicorn app.api:app --reload    
    os.system('python3 -m app.api')
    os.system('python3 -m app.interface')
    

Process(target=lambda: uvicorn.run('app.api:web', reload=True)).start()
Process(target=lambda: __import__('app.interface')).start()
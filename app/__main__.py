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
        
    os.system('python3.11 -m uvicorn app.api:web --reload')
    os.system('python3.11 -m app.interface')
    

Process(
    target=uvicorn.run, 
    args=('app.api:web',),
    kwargs={'reload': True}
).start()

Process(
    target=__import__, 
    args=('app.interface',)
).start()

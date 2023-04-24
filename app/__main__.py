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
    def run_server():
        Airline.load()            
        uvicorn.run('app.api:web', reload=True)
        
        
    def run_interface():
        import app.interface
    
    
    if __name__ == '__main__':
        for func in run_server, run_interface:
            Process(target=func).start()


Process(
    target=uvicorn.run, 
    args=('app.api:web',),
    kwargs={'reload': True}
).start()

Process(
    target=__import__, 
    args=('app.interface',)
).start()
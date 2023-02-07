"""
main
"""
from __future__ import annotations
from base import *
from objects import *


def importer():
    with open('data/default.json') as file:
        data: dict = json.load(file)
        
        

async def main():
    ...
    

if __name__ == '__main__':
    now = datetime.now()
    #asyncio.run(main())
    print(os.listdir())
    
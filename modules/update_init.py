"""
update "__all__" for all __init__.py file in directory
"""
from os import listdir, path

def f(name):
    with open(name, 'w') as file:
        dir = listdir()
        allpy = [f.removesuffix('.py') for f in dir 
            if f.endswith('.py') and not f.startswith('_')
        ]
        file.writelines(allpy)

dirname = path.dirname(__file__)
...
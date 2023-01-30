def version():
    from sys import version_info
    if version_info <= (3, 11):
        return 'required python >= 3.11'


def module():
    with open('requirements') as file:
        for module in file:
            try: 
                name, *version = module.split('==')
                version = version or False
                __import__(name)
            except:
                return 'please install requirements file'

def directory():
    from os import getcwd
    *_, dir = getcwd().split('/')
    return dir == 'UwU' or ...


def main():
    ...

def __getattr__(name: str):
    globals.__get__(name)()

if __name__ != '__main__':
    for func in vars(__import__('checking')).values():
        if callable(func) and (error := func()):
            raise Exception(error)
        
        
else:
    for func in list(globals().values()):
        if callable(func):
            print(func)
    print(directory())
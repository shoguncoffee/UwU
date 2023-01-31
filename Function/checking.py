def version():
    from sys import version_info
    if version_info <= (3, 11):
        return 'required python >= 3.11'


def module():
    with open('requirements') as file:
        for module in file:
            name, *version = module.split('==')
            try: 
                version = version or False
                __import__(name)
            except:
                return f'please install requirements file: {name}'

def directory():
    from os import getcwd
    *_, dir = getcwd().split('/')
    return dir == 'UwU' or ...


###################################################################

def __name(name: str):
    return f'!{name}'

def __filter():
    return [
        n for n, v in globals().items() 
        if callable(v) and not n.startswith('_')
    ]

def __main():
    var = globals()
    new = {
        __name(n): var.pop(n) for n in __filter()
    }
    var.update(new)
    
def __warp(func_name: str):
    def new():
        func = globals()[__name(func_name)]
        if (error := func()):
            raise Exception(error)
        
        print(f'check {func_name}: PASS')
    return new
        
def __getattr__(name: str):
    match name:
        case '__path__':
            pass
        case '__all__':
            for func in __all__:
                __warp(func)()
            return __all__
        case _:
            (func := __warp(name))()
            return func

if __name__ != '__main__': 
    __all__ = __filter() # type: ignore
    __main()
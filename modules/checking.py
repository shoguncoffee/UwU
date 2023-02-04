"""
contains functions intended to use immediately when importing occur
*you may be surprised by my amazing trick
"""
def version():
    from sys import version_info
    if version_info <= (3, 11):
        return 'required python >= 3.11'


def module():
    with open('requirements') as file:
        for module in file:
            name, *version = module.split('==')
            try: __import__(name.removesuffix('\n'))
            except:
                return f'please install requirements file: {name}'


def directory():
    from os import getcwd
    *_, dir = getcwd().split('/')
    if dir != 'UwU':
        return 'please run from correct directory'


def __main():
    label = lambda name: f'!{name}'
    var = globals()
    all = [
        n for n, v in var.items() 
        if callable(v) and not n.startswith('_')
    ]
    
    def warp(func_name: str):
        def new():
            func = var[label(func_name)]
            assert not (error := func()), error
            print(f'check {func_name}: PASS')
        return new

    def getattr(name: str):
        match name:
            case '__path__':
                pass
            case '__all__':
                for func in all:
                    warp(func)()
                return all
            case _:
                (func := warp(name))()
                return func

    new = {
        label(n): var.pop(n) for n in all
    }
    var.update(new, 
        __all__ = all, 
        __getattr__ = getattr
    )
        
__main()
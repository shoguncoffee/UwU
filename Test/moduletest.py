deprecated_names = ["old_function"]

def qwe(): print(999)

def __getattr__(name):
    print(name)
    if name in deprecated_names:
        print('warn')
        return 10
    #raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
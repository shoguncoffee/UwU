def qwe(): print(999)

def __getattr__(name: str):
    print(name)
    if not name.startswith('_'):
        return globals()[f'?{name}']

for name in list(globals()):
    if not name.startswith('_'):
        globals()[f'?{name}'] = globals().pop(name)
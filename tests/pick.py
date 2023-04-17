import pickle

class a:
    def __new__(cls, *a):
        ins =  super().__new__(cls)
        print('__new__', ins)
        return ins
        
    def __init__(self, k):
        print('__init__', self)
        self.q = k

x = a(10)
with open("tests/pick.txt", "wb") as f:
    pickle.dump(x, f)

print('dump')

with open("tests/pick.txt", "rb") as f:
    x2 = pickle.load(f)
    
print(x2)
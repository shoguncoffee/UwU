def my_generator0(n):
    for i in range(n):
        yield i
        if i >= 5:
            return

def my_generator1(n):
    for i in range(n):
        yield i
        if i >= 5:
            raise StopIteration
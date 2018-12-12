from funcy import autocurry, partial, flatten

# @autocurry
def method(n, x):
    if True:
        yield (x for x in range(20))
        yield (x for x in range(20, 30))


# This gets a TypeError: functools.partial object not iterable
print(list(flatten(partial(method, 10)(10))))

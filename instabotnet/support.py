class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__




def merge(a, b):
    result = dict(**a)

    [result.update({x: dict(**a[x], **b[x])}) for x in set(a.keys()) & set(b.keys())
        if isinstance(a[x], dict) and isinstance(b[x], dict)]

    [result.update({x: [*a[x], *b[x]]}) for x in set(a.keys()) & set(b.keys())
        if isinstance(a[x], list) and isinstance(b[x], list)]

    [result.update({x: a[x] if x in a else b[x]}) for x in set(a.keys()) ^ set(b.keys() )]

    return result

if __name__ == '__main__':
    x = merge(
        dict(
            a=dict(b=[3,4]),
            b=[5,4,6]
        ),
        dict(
            a=dict(c=[9]),
            b=[1]
        )
    )
    print(x)

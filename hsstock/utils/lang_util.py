from functools import wraps

def coroutine(func):
    """
    装饰器：向前执行到第一个`yield`表达式，预激`func`
    :param func:
    :return:
    """
    @wraps(func)
    def primer(*args, **kwargs):
        gen = func(*args,**kwargs)
        next(gen)
        return gen
    return primer

def create_factory(cls_name, field_names):
    try:
        field_names = field_names.replace(',', ' ').split()  # <1>
    except AttributeError:  # no .replace or .split
        pass  # assume it's already a sequence of identifiers
    field_names = tuple(field_names)  # <2>

    def __init__(self, *args, **kwargs):  # <3>
        attrs = dict(zip(self.__slots__, args))
        attrs.update(kwargs)
        for name, value in attrs.items():
            setattr(self, name, value)

    def __iter__(self):  # <4>
        for name in self.__slots__:
            yield getattr(self, name)

    def __repr__(self):  # <5>
        values = ', '.join('{}={!r}'.format(*i) for i
                           in zip(self.__slots__, self))
        return '{}({})'.format(self.__class__.__name__, values)

    cls_attrs = dict(__slots__ = field_names,  # <6>
                     __init__  = __init__,
                     __iter__  = __iter__,
                     __repr__  = __repr__)

    return type(cls_name, (object,), cls_attrs)  # <7>


if __name__ == '__main__':
    Dog = create_factory('Dog', ['name', 'weight', 'owner'])
    d1 = Dog('wc',80,'hujb')
    print(d1,d1.name, d1.weight, d1.owner)

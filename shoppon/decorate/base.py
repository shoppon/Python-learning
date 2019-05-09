import functools
import inspect


def base(func):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        func(args, kwargs)

    return wrap


class Bar(object):
    @base
    def foo(self, a, b, c):
        print('foo')


print(inspect.getargspec(Bar.foo))

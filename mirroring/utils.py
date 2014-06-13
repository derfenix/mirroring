# -*- coding: utf-8 -*-
"""
.. module: utils
    :symopsis: 

.. moduleauthor:: derfenix <derfenix@gmail.com>
"""


# noinspection PyPep8Naming
class cached_property(object):
    def __init__(self, func):
        self.func = func
        self.name = func.__name__

    def __get__(self, instance, cls=None):
        if self.name not in instance.__dict__:
            result = instance.__dict__[self.name] = self.func(instance)
            return result
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]
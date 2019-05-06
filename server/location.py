#! /usr/bin/python
from __future__ import with_statement, print_function, unicode_literals
#from builtins import input
from builtins import str
from builtins import map
import sys
sys.py3kwarning = True  #Turn on Python 3 warnings
#import future_builtins

class Location(tuple):
    '''A tuple which holds an x,y location.  Changes + and - to make sense

    Acts like tuples except that it is constrained to 2 integer elements and
    location.x returns the first element and location.y returns the second.
    Also, addition and subtraction work differently.  Instead of appending
    new items on the end, addition lets you add the coordinates of two
    locations where the return value is (x, y) where the x is x1+x2 and
    the y is y1+y2, etc.

    >>> loc = Location((1, 2))
    >>> loc2 = Location((5, 20))
    >>> str(loc)
    '(1, 2)'
    >>> repr(loc)
    'Location((1, 2))'
    >>> loc3 = loc + loc2
    >>> str(loc3)
    '(6, 22)'
    >>> loc2 + (100, 300)
    Location((105, 320))
    >>> (100, 300) + loc2
    Location((105, 320))
    >>> loc - loc2
    Location((-4, -18))
    >>> loc2 - loc
    Location((4, 18))
    >>> loc2.x
    5
    >>> loc.y
    2
    >>> loc2.col
    5
    >>> loc.row
    2
    >>> loc2_dup = Location((5, 20))
    >>> hash(loc2) == hash(loc2_dup)
    True
    >>> loc = Location((1,))
    Traceback (most recent call last):
    ...
    TypeError: Locations must be initialized with a tuple having exactly 2 integer elements
    >>> loc = Location((1, 3.5))
    Traceback (most recent call last):
    ...
    TypeError: Locations must be initialized with a tuple having exactly 2 integer elements

    '''
    def __new__(cls, in_tuple):    #python knows that __new__ is always a classmethod
        if ((not isinstance(in_tuple, tuple)) or (len(in_tuple) != 2) or \
           (not isinstance(in_tuple[0], int)) or (not isinstance(in_tuple[1], int))):
            raise TypeError("Locations must be initialized with"\
                            " a tuple having exactly 2 integer elements")
        return super(cls, Location).__new__(cls, in_tuple)

    def __init__(self, in_tuple):
        pass

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def col(self):
        return self[0]

    @property
    def row(self):
        return self[1]

    def __add__(self, other):
        '''Implements "me + x"'''
        if len(other) != 2:
            raise TypeError("Invalid item added to Location")
        return Location(tuple(map(lambda a, b: a+b, self, other)))

    def __sub__(self, other):
        '''Implements "me - x"'''
        if len(other) != 2:
            raise TypeError("Invalid item in Location subtraction")
        return Location(tuple(map(lambda a, b: a-b, self, other)))

    def __mul__(self, other):
        '''Implements "me * x" -- really only useful for multiplying vectors'''
        if len(other) != 2:
            raise TypeError("Invalid item in Location multiplication")
        return Location(tuple(map(lambda a, b: a*b, self, other)))

    def __rmul__(self, other):
        '''Implements "x * me" -- really only useful for multiplying vectors'''
        if len(other) != 2:
            raise TypeError("Invalid item in Location multiplication")
        return Location(tuple(map(lambda a, b: a*b, other, self)))

    def __radd__(self, other):
        '''Implements "x + me"'''
        if len(other) != 2:
            raise TypeError("Invalid item added to Location")
        return Location(tuple(map(lambda a, b: a+b, other, self)))

    def __rsub__(self, other):
        '''Implements "x - me"'''
        if len(other) != 2:
            raise TypeError("Invalid item in Location subtraction")
        return Location(tuple(map(lambda a, b: a-b, other, self)))

    def __repr__(self):
        return "Location(({loc[0]}, {loc[1]}))".format(loc=self)

    def __str__(self):
        # I think I could just inherit tuple's __str__ here rather than
        # defining this redundant formula.  That's the approach I took for
        # __format__
        return str(tuple((self[0], self[1])))

    def __hash__(self):
        '''Make sure two Location objects pointing to same location hash to
        the same value.  This enables me to be hashable and used where
        immutable types can be used'''
        # I believe making __hash__ behave this way is what allows this class
        # to be immutable (i.e. because it is hashable)
        return hash(tuple((self[0], self[1])))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    #input('press return to exit')

# -*- coding: utf-8 -*-

"""ScarlettOS compatibility."""

from __future__ import absolute_import, unicode_literals


import sys

# from six.moves import configparser

# PY2 = sys.version_info[0] == 2
# PY3 = not PY2

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


if PY2:
    pass
elif PY3:
    import os
    import random  # noqa
    import re
    import unicodedata
    import threading

    # NOTE: from mopidy
    import configparser  # noqa
    import queue  # noqa

    import subprocess  # noqa

    map = itertools.imap if sys.version_info < (3,) else map

    import errno
    from os import environ as environ
    import pprint
    pp = pprint.PrettyPrinter(indent=4)

    # from scarlett_os.internal import debugger

    import builtins
    builtins
    import urllib  # noqa
    from urllib.parse import urlparse, urlunparse, quote_plus, unquote_plus, \
        urlsplit, parse_qs, urlencode, quote, unquote
    urlparse, quote_plus, unquote_plus, urlunparse, urlsplit, parse_qs, \
        urlencode, quote, unquote
    from urllib.request import pathname2url, url2pathname
    pathname2url, url2pathname
    from urllib.request import urlopen, build_opener
    urlopen, build_opener
    from io import BytesIO as cBytesIO
    cBytesIO
    from io import StringIO
    StringIO = StringIO
    from functools import reduce, wraps
    reduce
    from operator import floordiv
    floordiv
    from itertools import zip_longest as izip_longest
    izip_longest
    import codecs

    import contextlib
    import time
    import textwrap  # noqa
    # import logging
    # from functools import reduce, wraps
    import traceback

    # logger = logging.getLogger(__name__)

    # reduce
    from operator import floordiv
    floordiv

    xrange = range
    long = int
    unichr = chr
    cmp = lambda a, b: (a > b) - (a < b)
    izip = zip

    getbyte = lambda b, i: b[i:i + 1]
    iterbytes = lambda b: (bytes([v]) for v in b)

    text_type = str
    string_types = (str,)
    integer_types = (int,)
    number_types = (int, float)
    # NOTE: why does anaconda do this below
    # NUMERIC_TYPES = tuple(list(INT_TYPES) + [float, complex])

    # NOTE: From https://github.com/mopidy/mopidy/blob/develop/mopidy/compat.py
    input = input
    intern = sys.intern

    # NOTE: everything else missing
    # http://nipy.org/dipy/devel/python3.html
    iteritems = lambda d: iter(d.items())
    itervalues = lambda d: iter(d.values())
    iterkeys = lambda d: iter(d.keys())
    listitems = lambda d: list(d.items())
    listkeys = lambda d: list(d.keys())
    listvalues = lambda d: list(d.values())

    listfilter = lambda *x: list(filter(*x))
    listmap = lambda *x: list(map(*x))

    # def itervalues(dct, **kwargs):
    #     return iter(dct.values(**kwargs))

    import builtins
    exec_ = getattr(builtins, "exec")

    def reraise(tp, value, tb):
        raise tp(value).with_traceback(tb)

    def swap_to_string(cls):
        return cls

    escape_decode = lambda b: codecs.escape_decode(b)[0]

    _FSCODING = "utf-8"


# taken from six
def add_metaclass(metaclass):
    """Class decorator for creating a class with a metaclass."""

    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        slots = orig_vars.get('__slots__')
        if slots is not None:
            if isinstance(slots, str):
                slots = [slots]
            for slots_var in slots:
                orig_vars.pop(slots_var)
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        return metaclass(cls.__name__, cls.__bases__, orig_vars)
    return wrapper

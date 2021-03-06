#-*- coding:utf-8 -*-

import pytest

import time
import random
import calendar
import datetime as dt

from spiceminer.time_ import Time


def values():
    def error(value, expected):
        return pytest.mark.xfail(raises=ValueError)((value, expected))

    ### Out of bounds
    # year
    yield error({'year': 0}, None)
    yield error({'year': 10000}, None)
    # month
    yield error({'month': 0}, None)
    yield error({'month': 13}, None)
    # day
    yield error({'day': 0}, None)
    yield error({'day': 32}, None)
    yield error({'month': 2, 'day': 29}, None)
    yield error({'month': 4, 'day': 31}, None)
    # hour
    yield error({'hour': -1}, None)
    yield error({'hour': 24}, None)
    # minute
    yield error({'minute': -1}, None)
    yield error({'minute': 60}, None)
    # second
    yield error({'second': -0.1}, None)
    yield error({'second': 60}, None)

    ### In bounds
    #year
    yield {'year': 1}, -62135596800.0
    yield {'year': 9999}, 253370764800.0
    # month
    yield {'month': 1}, 0.0
    yield {'month': 12}, 28857600.0
    # day
    yield {'day': 1}, 0.0
    yield {'day': 31}, 2592000.0
    # hour
    yield {'hour': 0}, 0.0
    yield {'hour': 23}, 82800.0
    # minute
    yield {'minute': 0}, 0.0
    yield {'minute': 59}, 3540.0
    # second
    yield {'second': 0}, 0.0
    yield {'second': 59.9}, 59.9

    ### Misc
    yield {}, 0.0
    for i in range(10):
        values = {'year': random.randint(1, 9999),
                'month': random.randint(1, 12),
                'day': random.randint(1, 28),
                'hour': random.randint(1, 23),
                'minute': random.randint(1, 59)}
        expected = calendar.timegm(dt.datetime(**values).timetuple())
        yield values, expected

def type_check():
    error = pytest.mark.xfail(raises=TypeError)

    types = [0.1, 1+5j, '1', None]
    for t in types:
        for field in ('year', 'month', 'day', 'hour', 'minute'):
            yield error({field: t})
    for t in types[1:]:
        yield error({'second': t})
    yield {'second': 0.1}

### Contructors ###
@pytest.mark.parametrize('args,expected', values())
def test_constructor_values(args, expected):
    assert Time(**args) == expected

@pytest.mark.parametrize('args', type_check())
def test_constructor_types(args):
    assert Time(**args)


def gen_fromposix():
    yield pytest.mark.xfail(raises=TypeError)([1+2j, None])
    # blackbox
    for i in range(8):
        posix = random.randint(-62135596800, 253370764800)
        yield posix, time.gmtime(posix)[:6]

@pytest.mark.parametrize('posix, args', gen_fromposix())
def test_clsmeth_fromposix(posix, args):
    assert Time.fromposix(posix) == Time(*args)


def gen_fromydoy():
    xfail_T = pytest.mark.xfail(raises=TypeError)
    xfail_V = pytest.mark.xfail(raises=ValueError)
    yield xfail_T(([None, 200], None))
    # day out of bounds
    yield xfail_V(([2000, -0.1], None))
    yield xfail_V(([2000, 366], None))
    yield xfail_V(([2001, 365], None))
    # day in bounds
    yield ([2000, 0], [2000])
    yield ([2000, 365 + (Time.DAY - 1.0) / Time.DAY], [2000, 12, 31, 23, 59, 59])
    yield ([2001, 364 + (Time.DAY - 1.0)  / Time.DAY], [2001, 12, 31, 23, 59, 59])
    # blackbox
    for i in range(8):
        posix = random.randint(-62135596800, 253370764799) + random.random()
        gm = time.gmtime(posix)
        ydoy = (gm[0], (gm[3] * Time.HOUR + gm[4] * Time.MINUTE + gm[5] + (posix - int(posix))) / Time.DAY + (gm[7] - 1))
        args = list(gm[:6])
        args[-1] += (posix - int(posix))
        yield ydoy, args

@pytest.mark.parametrize('ydoy,args', gen_fromydoy())
def test_clsmeth_fromydoy(ydoy, args):
    assert Time.fromydoy(*ydoy) == Time(*args)


def gen_fromdatetime():
    # blackbox
    for i in range(8):
        year = random.randint(1, 9999)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        hour = random.randint(1, 23)
        minute = random.randint(1, 59)
        second = random.randint(1, 59)
        msec = random.random()
        arg = dt.datetime(year, month, day, hour, minute, second) + dt.timedelta(0, msec)
        expected = [year, month, day, hour, minute, second + msec]
        yield arg, expected

@pytest.mark.parametrize('arg,expected', gen_fromdatetime())
def test_clsmeth_fromdatetime(arg, expected):
    diff = 10e-5
    expected = Time(*expected)
    assert (expected - diff) < Time.fromdatetime(arg) < (expected + diff)


### Comparisons ###
def gen_eq():
    for comp in [Time(), float(Time()), dt.datetime(1970, 1, 1), dt.date(1970, 1, 1)]:
        yield {}, comp

@pytest.mark.parametrize('args,comp', gen_eq())
def test_eq(args, comp):
    assert Time(**args) == comp

@pytest.mark.parametrize('args,comp', (({'year': 1969}, comp) for _, comp in gen_eq()))
def test_eq(args, comp):
    assert Time(**args) < comp

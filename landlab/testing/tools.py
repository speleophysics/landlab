import os
import shutil
import tempfile

from nose.tools import assert_true, assert_equal


class cd(object):
    def __init__(self, dir):
        self._dir = dir

    def __enter__(self):
        self._starting_dir = os.path.abspath(os.getcwd())
        if not os.path.isdir(self._dir):
            mkpath(self._dir)
        os.chdir(self._dir)
        return os.path.abspath(os.getcwd())

    def __exit__(self, type, value, traceback):
        os.chdir(self._starting_dir)


class cdtemp(object):
    def __init__(self, **kwds):
        self._kwds = kwds
        self._tmp_dir = None

    def __enter__(self):
        self._starting_dir = os.path.abspath(os.getcwd())
        self._tmp_dir = tempfile.mkdtemp(**self._kwds)
        os.chdir(self._tmp_dir)
        return os.path.abspath(self._tmp_dir)

    def __exit__(self, type, value, traceback):
        os.chdir(self._starting_dir)
        shutil.rmtree(self._tmp_dir)


def assert_is(expr1, expr2, msg=None):
    assert_true(expr1 is expr2, msg=msg)


def assert_is_not(expr1, expr2, msg=None):
    assert_true(expr1 is not expr2, msg=msg)


def assert_is_none(expr, msg=None):
    assert_true(expr is None, msg=msg)


def assert_is_not_none(expr, msg=None):
    assert_true(expr is not None, msg=msg)


def assert_in(first, second, msg=None):
    assert_true(first in second, msg=msg)


def assert_is_not_in(first, second, msg=None):
    assert_true(first not in second, msg=msg)


def assert_is_not(expr1, expr2, msg=None):
    assert_true(expr1 is not expr2, msg=msg)


def assert_is_instance(obj, cls, msg=None):
    assert_true(isinstance(obj, cls), msg=msg)


def assert_not_is_instance(obj, cls, msg=None):
    assert_true(not isinstance(obj, cls), msg=msg)


def assert_list_equal(list1, list2, msg=None):
    assert_true(isinstance(list1, list))
    assert_true(isinstance(list2, list))
    for a, b in zip(list1, list2):
        assert_equal(a, b)


def assert_tuple_equal(tuple1, tuple2, msg=None):
    assert_true(isinstance(tuple1, tuple))
    assert_true(isinstance(tuple1, tuple))
    for a, b in zip(tuple1, tuple2):
        assert_equal(a, b)


def assert_dict_equal(dict1, dict2, msg=None):
    assert_true(isinstance(dict1, dict))
    assert_true(isinstance(dict2, dict))
    assert_equal(dict1, dict2)


def assert_set_equal(set1, set2, msg=None):
    assert_true(isinstance(set1, set))
    assert_true(isinstance(set2, set))
    assert_equal(set1, set2)

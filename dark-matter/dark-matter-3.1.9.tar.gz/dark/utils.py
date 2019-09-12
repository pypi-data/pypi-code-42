from __future__ import division

import os
import string
import six
import bz2
import gzip
from os.path import basename
from contextlib import contextmanager
from re import compile
import numpy as np


def numericallySortFilenames(names):
    """
    Sort (ascending) a list of file names by their numerical prefixes.
    The number sorted on is the numeric prefix of the basename of
    the given filename. E.g., '../output/1.json.bz2' will sort before
    '../output/10.json.bz2'.

    @param: A C{list} of file names, each of whose basename starts with a
        string of digits.
    @return: The sorted C{list} of full file names.
    """

    def numericPrefix(name):
        """
        Find any numeric prefix of C{name} and return it as an C{int}.

        @param: A C{str} file name, whose name possibly starts with digits.
        @return: The C{int} number at the start of the name, else 0 if
            there are no leading digits in the name.
        """
        count = 0
        for ch in name:
            if ch in string.digits:
                count += 1
            else:
                break
        return 0 if count == 0 else int(name[0:count])

    return sorted(names, key=lambda name: numericPrefix(basename(name)))


# Set up a median function that works on different Python versions and on pypy
# (even if numpypy is still broken).
#
# First try numpy, and check that an ndarray has a partition method (to avoid a
# shortcoming in pypy numpy, see
# https://bitbucket.org/pypy/numpy/issues/12/median-calling-ndarraypartition
# If numpy seems ok, use it. Else try for the Python 3.4 median function, else
# write our own.

_a = np.array([1])

try:
    _a.partition
except AttributeError:
    # Cannot use numpy. Try for the new (Python 3.4) built-in function.
    try:
        from statistics import median as _median
    except ImportError:
        def _median(numbers):
            """
            Find the median of a set of numbers.

            @param numbers: A C{list} of numeric values.
            @return: The median value in C{numbers}.
            """
            numbers = sorted(numbers)
            n = len(numbers)
            if n % 2:
                return numbers[n // 2]
            else:
                n //= 2
                return (numbers[n - 1] + numbers[n]) / 2
else:
    # We have a working numpy. Just make sure we raise on an empty list as
    # numpy returns numpy.nan
    _median = np.median

del _a


def median(l):
    """
    Find the median of a set of numbers.

    @param l: A C{list} of numeric values.
    @raise ValueError: If C{l} is empty.
    @return: The median value in C{l}.
    """

    # Handle the zero length case ahead of time because various median
    # implementations do different things. numpy returns nan, whereas Python
    # 3.4 and later raise StatisticsError

    if len(l) == 0:
        # Match the empty-argument exception message of Python's built-in max
        # and min functions.
        raise ValueError('arg is an empty sequence')
    else:
        return _median(l)


@contextmanager
def asHandle(fileNameOrHandle, mode='rt', encoding='UTF-8'):
    """
    Decorator for file opening that makes it easy to open compressed files
    and which can be passed an already-open file handle or a file name.
    Based on L{Bio.File.as_handle}.

    @param fileNameOrHandle: Either a C{str} or a file handle.
    @param mode: The C{str} mode to use for opening the file.
    @param encoding: The C{str} encoding to use when opening the file.
    @return: A generator that can be turned into a context manager via
        L{contextlib.contextmanager}.
    """
    if isinstance(fileNameOrHandle, six.string_types):
        if fileNameOrHandle.endswith('.gz'):
            if six.PY3:
                yield gzip.open(fileNameOrHandle, mode=mode, encoding=encoding)
            else:
                yield gzip.GzipFile(fileNameOrHandle, mode=mode)
        elif fileNameOrHandle.endswith('.bz2'):
            if six.PY3:
                yield bz2.open(fileNameOrHandle, mode=mode, encoding=encoding)
            else:
                yield bz2.BZ2File(fileNameOrHandle, mode=mode)
        else:
            # Putting mode=mode, encoding=encoding into the following
            # causes a hard-to-understand error from the mocking library.
            with open(fileNameOrHandle) as fp:
                yield fp
    else:
        yield fileNameOrHandle


_rangeRegex = compile(r'^\s*(\d+)(?:\s*-\s*(\d+))?\s*$')


def parseRangeString(s, convertToZeroBased=False):
    """
    Parse a range string of the form 1-5,12,100-200.

    @param s: A C{str} specifiying a set of numbers, given in the form of
        comma separated numeric ranges or individual indices.
    @param convertToZeroBased: If C{True} all indices will have one
        subtracted from them.
    @return: A C{set} of all C{int}s in the specified set.
    """

    result = set()
    for _range in s.split(','):
        match = _rangeRegex.match(_range)
        if match:
            start, end = match.groups()
            start = int(start)
            if end is None:
                end = start
            else:
                end = int(end)
            if start > end:
                start, end = end, start
            if convertToZeroBased:
                result.update(range(start - 1, end))
            else:
                result.update(range(start, end + 1))
        else:
            raise ValueError(
                'Illegal range %r. Ranges must single numbers or '
                'number-number.' % _range)

    return result


if six.PY3:
    from six import StringIO
else:
    from six import StringIO as sixStringIO

    class StringIO(sixStringIO):
        """
        A StringIO class that can be used as a context manager, seeing as the
        six.StringIO class does not provide __enter__ and __exit__ methods
        under Python 2.
        """
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.close()
            return False


def baseCountsToStr(counts):
    """
    Convert base counts to a string.

    @param counts: A C{Counter} instance.
    @return: A C{str} representation of nucleotide counts at an offset.
    """
    return ' '.join([
        ('%s:%d' % (base, counts[base])) for base in sorted(counts)])


def nucleotidesToStr(nucleotides, prefix=''):
    """
    Convert offsets and base counts to a string.

    @param nucleotides: A C{defaultdict(Counter)} instance, keyed
        by C{int} offset, with nucleotides keying the Counters.
    @param prefix: A C{str} to put at the start of each line.
    @return: A C{str} representation of the offsets and nucleotide
        counts for each.
    """
    result = []
    for offset in sorted(nucleotides):
        result.append(
            '%s%d: %s' % (prefix, offset,
                          baseCountsToStr(nucleotides[offset])))
    return '\n'.join(result)


def countPrint(mesg, count, len1, len2=None):
    """
    Format a message followed by an integer count and a percentage (or
    two, if the sequence lengths are unequal).

    @param mesg: a C{str} message.
    @param count: a numeric value.
    @param len1: the C{int} length of sequence 1.
    @param len2: the C{int} length of sequence 2. If C{None}, will
        default to C{len1}.
    @return: A C{str} for printing.
    """
    def percentage(a, b):
        """
        What percent of a is b?

        @param a: a numeric value.
        @param b: a numeric value.
        @return: the C{float} percentage.
        """
        return 100.0 * a / b if b else 0.0

    if count == 0:
        return '%s: %d' % (mesg, count)
    else:
        len2 = len2 or len1
        if len1 == len2:
            return '%s: %d/%d (%.2f%%)' % (
                mesg, count, len1, percentage(count, len1))
        else:
            return ('%s: %d/%d (%.2f%%) of sequence 1, '
                    '%d/%d (%.2f%%) of sequence 2' % (
                        mesg,
                        count, len1, percentage(count, len1),
                        count, len2, percentage(count, len2)))


@contextmanager
def cd(newdir):
    """
    Trivial context manager for temporarily switching directory.

    @param dir: A C{str} directory to cd to.
    """
    olddir = os.getcwd()
    try:
        os.chdir(newdir)
        yield newdir
    finally:
        os.chdir(olddir)

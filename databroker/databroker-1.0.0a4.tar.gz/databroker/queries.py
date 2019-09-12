"""
This module is experimental.
"""
import abc
import collections.abc

import tzlocal

from .utils import normalize_human_friendly_time


class Query(collections.abc.Mapping):
    """
    This represents a MongoDB query.
    
    MongoDB queries are typically encoded as simple dicts. This object supports
    the dict interface in a read-only fashion. Subclassses add a nice __repr__
    and mutable attributes from which the contents of the dict are derived.
    """
    @abc.abstractproperty
    def query(self):
        ...

    @abc.abstractproperty
    def kwargs(self):
        ...

    def __iter__(self):
        return iter(self.query)

    def __getitem__(self, key):
        return self.query[key]
    
    def __len__(self):
        return len(self.query)

    def replace(self, **kwargs):
        """
        Make a copy with parameters changed.
        """
        return type(self)(**{**self.kwargs, **kwargs})

    def __repr__(self):
        return (f"{type(self).__name__}("
                f"{', '.join(f'{k}={v}' for k, v in self.kwargs.items())})")


class TimeRange(Query):
    """
    A search query representing a time range.

    Parameters
    ----------
    since, until: dates gives as timestamp, datetime, or human-friendly string, optional
    timezone : string
        As in, 'US/Eastern'. If None is given, tzlocal is used.
    """
    def __init__(self, since=None, until=None, timezone=None):
        if timezone is None:
            timezone = tzlocal.get_localzone().zone
        self.timezone = timezone
        if since is None:
            self._since_normalized = None
        else:
            self._since_normalized = normalize_human_friendly_time(
                since, tz=self.timezone)
        self._since_raw = since
        if until is None:
            self._until_normalized = None
        else:
            self._until_normalized = normalize_human_friendly_time(
                until, tz=self.timezone)
        self._until_raw = until
        if since is not None and until is not None:
            if self._since_normalized > self._until_normalized:
                raise ValueError("since must not be greater than until.")

    @property
    def kwargs(self):
        return {'since': self._since_raw, 'until': self._until_raw}

    @property
    def query(self):
        query = {'time': {}}
        if self._since_normalized is not None:
            query['time']['$gte'] = self._since_normalized
        if self._until_normalized is not None:
            query['time']['$lt'] = self._until_normalized
        return query

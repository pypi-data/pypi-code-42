from __future__ import annotations

from piccolo.query.base import Query
from piccolo.querystring import QueryString


class Create(Query):
    """
    Creates a database table.
    """

    @property
    def querystring(self) -> QueryString:
        base = f'CREATE TABLE {self.table._meta.tablename}'
        columns = ', '.join(['{}' for i in self.table._meta.columns])
        query = f'{base} ({columns})'
        return QueryString(
            query,
            *[i.querystring for i in self.table._meta.columns]
        )

    def __str__(self) -> str:
        return self.querystring.__str__()

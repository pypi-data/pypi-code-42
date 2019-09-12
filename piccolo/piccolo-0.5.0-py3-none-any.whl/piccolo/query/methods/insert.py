from __future__ import annotations
import typing as t

from piccolo.query.base import Query
from piccolo.query.mixins import AddDelegate
from piccolo.querystring import QueryString

if t.TYPE_CHECKING:
    from piccolo.table import Table


class Insert(Query):
    def setup_delegates(self):
        self.add_delegate = AddDelegate()

    def add(self, *instances: Table) -> Insert:
        self.add_delegate.add(*instances, table_class=self.table)
        return self

    def run_callback(self, results):
        """
        Assign the ids of the created rows to the model instances.
        """
        for index, row in enumerate(results):
            self.add_delegate._add[index].id = row["id"]

    @property
    def sqlite_querystring(self) -> QueryString:
        base = f"INSERT INTO {self.table._meta.tablename}"
        columns = ",".join([i._meta.name for i in self.table._meta.columns])
        values = ",".join(["{}" for i in self.add_delegate._add])
        query = f"{base} ({columns}) VALUES {values}"
        return QueryString(
            query,
            *[i.querystring for i in self.add_delegate._add],
            query_type="insert",
        )

    @property
    def postgres_querystring(self) -> QueryString:
        base = f"INSERT INTO {self.table._meta.tablename}"
        columns = ",".join([i._meta.name for i in self.table._meta.columns])
        values = ",".join(["{}" for i in self.add_delegate._add])
        query = f"{base} ({columns}) VALUES {values} RETURNING id"
        return QueryString(
            query,
            *[i.querystring for i in self.add_delegate._add],
            query_type="insert",
        )

from sqlalchemy import (
    Column, ForeignKey, Index,
    Integer, Float,
    Text, String, Unicode,
    Boolean,
    DateTime,
    LargeBinary,
    func,
    )
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref,
    )

from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.types import TypeDecorator, TEXT
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.dialects import postgresql
import json


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


@compiles(postgresql.HSTORE, "sqlite")
def compile_hstore_sqlite(type_, compiler, **kw):
    return "TEXT"


class JSONEncodedDict(TypeDecorator):
    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


#Index('my_index', MyModel.name, unique=True, mysql_length=255)

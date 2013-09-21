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

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


from sqlalchemy.ext.compiler import compiles
from sqlalchemy.dialects import postgresql


@compiles(postgresql.HSTORE, "sqlite")
def compile_hstore_sqlite(type_, compiler, **kw):
    return "TEXT"


#Index('my_index', MyModel.name, unique=True, mysql_length=255)
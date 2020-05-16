from sqlalchemy import Column
from sqlalchemy import Integer


def upgrade(migrate_engine):
    int_col = Column(Integer)
    int_col.create()

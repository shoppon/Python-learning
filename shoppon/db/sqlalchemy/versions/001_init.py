from sqlalchemy import Integer
from sqlalchemy import Table

def upgrade(migrate_engine):
    Table('fake', Integer())
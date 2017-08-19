import pdb
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, CatalogItem


#engine = create_engine('sqlite:///catalogitem.db')
engine = create_engine('postgresql+psycopg2://catalog:logacat@localhost/itemcatalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

pdb.set_trace()

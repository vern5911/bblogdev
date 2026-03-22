from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:////bibleblog.sqlite3', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from model import Bblog
    Base.metadata.create_all(bind=engine)

#To define your models, just subclass the Base class that was created by 
#the code above. If you are wondering why we don’t have to care about threads 
#here (like we did in the SQLite3 example above with the g object): 
#that’s because SQLAlchemy does that for us already with the scoped_session.

#To use SQLAlchemy in a declarative way with your application, you just have 
#to put the following code into your application module. 
#Flask will automatically remove database sessions at the end of the request 
#or when the application shuts down:

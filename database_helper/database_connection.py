from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool


class DatabaseConnection:
    def __init__(self, db_url):
        self.db_url = db_url
        self.engine = None
        self.Session = None

    def connect(self):
        self.engine = create_engine(self.db_url)
        self.Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        if self.Session is None:
            raise Exception('Database connection has not been established.')
        return self.Session()

    def get_engine(self):
        if self.engine is None:
            raise Exception('Database connection has not been established.')
        return self.engine

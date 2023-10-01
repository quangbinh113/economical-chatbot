import time

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
from sqlalchemy import inspect, MetaData
from backend_ref.config.database.config import DatabaseConfig, with_config
from sqlalchemy import Column, Integer, String, DateTime, func, Float
from backend_ref.config import base
from backend_ref.repositories.models import history,thread

# time.sleep(4)

class DatabaseSession:
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.Sessions = []
        self.Models = []

    def Url(self) -> str:
        return self.config.Host

    def GetDatabaseInfo(self):
        pass

    def create_db_session(self):
        try:
            # postgresql://sykros:fqQ3nN4L@localhost:9011/streamlist
            DATABASE_URL = f'postgresql://{self.config.User}:{self.config.Password}@{self.config.Host}:{self.config.Port}/streamlist'
            # Create a SQLAlchemy engine
            engine = create_engine(DATABASE_URL,echo=True)
            # Attempt to connect to the database
            connection = engine.connect()
            # Create a session
            Session = sessionmaker(bind=engine)
            _session = Session()

            base.metadata.create_all(bind=engine)
            metadata = MetaData()
            # Reflect all the tables in the database
            metadata.reflect(bind=engine)
            inspector = inspect(engine)
            # Loop through the tables in the database and generate models dynamically
            for table_name, table in metadata.tables.items():
                print(table_name)
                # table_model = type(
                #     table_name.capitalize(),  # Use the table name as the class name
                #     (base,),
                #     # {
                #     #     '__tablename__': table_name,
                #     #     '__table__': table,
                #     #     'id': table.c.id  # Make sure to map primary key if it's named 'id'
                #     # }
                # )

            print("Connection to the database successful.")

            return _session
        except OperationalError as e:
            print(f"Error: {e}")
            return None


# @with_config(config=DatabaseConfig(Host='127.0.0.1', Port=9011, User='sykros', Password='fqQ3nN4L'))
# class MyDBSession(DatabaseSession):
#     pass


# session: DatabaseSession = MyDBSession()


session = DatabaseSession(config=DatabaseConfig(Host='127.0.0.1', Port=9011, User='sykros', Password='fqQ3nN4L')).create_db_session()

import time
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
from sqlalchemy import inspect, MetaData
from backend_ref.config.database.config import DatabaseConfig, with_config
from sqlalchemy import Column, Integer, String, DateTime, func, Float
from backend_ref.config import base
from backend_ref.repositories.models import history, thread


# time.sleep(4)

class DatabaseSession:
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.Sessions = []
        self.Models = []

    def url(self) -> str:
        return self.config.Host

    def get_database_info(self):
        try:
            # Create the engine and inspector
            DATABASE_URL = f'postgresql://{self.config.User}:{self.config.Password}@{self.config.Host}:{self.config.Port}/chat_bot'
            engine = create_engine(DATABASE_URL, echo=False)
            inspector = inspect(engine)

            # Get a list of table names in the database
            table_names = inspector.get_table_names()

            # Get information about each table
            table_info = {}
            for table_name in table_names:
                columns = inspector.get_columns(table_name)
                table_info[table_name] = {
                    'columns': [column['name'] for column in columns],
                    'primary_key': inspector.get_primary_keys(table_name),
                }

            # You can print or return the table information as per your needs
            print("Database Tables:")
            for table_name, info in table_info.items():
                print(f"Table: {table_name}")
                print(f"Columns: {', '.join(info['columns'])}")
                print(f"Primary Key: {', '.join(info['primary_key'])}")

            return table_info

        except OperationalError as e:
            print(f"Error: {e}")
            return None

    def create_db_session(self):
        try:
            # postgresql://sykros:fqQ3nN4L@localhost:9011/streamlist
            DATABASE_URL = f'postgresql://{self.config.User}:{self.config.Password}@{self.config.Host}:{self.config.Port}'
            # Create a SQLAlchemy engine
            engine = create_engine(DATABASE_URL, echo=False)  # echo để check log
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
                print(f'{table_name}' + " " + 'has created')
            print("Connection to the database successful.")
            return _session
        except OperationalError as e:
            print(f"Error: {e}")
            return None

    def get_db(self):
        DATABASE_URL = f'postgresql://{self.config.User}:{self.config.Password}@{self.config.Host}:{self.config.Port}/chat_bot'
        engine = create_engine(DATABASE_URL, echo=False)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base = declarative_base()
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

session = DatabaseSession(
        config=DatabaseConfig(Host='dbpostgres', Port=5432, User='david', Password='david')
    ).create_db_session()

# session = DatabaseSession(
#         config=DatabaseConfig(Host='127.0.0.1', Port=9000, User='david', Password='david')
#     )
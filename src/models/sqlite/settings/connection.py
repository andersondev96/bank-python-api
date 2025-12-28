# src/models/sqlite/settings/connection.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBConnectionHandler:

    def __init__(self, connection_string: str = "sqlite:///storage.db") -> None:
        self.__connection_string = connection_string
        self.__engine = None
        self.session = None

    def connection_to_db(self) -> None:
        if self.__engine is None:
            self.__engine = create_engine(self.__connection_string, echo=False)

    def get_engine(self):
        if self.__engine is None:
            self.connection_to_db()
        return self.__engine

    def __enter__(self):
        self.connection_to_db()
        session_maker = sessionmaker(bind=self.__engine)
        self.session = session_maker()
        return self

    def __exit__(self, exec_type, exec_val, exec_tb):
        if self.session:
            self.session.close()
            self.session = None

db_connection_handler = DBConnectionHandler()

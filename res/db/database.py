"""
Database module to handle the database configuration and session.
"""
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from .config import Config
from .models import Base


class Database:
    """
    Database class to handle the database configuration and session.
    """
    def __init__(self):
        """
        Initialize the database configuration and create an engine and session factory.
        """
        self.config = Config()
        self.engine = self._create_engine()
        self.session_factory = scoped_session(sessionmaker(bind=self.engine))

    def _create_engine(self):
        """
        Create and return the database engine.
        :return: SQLAlchemy engine
        """
        return create_engine(self.config.sqlalchemy_database_uri)

    def create_tables(self):
        """
        Create all tables in the database if they do not exist.
        """
        Base.metadata.create_all(self.engine)

    def get_new_session(self):
        """
        Create a new session and return it.
        :return: A new SQLAlchemy session
        """
        return self.session_factory()

    def close(self):
        """
        Close the database engine and remove session.
        """
        self.session_factory.remove()
        self.engine.dispose()

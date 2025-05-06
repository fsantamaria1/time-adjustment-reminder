"""
This module contains unit tests for the database module.
"""
import os
from unittest.mock import patch
import pytest
from res.db.database import Database


class TestDatabaseUnit:
    """
    Class to contain the unit tests for the Database class.
    """
    @pytest.fixture
    def db_instance(self):
        """
        Fixture to create a Database instance for testing.
        """
        with patch.dict(os.environ,  {
            'DB_SERVER': 'localhost',
            'DB_NAME': 'test_db',
            'DB_USERNAME': 'test_user',
            'DB_PASSWORD': 'test_password',
        }):
            return Database()

    def test_init(self, db_instance):
        """
        Test the __init__ method to ensure the engine and session_factory are initialized.
        """
        assert db_instance.engine is not None
        assert db_instance.session_factory is not None

    def test_create_engine(self, db_instance):
        """
        Test the _create_engine method to ensure it creates an engine with the correct URI.
        """
        assert db_instance.engine.url.drivername == "mssql+pyodbc"

    @patch('res.db.database.Base.metadata.create_all')
    def test_create_tables(self, mock_create_all, db_instance):
        """
        Test the create_tables method to ensure tables are created.
        """
        db_instance.create_tables()
        mock_create_all.assert_called_once_with(db_instance.engine)

    def test_get_new_session(self, db_instance):
        """
        Test the get_new_session method to ensure a new session is returned.
        """
        session = db_instance.get_new_session()
        assert session is not None

    @patch('res.db.database.scoped_session.remove')
    def test_close(self, mock_remove, db_instance):
        """
        Test the close method to ensure the engine and session are closed.
        """
        with patch.object(db_instance.engine, 'dispose', autospec=True) as mock_dispose:
            db_instance.close()
            mock_remove.assert_called_once()
            mock_dispose.assert_called_once()

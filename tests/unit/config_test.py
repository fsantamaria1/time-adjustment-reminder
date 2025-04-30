"""
Tests for the Config class in the database.config module.
"""
import urllib.parse
import pytest
from res.db.config import Config


class TestConfig:
    """
    Tests for the Config class.
    """

    @pytest.fixture(autouse=True)
    def setup_env(self, monkeypatch):
        """
        Fixture to set up environment variables and mocks for each test.
        """
        monkeypatch.setenv('DB_SERVER', 'test_server')
        monkeypatch.setenv('DB_USERNAME', 'test_user')
        monkeypatch.setenv('DB_PASSWORD', 'test_password')
        monkeypatch.setenv('DB_NAME', 'test_database')
        # Mock load_dotenv
        monkeypatch.setattr('dotenv.load_dotenv', lambda: None)

    @pytest.fixture()
    def valid_config(self):
        """
        Fixture to return a valid Config object.
        """
        return Config()

    def test_config_initialization(self, valid_config):
        """
        Test that the Config class initializes environment variables correctly.
        """
        assert valid_config.server == 'test_server'
        assert valid_config.username == 'test_user'
        assert valid_config.password == 'test_password'
        assert valid_config.database == 'test_database'

    def test_connection_string(self, valid_config):
        """
        Test that the connection string is constructed correctly.
        """
        expected_connection_string = (
            'DRIVER=ODBC Driver 17 for SQL Server;'
            'SERVER=test_server;DATABASE=test_database;UID=test_user;PWD=test_password;'
            'Encrypt=yes;TrustServerCertificate=yes;'
        )
        expected_uri = ('mssql+pyodbc:///?odbc_connect=' +
                        urllib.parse.quote_plus(expected_connection_string))
        assert valid_config.sqlalchemy_database_uri == expected_uri

    def test_str_method(self, valid_config):
        """
        Test the __str__ method of the Config class.
        """
        assert str(valid_config) == 'Config'

    @pytest.mark.parametrize("missing_var, expected_error", [
        ('DB_SERVER', 'Configuration variable DB_SERVER is not set'),
        ('DB_USERNAME', 'Configuration variable DB_USERNAME is not set'),
        ('DB_PASSWORD', 'Configuration variable DB_PASSWORD is not set'),
        ('DB_NAME', 'Configuration variable DB_NAME is not set')
    ])
    def test_validate_config_missing_vars(self, missing_var, expected_error, monkeypatch):
        """
        Test validation for missing environment variables.
        """
        monkeypatch.delenv(missing_var, raising=False)
        with pytest.raises(ValueError) as exc_info:
            Config()
        assert str(exc_info.value) == expected_error

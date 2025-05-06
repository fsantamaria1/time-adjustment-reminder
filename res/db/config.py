"""
This module contains the configuration class for the database connection.
"""
import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Configuration class for the database connection.
    """
    def __init__(self):
        self.server = os.getenv('DB_SERVER')
        self.username = os.getenv('DB_USERNAME')
        self.password = os.getenv('DB_PASSWORD')
        self.database = os.getenv('DB_NAME')
        self.validate_config()

        self.connection_string = (
            f'DRIVER=ODBC Driver 17 for SQL Server;'
            f'SERVER={self.server};'
            f'DATABASE={self.database};'
            f'UID={self.username};'
            f'PWD={self.password};'
            f'Encrypt=yes;TrustServerCertificate=yes;'
        )

        self.sqlalchemy_database_uri = ('mssql+pyodbc:///?odbc_connect=' +
                                        urllib.parse.quote_plus(self.connection_string))

    def validate_config(self):
        """
        Validate the configuration.
        :raises ValueError: If any of the required configuration variables are not set.
        """
        if not self.server:
            raise ValueError("Configuration variable DB_SERVER is not set")
        if not self.username:
            raise ValueError("Configuration variable DB_USERNAME is not set")
        if not self.password:
            raise ValueError("Configuration variable DB_PASSWORD is not set")
        if not self.database:
            raise ValueError("Configuration variable DB_NAME is not set")

    def __str__(self):
        return "Config"

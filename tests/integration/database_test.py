"""
This module contains integration tests for the Database class.
"""
import pytest
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, ProgrammingError, SQLAlchemyError
from res.db.database import Database


class TestDatabaseIntegration:
    """
    Test class for the Database class.
    """

    @pytest.fixture(scope="module")
    def db_instance(self):
        """
        Fixture to create a Database instance connected to MS SQL database.
        """
        db = Database()
        yield db
        db.close()

    @pytest.fixture(scope="module")
    def connection_successful(self, db_instance):
        """
        Test to ensure the database engine is connected.
        """
        with db_instance.get_new_session() as session:
            try:
                session.execute(text("SELECT 1"))
            except OperationalError as e:
                pytest.fail(f"OperationalError: Failed to execute SQL query: {e}")
            except ProgrammingError as e:
                pytest.fail(f"ProgrammingError: Failed to execute SQL query: {e}")
            except SQLAlchemyError as e:
                pytest.fail(f"SQLAlchemyError: An error occurred during SQL execution: {e}")

    @pytest.mark.usefixtures("connection_successful")
    def test_create_and_query_table(self, db_instance):
        """
        Test to create a table and query it to ensure basic database operations work.
        """
        with db_instance.get_new_session() as session:
            session.execute(text(
                "CREATE TABLE "
                "test_table_reminder_integration (id INT PRIMARY KEY, name NVARCHAR(50))"
            ))
            session.execute(
                text("INSERT INTO "
                     "test_table_reminder_integration (id, name) VALUES (1, 'Test')")
            )
            result = session.execute(
                text("SELECT name "
                     "FROM test_table_reminder_integration WHERE id=1")).fetchone()
            # Delete the table
            session.execute(text("DROP TABLE test_table_reminder_integration"))
            assert result[0] == 'Test'

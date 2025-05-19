"""
This module contains fixtures for the integration tests.

It provides fixtures for creating a database connection, managing database sessions, and generating
valid instances of Project, Phase, and Plan models with unique primary keys for testing purposes.
"""
import random
from datetime import date, datetime
import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import NoResultFound
from res.db.config import Config
from res.db.models import Employee, Timecard, DayEntry, PayPeriod


# Create a single engine for the entire test suite
engine = create_engine(Config().sqlalchemy_database_uri, echo=True)
# Bind the session to the engine
Session = sessionmaker(bind=engine)


def generate_unique_primary_key(model, pk_column, start=1000, end=999999):
    """Generate a random integer for the primary key and ensure it doesn't exist in the database."""
    while True:
        with Session(bind=engine) as session:
            random_pk = random.randint(start, end)  # Generate a random integer within the range
            try:
                # Try querying the database for an existing primary key
                session.query(model).filter(pk_column == random_pk).one()
            except NoResultFound:
                # If no result found, the primary key is unique
                return random_pk


def generate_unique_primary_key_str(model, pk_column, start=1000, end=999999):
    """Generate a random integer for the primary key and ensure it doesn't exist in the database."""
    while True:
        with Session(bind=engine) as session:
            # Generate a random integer within the range
            random_pk = str(random.randint(start, end))
            try:
                # Try querying the database for an existing primary key
                session.query(model).filter(pk_column == random_pk).one()
            except NoResultFound:
                # If no result found, the primary key is unique
                return random_pk


@pytest.fixture(name='db_connection', scope='module')
def db_connection_fixture():
    """Set up a database connection for the module."""
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(name='db_session', scope='function')
def db_session_fixture(db_connection):
    """Set up a session with a transaction for each test function."""
    transaction = db_connection.begin_nested()
    session = Session(bind=db_connection)
    yield session
    session.close()

    if transaction.is_active:
        transaction.rollback()


@pytest.fixture(name='valid_employee', scope='function')
def valid_employee_fixture() -> Employee:
    """
    Create a valid Employee with a unique primary key.
    :return: an Employee object
    """
    associate_id = generate_unique_primary_key_str(Employee, Employee.associate_id)
    worker_id = generate_unique_primary_key_str(Employee, Employee.worker_id)
    return Employee(associate_id=associate_id, worker_id=worker_id,
                    first_name='Test First Name', last_name='Test Last Name')


@pytest.fixture(name='valid_pay_period', scope='function')
def valid_pay_period_fixture() -> PayPeriod:
    """
    Create a valid PayPeriod object with dates.
    Note: the primary key is assigned upon persistence (e.g., when flushed or committed to the database).
    :return: a PayPeriod object
    """
    return PayPeriod(pay_period_start=date(2023, 1, 1),
                     pay_period_end=date(2023, 1, 15))


@pytest.fixture(name='valid_timecard', scope='function')
def valid_timecard_fixture(db_session, valid_employee: Employee) -> Timecard:
    """
    Create a valid Timecard with a unique primary key.
    :param db_session: The database session fixture
    :param valid_employee: The valid employee fixture
    :return: a Timecard object
    """
    # Ensure the employee is added before creating the timecard
    db_session.add(valid_employee)

    return Timecard(timecard_id='TC-12345678987654321',
                    associate_id=valid_employee.associate_id,
                    pay_period_id=1,
                    has_exceptions=True)


@pytest.fixture(name='valid_day_entry', scope='function')
def valid_day_entry_fixture(db_session, valid_timecard: Timecard) -> DayEntry:
    """
    Create a valid DayEntry with a unique primary key.
    :param db_session: The database session fixture
    :param valid_timecard: The valid timecard fixture
    :return: a DayEntry object
    """
    # Ensure the timecard is added before creating the day entry
    db_session.add(valid_timecard)

    return DayEntry(entry_id='DE-12345678987654321',
                    timecard_id=valid_timecard.timecard_id,
                    entry_date=date(2022, 1, 1),
                    clock_in_time=datetime(2022, 1, 1, 0, 0, 0),
                    clock_out_time=datetime(2022, 1, 1, 0, 0, 0))

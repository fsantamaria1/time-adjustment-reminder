"""
This module contains functions to interact with the database.
"""
from sqlalchemy import or_
from .models import Employee, Timecard, DayEntry


def get_all_employees(session):
    """
    Get all employees from the database.
    :param session: SQLAlchemy session
    :return: List of Employee objects
    """
    return session.query(Employee).all()


def get_employee_by_associate_id(session, employee_id):
    """
    Get an employee by ID from the database.
    :param session: SQLAlchemy session
    :param employee_id: Employee ID
    :return: Employee object
    """
    return session.query(Employee).filter(Employee.associate_id == employee_id).first()


def get_employee_by_worker_id(session, worker_id):
    """
    Get an employee by worker ID from the database.
    :param session: SQLAlchemy session
    :param worker_id: Worker ID
    :return: Employee object
    """
    return session.query(Employee).filter(Employee.worker_id == worker_id).first()


def get_time_cards_with_missing_punches(session):
    """
    Get time cards with missing punches.
    :param session: The database session.
    :return: A list of time cards with missing punches.
    """
    # 2001-01-01 00:00:00.0000000 -05:00 is ADPs placeholder for missing punches
    return session.query(Timecard).join(DayEntry).filter(
        or_(DayEntry.clock_in_time == '2001-01-01 00:00:00.0000000 -05:00',
            DayEntry.clock_out_time == '2001-01-01 00:00:00.0000000 -05:00')
    ).all()

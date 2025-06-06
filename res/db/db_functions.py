"""
This module contains functions to interact with the database.
"""
from sqlalchemy import or_
from .models import Employee, Timecard, DayEntry, PayPeriod


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


def get_time_cards_with_missing_punches(session, pay_period_id=None):
    """
    Get time cards with missing punches.
    :param session: The database session.
    :param pay_period_id: (Optional) The ID of the pay period to filter by.
    :return: A list of time cards with missing punches.
    """
    # 2001-01-01 00:00:00.0000000 -05:00 is ADPs placeholder for missing punches
    # 2000-01-01 00:00:00.0000000 +00:00 is an additional placeholder for missing punches
    missing_punch_times = [
        '2001-01-01 00:00:00.0000000 -05:00',
        '2000-01-01 00:00:00.0000000 +00:00'
    ]

    # Query for time cards with missing punches
    query = session.query(Timecard).join(DayEntry).filter(
        or_(DayEntry.clock_in_time.in_(missing_punch_times),
            DayEntry.clock_out_time.in_(missing_punch_times))
    ).distinct()

    # If a pay period ID is provided, filter by it
    if pay_period_id is not None:
        query = query.filter(Timecard.pay_period_id == pay_period_id)

    return query.all()


def get_employees_with_missing_punches_by_pay_period(session, pay_period_id):
    """
    Get employees with missing punches by pay period.
    :param session: The database session.
    :param pay_period_id: The ID of the pay period.
    :return: A list of employees with missing punches for the specified pay period.
    """
    time_cards = get_time_cards_with_missing_punches(session, pay_period_id)
    employee_ids = {timecard.associate_id for timecard in time_cards}
    return session.query(Employee).filter(Employee.associate_id.in_(employee_ids)).all()


def get_worker_ids_with_missing_punches_by_pay_period(session, pay_period_id):
    """
    Get worker IDs with time cards containing missing punches by pay period.
    :param session: The database session.
    :param pay_period_id: The ID of the pay period.
    :return: A list of worker IDs.
    """
    time_cards = get_time_cards_with_missing_punches(session, pay_period_id)
    worker_ids = {timecard.employee.worker_id for timecard in time_cards}
    return worker_ids


def get_pay_period_by_start_date(session, start_date):
    """
    Get pay period by start date.
    :param session: The database session.
    :param start_date: The start date of the pay period.
    :return: A PayPeriod object or None if not found.
    """
    return session.query(PayPeriod).filter(PayPeriod.pay_period_start == start_date).first()

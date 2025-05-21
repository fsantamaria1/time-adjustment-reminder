"""
This module contains the models for the database.
"""
import os
from datetime import date, datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship

Base = declarative_base()


class Employee(Base):
    """
    Employee model for the database.
    """
    __tablename__ = 'Employees'
    __table_args__ = {'schema': os.environ.get('schema', 'dbo')}

    associate_id = Column(String(20), primary_key=True)
    worker_id = Column(String(20), unique=True, nullable=False)
    first_name = Column(String(25))
    last_name = Column(String(25))

    timecards = relationship('Timecard', back_populates="employee")

    def __init__(self,
                 associate_id: str,
                 worker_id: str,
                 first_name: str,
                 last_name: str):
        """
        Initialize the Employee object.
        :param associate_id: The associate id.
        :param worker_id: The worker id.
        :param first_name: The first name of the employee.
        :param last_name: The last name of the employee.
        """
        # Check that all the arguments are of the correct type
        if not isinstance(associate_id, str):
            raise TypeError("associate_id must be a string")
        if not isinstance(worker_id, str):
            raise TypeError("worker_id must be a string")
        if not isinstance(first_name, str):
            raise TypeError("first_name must be a string")
        if not isinstance(last_name, str):
            raise TypeError("last_name must be a string")

        self.associate_id = associate_id
        self.worker_id = worker_id
        self.first_name = first_name
        self.last_name = last_name

    def to_dict(self):
        """
        Convert the object to a dictionary.
        :return: A dictionary containing the employee data.
        """
        return {
            'associate_id': self.associate_id,
            'worker_id': self.worker_id,
            'first_name': self.first_name,
            'last_name': self.last_name
        }

    def __repr__(self):
        return (f"<Employee(associate_id={self.associate_id}, "
                f"worker_id={self.worker_id}, "
                f"first_name={self.first_name}, "
                f"last_name={self.last_name})>")


class PayPeriod(Base):
    """
    Pay period model for the database.
    """
    __tablename__ = 'PayPeriods'
    __table_args__ = {'schema': os.environ.get('schema', 'dbo')}

    pay_period_id = Column(Integer, primary_key=True, autoincrement=True)
    pay_period_start = Column(Date)
    pay_period_end = Column(Date)

    timecards = relationship("Timecard", back_populates="pay_period")

    def __init__(self,
                 pay_period_start: date,
                 pay_period_end: date):
        """
        Initialize the PayPeriod object.
        :param pay_period_start: The start date of the pay period.
        :param pay_period_end: The end date of the pay period.
        """
        # Check that all the arguments are of the correct type
        if not isinstance(pay_period_start, date):
            raise TypeError("pay_period_start must be a date")
        if not isinstance(pay_period_end, date):
            raise TypeError("pay_period_end must be a date")
        if pay_period_start > pay_period_end:
            raise ValueError("pay_period_start must be before pay_period_end")

        self.pay_period_start = pay_period_start
        self.pay_period_end = pay_period_end

    def to_dict(self):
        """
        Convert the object to a dictionary.
        :return: A dictionary containing the pay period data.
        """
        return {
            'pay_period_id': self.pay_period_id,
            'pay_period_start': self.pay_period_start,
            'pay_period_end': self.pay_period_end
        }

    def __repr__(self):
        return (f"<PayPeriod(pay_period_id={self.pay_period_id}, "
                f"pay_period_start={self.pay_period_start}, "
                f"pay_period_end={self.pay_period_end})>")


class Timecard(Base):
    """
    Timecard model for the database.
    """
    __tablename__ = 'Timecards'
    __table_args__ = {'schema': os.environ.get('schema', 'dbo')}

    timecard_id = Column(String(25), primary_key=True)
    associate_id = Column(String(20), ForeignKey(Employee.associate_id))
    pay_period_id = Column(Integer, ForeignKey(PayPeriod.pay_period_id), nullable=False)
    has_exceptions = Column(Boolean, nullable=False)

    employee = relationship("Employee", back_populates="timecards")
    day_entries = relationship("DayEntry", back_populates="timecard")
    pay_period = relationship("PayPeriod", back_populates="timecards")

    def __init__(self,
                 timecard_id: str,
                 associate_id: str,
                 pay_period_id: int,
                 has_exceptions: bool):
        """
            Initialize the Timecard object.
            :param timecard_id: The timecard id.
            :param associate_id: The associate id.
            :param pay_period_id: The pay period id.
            :param has_exceptions: Whether the timecard has exceptions.
            """
        # Check that all the arguments are of the correct type
        if not isinstance(timecard_id, str):
            raise TypeError("timecard_id must be a string")
        if not isinstance(associate_id, str):
            raise TypeError("associate_id must be a string")
        if not isinstance(pay_period_id, int):
            raise TypeError("pay_period_id must be an integer")
        if not isinstance(has_exceptions, bool):
            raise TypeError("has_exceptions must be a boolean")

        self.timecard_id = timecard_id
        self.associate_id = associate_id
        self.pay_period_id = pay_period_id
        self.has_exceptions = has_exceptions

    def to_dict(self):
        """
        Convert the object to a dictionary.
        :return: A dictionary containing the timecard data.
        """
        return {
            'timecard_id': self.timecard_id,
            'associate_id': self.associate_id,
            'pay_period_id': self.pay_period_id,
            'has_exceptions': self.has_exceptions
        }

    def __repr__(self):
        return (f"<Timecard(timecard_id={self.timecard_id}, "
                f"associate_id={self.associate_id}, "
                f"pay_period_id={self.pay_period_id}, "
                f"has_exceptions={self.has_exceptions})>")


class DayEntry(Base):
    """
    Day entry model for the database.
    """
    __tablename__ = 'DayEntries'
    __table_args__ = {'schema': os.environ.get('schema', 'dbo')}

    entry_id = Column(String(50), primary_key=True)
    timecard_id = Column(String(25), ForeignKey(Timecard.timecard_id))
    entry_date = Column(Date)
    clock_in_time = Column(DateTime(timezone=True))
    clock_out_time = Column(DateTime(timezone=True))

    timecard = relationship("Timecard", back_populates="day_entries")

    def __init__(self,
                 entry_id: str,
                 timecard_id: str,
                 entry_date: date,
                 clock_in_time: datetime | str,
                 clock_out_time: datetime | str):
        """
        Initialize the DayEntry object.
        :param entry_id: The unique identifier for the entry.
        :param timecard_id: The timecard id.
        :param entry_date: The entry date.
        :param clock_in_time: The clock in time in the format '%Y-%m-%d %H:%M:%S.%f %z'.
        Example '2001-01-01 00:00:00.0000000 -05:00'
        :param clock_out_time: The clock out time in the format '%Y-%m-%d %H:%M:%S.%f %z'.
        Example '2001-01-01 00:00:00.0000000 -05:00'
        """

        # Check that all the arguments are of the correct type
        if not isinstance(entry_id, str):
            raise TypeError("entry_id must be a string")
        if not isinstance(timecard_id, str):
            raise TypeError("timecard_id must be a string")
        if not isinstance(entry_date, date):
            raise TypeError("entry_date must be a date")

        self.entry_id = entry_id
        self.timecard_id = timecard_id
        self.entry_date = entry_date
        self.clock_in_time = clock_in_time
        self.clock_out_time = clock_out_time

    def to_dict(self):
        """
        Convert the object to a dictionary.
        :return: A dictionary containing the day entry data.
        """
        return {
            'entry_id': self.entry_id,
            'timecard_id': self.timecard_id,
            'entry_date': self.entry_date,
            'clock_in_time': self.clock_in_time,
            'clock_out_time': self.clock_out_time
        }

    def __repr__(self):
        return (f"<DayEntry(entry_id={self.entry_id}, "
                f"timecard_id={self.timecard_id}, "
                f"entry_date={self.entry_date}, "
                f"clock_in_time={self.clock_in_time}, "
                f"clock_out_time={self.clock_out_time})>")

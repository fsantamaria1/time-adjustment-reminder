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
    __table_args__ = {'schema': os.environ.get('schema')}

    associate_id = Column(String(20), primary_key=True, nullable=False)
    first_name = Column(String(25))
    last_name = Column(String(25))

    timecards = relationship('Timecard')

    def __init__(self,
                 associate_id: str,
                 first_name: str,
                 last_name: str):
        """
        Initialize the Employee object.
        :param associate_id: The associate id.
        :param first_name: The first name of the employee.
        :param last_name: The last name of the employee.
        """
        # Check that all the arguments are of the correct type
        if not isinstance(associate_id, str):
            raise TypeError("associate_id must be a string")
        if not isinstance(first_name, str):
            raise TypeError("first_name must be a string")
        if not isinstance(last_name, str):
            raise TypeError("last_name must be a string")

        self.associate_id = associate_id
        self.first_name = first_name
        self.last_name = last_name

    def to_dict(self):
        """
        Convert the object to a dictionary.
        :return: A dictionary containing the employee data.
        """
        return {
            'associate_id': self.associate_id,
            'first_name': self.first_name,
            'last_name': self.last_name
        }

    def __repr__(self):
        return (f"<Employee(associate_id={self.associate_id}, "
                f"first_name={self.first_name}, "
                f"last_name={self.last_name})>")


class AdpStatus(Base):
    """
    ADP status model for the database.
    """
    __tablename__ = 'Statuses'
    __table_args__ = {'schema': os.environ.get('schema')}

    status_id = Column(Integer, primary_key=True, autoincrement=True)
    status_code = Column(String(50))

    def __init__(self, status_code: str):
        """
        Initialize the ADP status object.
        :param status_code: The status code.
        """
        # Check that the argument is of the correct type
        if not isinstance(status_code, str):
            raise TypeError("status_code must be a string")

        self.status_code = status_code

    def to_dict(self):
        """
        Convert the object to a dictionary.
        :return: A dictionary containing the ADP status data.
        """
        return {
            'status_id': self.status_id,
            'status_code': self.status_code
        }

    def __repr__(self):
        return f"<AdpStatus(status_id={self.status_id}, status_code={self.status_code})>"


class Timecard(Base):
    """
    Timecard model for the database.
    """
    __tablename__ = 'Timecards'
    __table_args__ = {'schema': os.environ.get('schema')}

    timecard_id = Column(String(25), primary_key=True, nullable=False)
    associate_id = Column(String(20), ForeignKey(Employee.associate_id))
    pay_period_id = Column(Integer, nullable=False)
    status_id = Column(Integer, ForeignKey(AdpStatus.status_id))
    has_exceptions = Column(Boolean, nullable=False)

    employee = relationship("Employee", back_populates="timecards")
    day_entries = relationship("DayEntry", back_populates="timecard")

    def __init__(self,
                 timecard_id: str,
                 associate_id: str,
                 pay_period_id: int,
                 status_id: int,
                 has_exceptions: bool):
        """
            Initialize the Timecard object.
            :param timecard_id: The timecard id.
            :param associate_id: The associate id.
            :param pay_period_id: The pay period id.
            :param status_id: The status id.
            :param has_exceptions: Whether the timecard has exceptions.
            """
        # Check that all the arguments are of the correct type
        if not isinstance(timecard_id, str):
            raise TypeError("timecard_id must be a string")
        if not isinstance(associate_id, str):
            raise TypeError("associate_id must be a string")
        if not isinstance(pay_period_id, int):
            raise TypeError("pay_period_id must be an integer")
        if not isinstance(status_id, int):
            raise TypeError("status_id must be an integer")
        if not isinstance(has_exceptions, bool):
            raise TypeError("has_exceptions must be a boolean")

        self.timecard_id = timecard_id
        self.associate_id = associate_id
        self.pay_period_id = pay_period_id
        self.status_id = status_id
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
            'status_id': self.status_id,
            'has_exceptions': self.has_exceptions
        }

    def __repr__(self):
        return (f"<Timecard(timecard_id={self.timecard_id}, "
                f"associate_id={self.associate_id}, "
                f"pay_period_id={self.pay_period_id}, "
                f"status_id={self.status_id}, "
                f"has_exceptions={self.has_exceptions})>")


class DayEntry(Base):
    """
    Day entry model for the database.
    """
    __tablename__ = 'DayEntries'
    __table_args__ = {'schema': os.environ.get('schema')}

    entry_id = Column(String(50), primary_key=True, nullable=False)
    timecard_id = Column(String(25), ForeignKey(Timecard.timecard_id))
    entry_date = Column(Date)
    clock_in_time = Column(DateTime(timezone=True))
    clock_out_time = Column(DateTime(timezone=True))
    status_id = Column(Integer, ForeignKey(AdpStatus.status_id))

    timecard = relationship("Timecard", back_populates="day_entries")

    def __init__(self,
                 entry_id: str,
                 timecard_id: str,
                 entry_date: date,
                 clock_in_time: datetime,
                 clock_out_time: datetime,
                 status_id: int):
        """
        Initialize the DayEntry object.
        :param entry_id: The entry
        :param timecard_id: The timecard id.
        :param entry_date: The entry date.
        :param clock_in_time: The clock in time.
        :param clock_out_time: The clock out time.
        :param status_id: The status id.
        """

        # Check that all the arguments are of the correct type
        if not isinstance(entry_id, str):
            raise TypeError("entry_id must be a string")
        if not isinstance(timecard_id, str):
            raise TypeError("timecard_id must be a string")
        if not isinstance(entry_date, date):
            raise TypeError("entry_date must be a date")
        if not isinstance(clock_in_time, datetime):
            raise TypeError("clock_in_time must be a datetime")
        if not isinstance(clock_out_time, datetime):
            raise TypeError("clock_out_time must be a datetime")
        if not isinstance(status_id, int):
            raise TypeError("status_id must be an integer")

        self.entry_id = entry_id
        self.timecard_id = timecard_id
        self.entry_date = entry_date
        self.clock_in_time = clock_in_time
        self.clock_out_time = clock_out_time
        self.status_id = status_id

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
            'clock_out_time': self.clock_out_time,
            'status_id': self.status_id
        }

    def __repr__(self):
        return (f"<DayEntry(entry_id={self.entry_id}, "
                f"timecard_id={self.timecard_id}, "
                f"entry_date={self.entry_date}, "
                f"clock_in_time={self.clock_in_time}, "
                f"clock_out_time={self.clock_out_time}, "
                f"status_id={self.status_id})>")

"""
This module contains integration tests for the database models.
"""
import pytest
from sqlalchemy.exc import IntegrityError
from res.db.models import Employee, Timecard, DayEntry, PayPeriod


class TestEmployee:
    """
    Integration tests for the Employee model.
    """

    def test_employee_valid(self, db_session, valid_employee: Employee):
        """
        Test that an Employee record can be created with valid attributes.
        """
        db_session.add(valid_employee)
        db_session.flush()
        employee = db_session.query(Employee).filter(
            Employee.associate_id == valid_employee.associate_id
        ).first()

        assert employee.associate_id == valid_employee.associate_id
        assert employee.first_name == valid_employee.first_name
        assert employee.last_name == valid_employee.last_name

    @pytest.mark.parametrize(
        "valid_field_name, invalid_value",
        [
            ("associate_id", None),
            ("worker_id", None),
        ],
    )
    def test_employee_with_null_non_nullables(self,
                                              db_session,
                                              valid_employee,
                                              valid_field_name,
                                              invalid_value):
        """
        Test that an Employee record cannot be created with invalid attributes.
        """
        setattr(valid_employee, valid_field_name, invalid_value)
        db_session.add(valid_employee)

        with pytest.raises(IntegrityError):
            db_session.flush()


class TestPayPeriod:
    """
    Integration tests for the PayPeriod model.
    """

    def test_pay_period_valid(self, db_session, valid_pay_period: PayPeriod):
        """
        Test that a PayPeriod record can be created with valid attributes.
        """
        db_session.add(valid_pay_period)
        db_session.flush()
        pay_period = db_session.query(PayPeriod).filter(
            PayPeriod.pay_period_id == valid_pay_period.pay_period_id
        ).first()

        assert pay_period.pay_period_id == valid_pay_period.pay_period_id
        assert pay_period.pay_period_start == valid_pay_period.pay_period_start
        assert pay_period.pay_period_end == valid_pay_period.pay_period_end


class TestTimecard:
    """
    Integration tests for the Timecard model.
    """

    def test_timecard_valid(self, db_session, valid_timecard: Timecard):
        """
        Test that a Timecard record can be created with valid attributes.
        """
        db_session.add(valid_timecard)
        db_session.flush()
        timecard = db_session.query(Timecard).filter(
            Timecard.timecard_id == valid_timecard.timecard_id
        ).first()

        assert timecard.timecard_id == valid_timecard.timecard_id
        assert timecard.associate_id == valid_timecard.associate_id
        assert timecard.pay_period_id == valid_timecard.pay_period_id
        assert timecard.has_exceptions == valid_timecard.has_exceptions

    @pytest.mark.parametrize(
        "valid_field_name, invalid_value",
        [
            ("timecard_id", None),
            ("pay_period_id", None),
            ("has_exceptions", None),
        ],
    )
    def test_timecard_with_null_non_nullables(self,
                                              db_session,
                                              valid_timecard,
                                              valid_field_name,
                                              invalid_value):
        """
        Test that a Timecard record cannot be created with invalid attributes.
        """
        setattr(valid_timecard, valid_field_name, invalid_value)
        db_session.add(valid_timecard)

        with pytest.raises(IntegrityError):
            db_session.flush()


class TestDayEntry:
    """
    Integration tests for the DayEntry model.
    """

    def test_day_entry_valid(self, db_session, valid_day_entry: DayEntry):
        """
        Test that a DayEntry record can be created with valid attributes.
        """
        db_session.add(valid_day_entry)
        db_session.flush()
        day_entry = db_session.query(DayEntry).filter(
            DayEntry.entry_id == valid_day_entry.entry_id
        ).first()

        assert day_entry.entry_id == valid_day_entry.entry_id
        assert day_entry.timecard_id == valid_day_entry.timecard_id
        assert day_entry.entry_date == valid_day_entry.entry_date
        assert day_entry.clock_in_time == valid_day_entry.clock_in_time
        assert day_entry.clock_out_time == valid_day_entry.clock_out_time

    @pytest.mark.parametrize(
        "valid_field_name, invalid_value",
        [
            ("entry_id", None),
        ],
    )
    def test_day_entry_with_null_non_nullables(self,
                                               db_session,
                                               valid_day_entry,
                                               valid_field_name,
                                               invalid_value):
        """
        Test that a DayEntry record cannot be created with invalid attributes.
        """
        setattr(valid_day_entry, valid_field_name, invalid_value)
        db_session.add(valid_day_entry)

        with pytest.raises(IntegrityError):
            db_session.flush()

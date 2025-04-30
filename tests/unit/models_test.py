"""
This module contains tests for the models in the database package.
"""
from datetime import date, datetime
import pytest
from res.db.models import Employee, Timecard, DayEntry


class TestEmployee:
    """
    Test for the Employee class.
    """

    @pytest.fixture
    def valid_employee(self) -> Employee:
        """
        Create a valid Employee object.
        """
        return Employee(
            associate_id="associate_id",
            worker_id='worker_id',
            first_name='first name',
            last_name='last name'
        )

    def test_employee_instantiation_with_valid_attributes(self, valid_employee: Employee):
        """
        Test that the Employee class can be instantiated with valid attributes.
        """
        employee = valid_employee
        assert employee.associate_id == 'associate_id'
        assert employee.first_name == 'first name'
        assert employee.last_name == 'last name'
        assert employee.worker_id == 'worker_id'

    def test_employee_to_dict(self, valid_employee: Employee):
        """
        Test the to_dict method of the Employee class.
        :return:
        """
        employee = valid_employee
        assert employee.to_dict() == {
            'associate_id': 'associate_id',
            'worker_id': 'worker_id',
            'first_name': 'first name',
            'last_name': 'last name'
        }

    def test_employee_repr(self, valid_employee: Employee):
        """
        Test the __repr__ method of the Employee class.
        :return:
        """
        employee = valid_employee
        assert repr(employee) == ("<Employee(associate_id=associate_id, worker_id=worker_id, "
                                  "first_name=first name, last_name=last name)>")

    def test_attempt_instantiate_employee_missing_attributes(self):
        """
        Test that the Employee class cannot be instantiated without all required attributes.
        :return:
        """
        with pytest.raises(TypeError):
            # Missing required attributes
            Employee(associate_id=None, worker_id=None, first_name=None, last_name=None)

    @pytest.mark.parametrize("kwargs, exception_message", [
        ({"associate_id": 1, "worker_id": 'worker_id', "first_name": 'first name',
          "last_name": 'last name'},
         "associate_id must be a string"),
        ({"associate_id": 'associate_id', "worker_id": 1, "first_name": 'first name',
          "last_name": 'last name'},
         "worker_id must be a string"),
        ({"associate_id": 'associate_id', "worker_id": 'worker_id', "first_name": 1,
          "last_name": 'last name'},
         "first_name must be a string"),
        ({"associate_id": 'associate_id', "worker_id": 'worker_id', "first_name": 'first name',
          "last_name": 1},
         "last_name must be a string"),
    ])
    def test_employee_instantiation_with_invalid_attributes(self, kwargs, exception_message):
        """
        Test that the Employee class cannot be instantiated with invalid attributes.
        """
        with pytest.raises(TypeError) as exc_info:
            # Invalid attributes
            Employee(**kwargs)
        assert str(exc_info.value) == exception_message


class TestTimecard:
    """
    Test for the Timecard class.
    """

    @pytest.fixture
    def valid_timecard(self) -> Timecard:
        """
        Create a valid Timecard object.
        """
        return Timecard(timecard_id="timecard_id", associate_id='associate_id', pay_period_id=1,
                        has_exceptions=True)

    def test_timecard_instantiation_with_valid_attributes(self, valid_timecard: Timecard):
        """
        Test that the Timecard class can be instantiated with valid attributes.
        """
        timecard = valid_timecard
        assert timecard.timecard_id == 'timecard_id'
        assert timecard.associate_id == 'associate_id'
        assert timecard.pay_period_id == 1
        assert timecard.has_exceptions is True

    def test_timecard_to_dict(self, valid_timecard: Timecard):
        """
        Test the to_dict method of the Timecard class.
        :return:
        """
        timecard = valid_timecard
        assert timecard.to_dict() == {
            'timecard_id': 'timecard_id',
            'associate_id': 'associate_id',
            'pay_period_id': 1,
            'has_exceptions': True
        }

    def test_timecard_repr(self, valid_timecard: Timecard):
        """
        Test the __repr__ method of the Timecard class.
        :return:
        """
        timecard = valid_timecard
        assert repr(timecard) == ("<Timecard(timecard_id=timecard_id, associate_id=associate_id, "
                                  "pay_period_id=1, has_exceptions=True)>")

    @pytest.mark.parametrize("kwargs, exception_message", [
        ({"timecard_id": 1, "associate_id": "associate_id", "pay_period_id": 1,
          "has_exceptions": True},
            "timecard_id must be a string"),
        ({"timecard_id": "timecard_id", "associate_id": 1, "pay_period_id": 1,
          "has_exceptions": True},
            "associate_id must be a string"),
        ({"timecard_id": "timecard_id", "associate_id": "associate_id", "pay_period_id": "1",
          "has_exceptions": True},
            "pay_period_id must be an integer"),
        ({"timecard_id": "timecard_id", "associate_id": "associate_id", "pay_period_id": 1,
          "has_exceptions": 1},
            "has_exceptions must be a boolean"),
    ])
    def test_timecard_instantiation_with_invalid_attributes(self, kwargs, exception_message):
        """
        Test that the Timecard class cannot be instantiated with invalid attributes.
        """
        with pytest.raises(TypeError) as exc_info:
            # Invalid attributes
            Timecard(**kwargs)
        assert str(exc_info.value) == exception_message

    def test_attempt_instantiate_timecard_missing_attributes(self):
        """
        Test that the Timecard class cannot be instantiated without all required attributes.
        :return:
        """
        with pytest.raises(TypeError):
            # Missing required attributes
            Timecard(timecard_id=None, associate_id=None, pay_period_id=None,
                     has_exceptions=None)


class TestDayEntry:
    """
    Test for the DayEntry class.
    """

    @pytest.fixture
    def valid_day_entry(self) -> DayEntry:
        """
        Create a valid DayEntry object.
        """
        return DayEntry(entry_id="entry_id", timecard_id='timecard_id', entry_date=date(2022, 1, 1),
                        clock_in_time=datetime(2022, 1, 1, 0, 0, 0),
                        clock_out_time=datetime(2022, 1, 1, 0, 0, 0))

    def test_day_entry_instantiation_with_valid_attributes(self, valid_day_entry: DayEntry):
        """
        Test that the DayEntry class can be instantiated with valid attributes.
        """
        day_entry = valid_day_entry
        assert day_entry.entry_id == 'entry_id'
        assert day_entry.timecard_id == 'timecard_id'
        assert day_entry.entry_date == date(2022, 1, 1)
        assert day_entry.clock_in_time == datetime(2022, 1, 1, 0, 0, 0)
        assert day_entry.clock_out_time == datetime(2022, 1, 1, 0, 0, 0)

    def test_day_entry_to_dict(self, valid_day_entry: DayEntry):
        """
        Test the to_dict method of the DayEntry class.
        :return:
        """
        day_entry = valid_day_entry
        assert day_entry.to_dict() == {
            'entry_id': 'entry_id',
            'timecard_id': 'timecard_id',
            'entry_date': date(2022, 1, 1),
            'clock_in_time': datetime(2022, 1, 1, 0, 0, 0),
            'clock_out_time': datetime(2022, 1, 1, 0, 0, 0),
        }

    def test_day_entry_repr(self, valid_day_entry: DayEntry):
        """
        Test the __repr__ method of the DayEntry class.
        :return:
        """
        day_entry = valid_day_entry
        assert repr(day_entry) == ("<DayEntry(entry_id=entry_id, timecard_id=timecard_id, "
                                   "entry_date=2022-01-01, "
                                   "clock_in_time=2022-01-01 00:00:00, "
                                   "clock_out_time=2022-01-01 00:00:00>")

    def test_attempt_instantiate_day_entry_missing_attributes(self):
        """
        Test that the DayEntry class cannot be instantiated without all required attributes.
        :return:
        """
        with pytest.raises(TypeError):
            # Missing required attributes
            DayEntry(entry_id=None, timecard_id=None, entry_date=None,
                     clock_in_time=None, clock_out_time=None)

    @pytest.mark.parametrize("kwargs, exception_message", [
        ({"entry_id": 1, "timecard_id": "timecard_id", "entry_date": date(2022, 1, 1),
          "clock_in_time": datetime(2022, 1, 1, 0, 0, 0),
          "clock_out_time": datetime(2022, 1, 1, 0, 0, 0)},
            "entry_id must be a string"),
        ({"entry_id": "entry_id", "timecard_id": 1, "entry_date": date(2022, 1, 1),
          "clock_in_time": datetime(2022, 1, 1, 0, 0, 0),
          "clock_out_time": datetime(2022, 1, 1, 0, 0, 0)},
            "timecard_id must be a string"),
        ({"entry_id": "entry_id", "timecard_id": "timecard_id", "entry_date": 1,
          "clock_in_time": datetime(2022, 1, 1, 0, 0, 0),
          "clock_out_time": datetime(2022, 1, 1, 0, 0, 0)},
            "entry_date must be a date"),
        ({"entry_id": "entry_id", "timecard_id": "timecard_id", "entry_date": date(2022, 1, 1),
          "clock_in_time": 1,
          "clock_out_time": datetime(2022, 1, 1, 0, 0, 0)},
            "clock_in_time must be a datetime"),
        ({"entry_id": "entry_id", "timecard_id": "timecard_id", "entry_date": date(2022, 1, 1),
          "clock_in_time": datetime(2022, 1, 1, 0, 0, 0),
          "clock_out_time": 1},
            "clock_out_time must be a datetime"),
    ])
    def test_day_entry_instantiation_with_invalid_attributes(self, kwargs, exception_message):
        """
        Test that the DayEntry class cannot be instantiated with invalid attributes.
        """
        with pytest.raises(TypeError) as exc_info:
            # Invalid attributes
            DayEntry(**kwargs)
        assert str(exc_info.value) == exception_message

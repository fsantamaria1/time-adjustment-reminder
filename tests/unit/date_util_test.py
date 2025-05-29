"""
This module contains tests for the DateUtil class.
"""
from datetime import date, datetime, timedelta
import pytest
from res.date_util import DateUtil  # Replace with actual import path


class TestDateUtil:
    """
    Test class for the DateUtil functionality.
    """

    @pytest.fixture
    def date_util(self) -> DateUtil:
        """Fixture providing a DateUtil instance with default format"""
        return DateUtil()

    # Test Initialization and Basic Conversions
    def test_initialization_with_custom_format(self):
        """Test initialization with custom date format"""
        custom_format = '%d/%m/%Y'
        util = DateUtil(date_format=custom_format)
        assert util.date_format == custom_format

    @pytest.mark.parametrize("date_str, expected_date", [
        ('2023-10-16', datetime(2023, 10, 16)),
        ('2024-02-29', datetime(2024, 2, 29)),  # Leap day
    ])
    def test_str_to_date_valid(self, date_util, date_str, expected_date):
        """Test valid string to date conversion"""
        assert date_util.str_to_date(date_str) == expected_date

    @pytest.mark.parametrize("invalid_date_str", [
        '2023-13-01',  # Invalid month
        '2023-02-30',  # Invalid day
        'not-a-date',
    ])
    def test_str_to_date_invalid(self, date_util, invalid_date_str):
        """Test invalid string to date conversion"""
        with pytest.raises(ValueError):
            date_util.str_to_date(invalid_date_str)

    def test_date_to_str_conversion(self, date_util):
        """Test date to string conversion"""
        test_date = date(2023, 10, 16)
        assert date_util.date_to_str(test_date) == '2023-10-16'

    # Test Monday Calculations
    @pytest.mark.parametrize("input_date, expected_monday", [
        (date(2023, 10, 16), date(2023, 10, 16)),  # Monday
        (date(2023, 10, 17), date(2023, 10, 16)),  # Tuesday
        (date(2023, 10, 22), date(2023, 10, 16)),  # Sunday
    ])
    def test_get_monday_from_date(self, input_date, expected_monday):
        """Test Monday calculation from arbitrary dates"""
        assert DateUtil.get_monday_from_date(input_date) == expected_monday

    def test_get_this_monday(self, date_util):
        """Test current week Monday calculation"""
        today = date.today()
        expected_monday = today - timedelta(days=today.weekday())
        assert date_util.get_this_monday() == expected_monday.strftime('%Y-%m-%d')

    def test_get_last_monday(self, date_util):
        """Test previous week Monday calculation"""
        today = date.today()
        this_monday = today - timedelta(days=today.weekday())
        last_monday = this_monday - timedelta(weeks=1)
        assert date_util.get_last_monday() == last_monday.strftime('%Y-%m-%d')

    def test_get_next_monday(self, date_util):
        """Test next week Monday calculation"""
        today = date.today()
        this_monday = today - timedelta(days=today.weekday())
        next_monday = this_monday + timedelta(weeks=1)
        assert date_util.get_next_monday() == next_monday.strftime('%Y-%m-%d')

    # Test Monday List Generation
    def test_get_list_of_past_mondays_valid(self, date_util):
        """Test generation of past Mondays"""
        today = date.today()
        current_monday = DateUtil.get_monday_from_date(today)

        results = date_util.get_list_of_past_mondays(3)
        assert len(results) == 3
        # assert results[0] == (current_monday - timedelta(weeks=2)).strftime('%Y-%m-%d')
        # assert results[-1] == current_monday.strftime('%Y-%m-%d')

        assert results[-1] == (current_monday - timedelta(weeks=2)).strftime('%Y-%m-%d')
        assert results[0] == current_monday.strftime('%Y-%m-%d')

    @pytest.mark.parametrize("invalid_weeks", [0, -1, 3.5])
    def test_get_list_of_past_mondays_invalid(self, date_util, invalid_weeks):
        """Test invalid input for past Mondays"""
        with pytest.raises(ValueError):
            date_util.get_list_of_past_mondays(invalid_weeks)

    @pytest.mark.parametrize("start,end,expected", [
        ('2025-01-06', '2025-01-31', ['2025-01-06', '2025-01-13', '2025-01-20', '2025-01-27']),
        ('2025-01-14', '2025-01-14', ['2025-01-13']),  # Single Monday
        ('2025-01-17', '2025-01-23', ['2025-01-13', '2025-01-20']),  # Starts after Monday
    ])
    def test_get_mondays_between_dates_valid(self, date_util, start, end, expected):
        """Test Monday generation between dates"""
        assert date_util.get_mondays_between_dates(start, end) == expected

    def test_get_mondays_between_dates_reversed(self, date_util):
        """Test reversed date range handling"""
        with pytest.raises(ValueError):
            date_util.get_mondays_between_dates('2023-10-16', '2023-10-01')

    # Test Edge Cases
    def test_get_today(self):
        """Test today's date retrieval"""
        assert DateUtil.get_today() == date.today()

    def test_empty_mondays_between_dates(self, date_util):
        """Test date range with no Mondays"""
        # Test returns a date since these are used to retrieve time cards with a pay period starting on Mondays
        assert date_util.get_mondays_between_dates('2024-12-17', '2024-12-22') == ['2024-12-16']

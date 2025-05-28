"""
Contains the DateUtil class for performing date operations.
"""
from datetime import date, datetime, timedelta
from typing import List


class DateUtil:
    """
    A utility class for performing date operations.
    """

    def __init__(self, date_format: str = '%Y-%m-%d'):
        """
        Initializes the DateUtil class with a date format.
        :param date_format: str: The date format to use (default: '%Y-%m-%d').
        """
        self.date_format = date_format

    def str_to_date(self, date_str: str) -> datetime:
        """
        Converts a string to a datetime object.
        :param date_str: str: A string formatted as self.date_format.
        :return: datetime: A datetime object.
        :raises ValueError: If the input string is not in the correct format.
        """
        return datetime.strptime(date_str, self.date_format)

    def date_to_str(self, date_obj: date) -> str:
        """
        Converts a date object to a string using the instance's date format.
        :param date_obj: date: A date object.
        :return: str: A string formatted as self.date_format.
        """
        return date_obj.strftime(self.date_format)

    @staticmethod
    def get_monday_from_date(some_date: date) -> date:
        """
        Returns the Monday of the week for the given date.
        :param some_date: date: A date object.
        :return: date: The Monday of the week for the given date.
        """
        return some_date - timedelta(days=some_date.weekday())

    def get_this_monday(self) -> str:
        """
        Returns the Monday of the current week.
        :return: str: A string representing the Monday of the current week.
        Example:
            date_util = DateUtil()
            date_util.get_this_monday()
            '2023-10-16'
        """
        today = date.today()
        this_monday = self.get_monday_from_date(today)
        return self.date_to_str(this_monday)

    def get_last_monday(self) -> str:
        """
        Returns the Monday of the previous week.
        :return: str: A string representing the Monday of the previous week.
        Example:
            date_util = DateUtil()
            date_util.get_last_monday()
            '2023-10-09'
        """
        today = date.today()
        last_monday = self.get_monday_from_date(today) - timedelta(weeks=1)
        return self.date_to_str(last_monday)

    def get_next_monday(self) -> str:
        """
        Returns the Monday of the next week.
        :return: str: A string representing the Monday of the next week.
        Example:
            date_util = DateUtil()
            date_util.get_next_monday()
            '2023-10-23'
        """
        today = date.today()
        next_monday = self.get_monday_from_date(today) + timedelta(weeks=1)
        return self.date_to_str(next_monday)

    def get_list_of_past_mondays(self, num_weeks: int) -> List[str]:
        """
        Returns a list of Monday dates for the past `num_weeks` weeks.
        :param num_weeks: int: The number of weeks for which to generate Monday dates.
        :return: List[str]: A list of Monday dates formatted as self.date_format.
        Example:
            date_util = DateUtil()
            date_util.get_list_of_past_mondays(3)
            ['2023-10-02', '2023-10-09', '2023-10-16']
        """
        if num_weeks < 1 or type(num_weeks) is not int:
            raise ValueError("num_weeks must be a positive integer")
        today = date.today()
        current_monday = self.get_monday_from_date(today)

        return [
            self.date_to_str(current_monday - timedelta(weeks=i))
            for i in range(num_weeks)
        ]

    def get_mondays_between_dates(self, start_date_str: str, end_date_str: str) -> List[str]:
        """
        Returns a list of Monday dates between two given dates.
        :param start_date_str: str: A string formatted as self.date_format.
        :param end_date_str: str: A string formatted as self.date_format.
        :return: List[str]: A list of Monday dates formatted as self.date_format.
        Example:
            date_util = DateUtil()
            date_util.get_mondays_between_dates('2023-10-01', '2023-10-15')
            ['2023-10-02', '2023-10-09']
        Example 2:
            date_util = DateUtil()
            date_util.get_mondays_between_dates('2025-01-14', '2025-01-14')
            ['2025-01-13']
            # Returns a Monday even though there are no Mondays between the dates.
            This was done on purpose as we might want to get the Monday of the start date.
        """
        if start_date_str > end_date_str:
            return []
        start_date = self.str_to_date(start_date_str)
        end_date = self.str_to_date(end_date_str)
        start_monday = self.get_monday_from_date(start_date)
        mondays = []
        while start_monday <= end_date:
            mondays.append(self.date_to_str(start_monday))
            start_monday += timedelta(weeks=1)
        return mondays

    @staticmethod
    def get_today() -> date:
        """
        Returns today's date.
        :return: date: Today's date as a date object.
        """
        return date.today()

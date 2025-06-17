"""
Data models for the Tahara Calculator.

This module contains the core data structures for representing 
menstrual periods and forbidden days in Hebrew calendar calculations.
"""

from pyluach import dates


class MenstrualPeriod:
    """Represents a menstrual period with Hebrew calendar date and timing."""
    
    def __init__(self, hebrew_date, time_of_day, cycle_interval=None):
        """
        Initialize a menstrual period.
        
        Args:
            hebrew_date: Hebrew calendar date of the period
            time_of_day: 0 for night, 1 for day
            cycle_interval: Number of days between periods (optional)
        """
        self.hebrew_date = hebrew_date
        self.time_of_day = time_of_day  # 0 = night, 1 = day
        self.weekday = hebrew_date.weekday()
        self.cycle_interval = cycle_interval
        self._forbidden_days_list = []

    @property
    def forbidden_days_list(self):
        """Get the list of forbidden days for this period."""
        return self._forbidden_days_list

    @forbidden_days_list.setter
    def forbidden_days_list(self, forbidden_days_list):
        """Set the list of forbidden days for this period."""
        self._forbidden_days_list = forbidden_days_list

    def add_forbidden_day(self, forbidden_day):
        """Add a forbidden day to this period."""
        self.forbidden_days_list.append(forbidden_day)

    @property
    def period_details(self):
        """Get period details as a list."""
        return [self.time_of_day, self.cycle_interval]

    @period_details.setter
    def period_details(self, details_list):
        """Set period details from a list."""
        if len(details_list) >= 2:
            self.time_of_day = details_list[0]
            self.cycle_interval = details_list[1]


class ForbiddenDay:
    """Represents a forbidden day with its restrictions and timing."""
    
    def __init__(self, menstrual_period, restriction_name, hebrew_date, time_of_day):
        """
        Initialize a forbidden day.
        
        Args:
            menstrual_period: The associated menstrual period
            restriction_name: Name of the restriction (Hebrew)
            hebrew_date: Hebrew date of the forbidden day
            time_of_day: 0 for night, 1 for day
        """
        self.menstrual_period = menstrual_period
        self.restriction_name = restriction_name
        self.hebrew_date = hebrew_date
        self.year = hebrew_date.year
        self.month = hebrew_date.month
        self.day = hebrew_date.day
        self.weekday = hebrew_date.weekday()
        self.time_of_day = time_of_day
        self.restriction_details = [
            self.restriction_name, 
            self.time_of_day, 
            self.menstrual_period.hebrew_date.month
        ]

    def get_restriction_details(self):
        """Get the restriction details as a list."""
        return self.restriction_details

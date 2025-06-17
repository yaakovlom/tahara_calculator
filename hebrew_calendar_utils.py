"""
Hebrew calendar utilities for the Tahara Calculator.

This module provides utility functions for working with Hebrew calendar dates
and calculating month lengths.
"""

from pyluach import dates, hebrewcal


def get_hebrew_month_length(hebrew_month: hebrewcal.Month):
    """
    Get the length of the Hebrew month.
    
    Args:
        hebrew_month: A Hebrew calendar month object
        
    Returns:
        int: The number of days in the month
    """
    next_month_first_day = dates.HebrewDate(
        (hebrew_month + 1).year, 
        (hebrew_month + 1).month, 
        1
    ) - 1
    current_month_length = next_month_first_day.day
    return current_month_length

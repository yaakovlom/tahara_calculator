"""
Date conversion utilities for the Tahara Calculator.

This module provides functions to convert between Gregorian and Hebrew dates,
making it easier for users to input dates in familiar formats.
"""

import sys
import os
from datetime import datetime
from typing import Optional, Tuple

# Add the parent directory to the Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from pyluach import dates


def convert_gregorian_to_hebrew(gregorian_date_str: str) -> Optional[dates.HebrewDate]:
    """
    Convert a Gregorian date string to Hebrew date.
    
    Args:
        gregorian_date_str: Date string in format "DD/MM/YYYY", "DD-MM-YYYY", or "YYYY-MM-DD"
        
    Returns:
        HebrewDate object or None if conversion failed
    """
    try:
        # Handle different date formats
        if '/' in gregorian_date_str:
            parts = gregorian_date_str.split('/')
        elif '-' in gregorian_date_str:
            parts = gregorian_date_str.split('-')
        else:
            return None
        
        if len(parts) != 3:
            return None
        
        # Determine format based on first part length
        if len(parts[0]) == 4:  # YYYY-MM-DD format
            year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
        else:  # DD/MM/YYYY or DD-MM-YYYY format
            day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
        
        # Convert to Hebrew date
        gregorian_date = datetime(year, month, day)
        hebrew_date = dates.HebrewDate.from_pydate(gregorian_date.date())
        
        return hebrew_date
        
    except (ValueError, IndexError) as e:
        print(f"Error converting date '{gregorian_date_str}': {e}")
        return None


def format_hebrew_date_for_input(hebrew_date: dates.HebrewDate, time_of_day: int) -> str:
    """
    Format a Hebrew date for input file format.
    
    Args:
        hebrew_date: HebrewDate object
        time_of_day: 0 for night, 1 for day
        
    Returns:
        Formatted string for input file
    """
    return f"{hebrew_date.day}/{hebrew_date.month}/{hebrew_date.year} {time_of_day}"


def parse_mixed_date_input(date_input: str) -> Optional[Tuple[dates.HebrewDate, int]]:
    """
    Parse date input that could be either Hebrew or Gregorian format.
    
    Args:
        date_input: Date string with time_of_day (e.g., "15/03/2024 1", "8/12/5785 0", or "today 1")
        
    Returns:
        Tuple of (HebrewDate, time_of_day) or None if parsing failed
    """
    try:
        parts = date_input.strip().split()
        if len(parts) < 2:
            return None
        
        date_part = parts[0].lower()
        time_of_day = int(parts[1])
        
        if time_of_day not in [0, 1]:
            return None
        
        # Handle "today" keyword
        if date_part == "today":
            today = datetime.now()
            hebrew_date = dates.HebrewDate.from_pydate(today.date())
            return hebrew_date, time_of_day
        
        # Try to parse as Hebrew date first
        try:
            date_components = [int(n) for n in date_part.split("/")]
            if len(date_components) == 3:
                # Check if it looks like a Hebrew date (year > 5000)
                if date_components[2] > 5000:
                    hebrew_date = dates.HebrewDate(*date_components[::-1])  # reverse for Hebrew format
                    return hebrew_date, time_of_day
        except:
            pass
        
        # Try to parse as Gregorian date
        hebrew_date = convert_gregorian_to_hebrew(date_part)
        if hebrew_date:
            return hebrew_date, time_of_day
        
        return None
        
    except (ValueError, IndexError) as e:
        print(f"Error parsing mixed date input '{date_input}': {e}")
        return None


def get_date_format_help() -> str:
    """Get help text for supported date formats."""
    return """
Supported Date Formats:

Hebrew Calendar:
  - 8/12/5785 0  (day/month/year time_of_day)
  
Gregorian Calendar:
  - 15/03/2024 1  (DD/MM/YYYY time_of_day)
  - 15-03-2024 1  (DD-MM-YYYY time_of_day)
  - 2024-03-15 1  (YYYY-MM-DD time_of_day)

Special Keywords:
  - today 1      (Current date, day)
  - today 0      (Current date, night)

Time of Day:
  - 0 = Night (ליל)
  - 1 = Day (יום)

Examples:
  - 8/12/5785 0    # Hebrew date, night
  - 15/03/2024 1   # Gregorian date, day
  - 2024-03-15 0   # ISO format, night
  - today 1        # Today, day
  - today 0        # Today, night
"""


def validate_date_input(date_input: str) -> bool:
    """
    Validate if a date input string is in correct format.
    
    Args:
        date_input: Date string to validate
        
    Returns:
        True if valid, False otherwise
    """
    result = parse_mixed_date_input(date_input)
    return result is not None


def get_today_hebrew_date() -> dates.HebrewDate:
    """
    Get today's date as a Hebrew date.
    
    Returns:
        HebrewDate object for today's date
    """
    today = datetime.now()
    return dates.HebrewDate.from_pydate(today.date())


def format_today_for_input(time_of_day: int) -> str:
    """
    Format today's date for input file format.
    
    Args:
        time_of_day: 0 for night, 1 for day
        
    Returns:
        Formatted string for input file with today's Hebrew date
    """
    today_hebrew = get_today_hebrew_date()
    return format_hebrew_date_for_input(today_hebrew, time_of_day)

"""
Data parsing utilities for the Tahara Calculator.

This module handles parsing text input into period objects.
"""

import sys
import os

# Add the parent directory to the Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from pyluach import dates
from src.models import MenstrualPeriod
from config.config_db import get_config
from utils.date_converter import parse_mixed_date_input


def convert_text_to_menstrual_period(date_text):
    """
    Convert date text to MenstrualPeriod object.
    Supports both Hebrew and Gregorian date formats.
    
    Args:
        date_text: Text string containing date and time information
        
    Returns:
        MenstrualPeriod: Parsed period object, or None if parsing failed
    """
    try:
        # Use the new mixed date parser
        result = parse_mixed_date_input(date_text)
        if result:
            hebrew_date, time_of_day = result
            menstrual_period = MenstrualPeriod(hebrew_date, time_of_day)
            return menstrual_period
        return None
    except (ValueError, IndexError) as error:
        config = get_config()
        if config.should_show_parsing_errors():
            print(f"Error parsing date '{date_text}': {error}")
        return None

"""
Data parsing utilities for the Tahara Calculator.

This module handles parsing text input into period objects.
"""

from pyluach import dates
from models import MenstrualPeriod


def convert_text_to_menstrual_period(date_text):
    """
    Convert date text to MenstrualPeriod object.
    
    Args:
        date_text: Text string containing date and time information
        
    Returns:
        MenstrualPeriod: Parsed period object, or None if parsing failed
    """
    try:
        parsed_details = date_text.strip().split()
        if len(parsed_details) < 2:
            return None
            
        date_components = [int(component) for component in parsed_details[0].split("/")]
        if len(date_components) != 3:
            return None
            
        time_of_day = int(parsed_details[1][0])
        if time_of_day in [0, 1]:
            menstrual_period = MenstrualPeriod(
                dates.HebrewDate(*date_components[::-1]), 
                time_of_day
            )
            return menstrual_period
        return None
    except (ValueError, IndexError) as error:
        print(f"Error parsing date '{date_text}': {error}")
        return None

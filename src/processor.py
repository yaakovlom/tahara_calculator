"""
Core processing logic for the Tahara Calculator.

This module contains the main processing logic that coordinates
all the other modules to perform the calculations.
"""

import sys
import os

# Add the parent directory to the Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.parsers import convert_text_to_menstrual_period
from src.calculations import calculate_forbidden_days


def process_periods_data(period_dates_list):
    """
    Process raw period data into menstrual period objects.
    
    Args:
        period_dates_list: List of raw date text entries
        
    Returns:
        list: List of MenstrualPeriod objects
    """
    menstrual_periods_list = []
    
    for date_text_entry in period_dates_list:
        try:
            menstrual_period = convert_text_to_menstrual_period(date_text_entry)
            if menstrual_period:
                menstrual_periods_list.append(menstrual_period)
        except NameError as parsing_error:
            print(parsing_error)
    
    return menstrual_periods_list


def calculate_cycle_intervals(menstrual_periods_list):
    """
    Calculate cycle intervals between consecutive periods.
    
    Args:
        menstrual_periods_list: List of menstrual periods
        
    Returns:
        list: List of cycle intervals
    """
    # Calculate the cycle intervals between consecutive periods
    for period_index, current_period in enumerate(menstrual_periods_list[1:]):
        cycle_interval = (
            current_period.hebrew_date - 
            menstrual_periods_list[period_index].hebrew_date + 1
        )
        current_period.cycle_interval = int(cycle_interval)
    
    return [period.cycle_interval for period in menstrual_periods_list[1:]]


def calculate_all_forbidden_days(menstrual_periods_list, historical_cycle_intervals):
    """
    Calculate forbidden days for all periods.
    
    Args:
        menstrual_periods_list: List of menstrual periods
        historical_cycle_intervals: List of historical cycle intervals
    """
    for period_index, current_period in enumerate(menstrual_periods_list):
        if historical_cycle_intervals:
            current_period.forbidden_days_list = calculate_forbidden_days(
                current_period, 
                historical_cycle_intervals[:period_index]
            )
        else:
            current_period.forbidden_days_list = calculate_forbidden_days(current_period)


def create_periods_index(menstrual_periods_list):
    """
    Create an index of periods by their Hebrew dates.
    
    Args:
        menstrual_periods_list: List of menstrual periods
        
    Returns:
        dict: Dictionary mapping Hebrew dates to periods
    """
    return {period.hebrew_date: period for period in menstrual_periods_list}

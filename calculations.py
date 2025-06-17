"""
Core calculation engine for forbidden days in the Tahara Calculator.

This module contains the main logic for calculating forbidden days
based on menstrual periods and Hebrew calendar rules.
"""

from pyluach import hebrewcal
from models import ForbiddenDay
from hebrew_calendar_utils import get_hebrew_month_length


def calculate_forbidden_days(menstrual_period, previous_cycle_intervals=None):
    """
    Calculate list of forbidden days from a menstrual period.
    
    Args:
        menstrual_period: The menstrual period to calculate from
        previous_cycle_intervals: List of previous cycle intervals (optional)
        
    Returns:
        list: List of ForbiddenDay objects and unbroken pattern lists
    """
    period_date = menstrual_period.hebrew_date
    hebrew_year = period_date.year
    hebrew_month = period_date.month
    hebrew_day = period_date.day
    current_month_length = get_hebrew_month_length(hebrewcal.Month(hebrew_year, hebrew_month))
    
    # Standard forbidden day calculations
    standard_30_day_cycle = ForbiddenDay(
        menstrual_period, 
        'עונה בינונית 30', 
        period_date + 29, 
        menstrual_period.time_of_day
    )
    monthly_cycle_pattern = ForbiddenDay(
        menstrual_period, 
        'וסת החודש', 
        period_date + current_month_length, 
        menstrual_period.time_of_day
    )
    standard_31_day_cycle = ForbiddenDay(
        menstrual_period, 
        'עונה בינונית 31', 
        period_date + 30, 
        menstrual_period.time_of_day
    )
    forbidden_days_list = [standard_30_day_cycle, monthly_cycle_pattern, standard_31_day_cycle]
    
    # Add personal cycle pattern if available
    if menstrual_period.cycle_interval:
        personal_cycle_pattern = ForbiddenDay(
            menstrual_period, 
            'הפלגה', 
            period_date + menstrual_period.cycle_interval - 1, 
            menstrual_period.time_of_day
        )
        forbidden_days_list.append(personal_cycle_pattern)
    
    # Add unbroken cycle patterns if available
    if previous_cycle_intervals:
        unbroken_patterns = _calculate_unbroken_patterns(
            menstrual_period, 
            previous_cycle_intervals, 
            period_date
        )
        if unbroken_patterns:
            forbidden_days_list.append(unbroken_patterns)
    
    # Add special restrictions based on time of day
    _add_time_based_restrictions(
        menstrual_period, 
        forbidden_days_list, 
        standard_30_day_cycle
    )

    return forbidden_days_list


def _calculate_unbroken_patterns(menstrual_period, previous_cycle_intervals, period_date):
    """
    Calculate unbroken cycle patterns from previous intervals.
    
    Args:
        menstrual_period: The current menstrual period
        previous_cycle_intervals: List of previous cycle intervals
        period_date: The Hebrew date of the current period
        
    Returns:
        list: List of unbroken pattern ForbiddenDay objects, or None
    """
    if len(previous_cycle_intervals) < 2:
        return None
        
    unbroken_cycle_patterns = []
    for current_interval in previous_cycle_intervals[-1::-1]:
        is_pattern_broken = False
        for comparison_interval in previous_cycle_intervals[-1:previous_cycle_intervals.index(current_interval):-1]:
            if comparison_interval > current_interval:
                is_pattern_broken = True
        if not is_pattern_broken:
            unbroken_pattern = ForbiddenDay(
                menstrual_period, 
                str(current_interval), 
                period_date + current_interval - 1, 
                menstrual_period.time_of_day
            )
            unbroken_cycle_patterns.append(unbroken_pattern)
    
    return unbroken_cycle_patterns if unbroken_cycle_patterns else None


def _add_time_based_restrictions(menstrual_period, forbidden_days_list, standard_30_day_cycle):
    """
    Add time-based restrictions (Or Zarua and Kartyupleity).
    
    Args:
        menstrual_period: The current menstrual period
        forbidden_days_list: List to add restrictions to
        standard_30_day_cycle: The 30-day cycle forbidden day
    """
    if not menstrual_period.time_of_day:  # Night time occurrence
        or_zarua_restriction = ForbiddenDay(
            menstrual_period, 
            'אור זרוע', 
            standard_30_day_cycle.hebrew_date - 1, 
            menstrual_period.time_of_day + 1
        )
        kartyupleity_restriction = ForbiddenDay(
            menstrual_period, 
            'כרתי ופלתי', 
            standard_30_day_cycle.hebrew_date, 
            menstrual_period.time_of_day + 1
        )
        forbidden_days_list.insert(0, or_zarua_restriction)
        forbidden_days_list.insert(2, kartyupleity_restriction)
    else:  # Day time occurrence
        or_zarua_restriction = ForbiddenDay(
            menstrual_period, 
            'אור זרוע', 
            standard_30_day_cycle.hebrew_date, 
            menstrual_period.time_of_day - 1
        )
        forbidden_days_list.insert(0, or_zarua_restriction)

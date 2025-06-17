"""
Output formatting utilities for the Tahara Calculator.

This module handles formatting and displaying calculation results.
"""

import sys
import os

# Add the parent directory to the Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from config.config_db import get_config

# Hebrew text mappings
TIME_OF_DAY_DICT = {0: "ליל", 1: "יום"}
WEEKDAY_DICT = {
    1: "ראשון",
    2: "שני", 
    3: "שלישי",
    4: "רביעי",
    5: "חמישי",
    6: "שישי",
    7: "שבת"
}


def format_output_lines(periods_indexed_by_date, historical_cycle_intervals):
    """
    Format the calculation results into output lines.
    
    Args:
        periods_indexed_by_date: Dictionary of periods indexed by Hebrew date
        historical_cycle_intervals: List of historical cycle intervals
        
    Returns:
        list: Formatted output lines ready for display or export
    """
    config = get_config()
    output_separator = config.get_date_separator()
    
    output_content_lines = []
    
    # Add cycle intervals if configured to show them
    if config.get("output.show_cycle_intervals", True):
        output_content_lines.append(f"רשימת הפלגות:\n{historical_cycle_intervals}\n{output_separator}\n")

    for period_date in periods_indexed_by_date:
        current_period = periods_indexed_by_date[period_date]
        
        # Add period header
        if config.get("output.show_hebrew_dates", True):
            period_header = (
                f"{period_date.hebrew_date_string()} "
                f"ב{TIME_OF_DAY_DICT[current_period.time_of_day]} "
                f"{WEEKDAY_DICT[period_date.weekday()]}:\n"
            )
        else:
            period_header = (
                f"Period {period_date.day}/{period_date.month}/{period_date.year} "
                f"ב{TIME_OF_DAY_DICT[current_period.time_of_day]} "
                f"{WEEKDAY_DICT[period_date.weekday()]}:\n"
            )
        output_content_lines.append(period_header)
        
        # Add forbidden days for this period
        for forbidden_day in current_period.forbidden_days_list:
            if isinstance(forbidden_day, list):
                # Handle unbroken patterns
                output_content_lines.append("  הפלגות שלא נעקרו:\n")
                for unbroken_pattern in forbidden_day:
                    pattern_line = _format_forbidden_day_line(unbroken_pattern, indent="    ")
                    output_content_lines.append(pattern_line)
            else:
                # Handle regular forbidden days
                forbidden_day_line = _format_forbidden_day_line(forbidden_day, indent="  ")
                output_content_lines.append(forbidden_day_line)
        
        output_content_lines.append(output_separator + "\n")
    
    return output_content_lines


def _format_forbidden_day_line(forbidden_day, indent="  "):
    """
    Format a single forbidden day into a display line.
    
    Args:
        forbidden_day: ForbiddenDay object to format
        indent: Indentation string for the line
        
    Returns:
        str: Formatted line for the forbidden day
    """
    return (
        f"{indent}{forbidden_day.restriction_name} - "
        f"{forbidden_day.hebrew_date.hebrew_date_string()} "
        f"ב{TIME_OF_DAY_DICT[forbidden_day.time_of_day]} "
        f"{WEEKDAY_DICT[forbidden_day.weekday]}\n"
    )


def print_results(output_content_lines):
    """
    Print results to console.
    
    Args:
        output_content_lines: List of formatted output lines
    """
    print("")
    for output_line in output_content_lines:
        print(output_line[:-1])

"""
Command-line interface for the Tahara Calculator.

This module provides the main CLI interface and coordinates
all other modules to perform the calculations.
"""

import sys
import os

# Add the parent directory to the Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils.file_operations import read_periods_list_file, export_results
from src.processor import (
    process_periods_data, 
    calculate_cycle_intervals, 
    calculate_all_forbidden_days, 
    create_periods_index
)
from utils.formatters import format_output_lines, print_results
from config.config_db import get_config


def get_input_file_path():
    """
    Get the input file path from command line arguments or user input.
    
    Returns:
        str: Path to the input file, or None if not found after retries
    """
    config = get_config()
    
    if len(sys.argv) > 1:
        input_file_path = sys.argv[1]
    else:
        default_file = config.get_default_input_file()
        input_file_path = input(f"Date data file not found. Please enter the date file path (default: {default_file}):\n")
        if not input_file_path.strip():
            input_file_path = default_file
    
    # Try to read the file up to the configured number of times
    max_attempts = config.get_max_retry_attempts()
    for file_read_attempt in range(max_attempts):
        period_dates_list = read_periods_list_file(input_file_path)
        if period_dates_list:
            return input_file_path, period_dates_list
        else:
            if file_read_attempt < max_attempts - 1:  # Don't prompt on last attempt
                default_file = config.get_default_input_file()
                input_file_path = input(f"Date data file not found. Please enter the date file path (default: {default_file}):\n")
                if not input_file_path.strip():
                    input_file_path = default_file
    
    return None, None


def get_output_file_path():
    """
    Get the output file path from command line arguments or config.
    
    Returns:
        str: Path to the output file, or None for console output
    """
    config = get_config()
    
    if len(sys.argv) > 2:
        return sys.argv[2]
    elif config.should_auto_export():
        return config.get_default_output_file()
    return None


def main():
    """Main entry point for the Tahara Calculator."""
    # Get input file and data
    input_file_path, period_dates_list = get_input_file_path()
    if not period_dates_list:
        print("Date data file not found.\n")
        sys.exit(1)

    # Get output file path (optional)
    output_file_path = get_output_file_path()

    # Process the data
    menstrual_periods_list = process_periods_data(period_dates_list)
    if not menstrual_periods_list:
        print("No valid periods found in input file.\n")
        sys.exit(1)

    # Calculate cycle intervals
    historical_cycle_intervals = calculate_cycle_intervals(menstrual_periods_list)

    # Calculate forbidden days for all periods
    calculate_all_forbidden_days(menstrual_periods_list, historical_cycle_intervals)

    # Create index for output formatting
    periods_indexed_by_date = create_periods_index(menstrual_periods_list)

    # Format output
    output_content_lines = format_output_lines(periods_indexed_by_date, historical_cycle_intervals)

    # Export or print results
    if output_file_path:
        export_results(output_file_path, output_content_lines)
    else:
        print_results(output_content_lines)


if __name__ == "__main__":
    main()

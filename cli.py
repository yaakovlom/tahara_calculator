"""
Command-line interface for the Tahara Calculator.

This module provides the main CLI interface and coordinates
all other modules to perform the calculations.
"""

import sys
from file_operations import read_periods_list_file, export_results
from processor import (
    process_periods_data, 
    calculate_cycle_intervals, 
    calculate_all_forbidden_days, 
    create_periods_index
)
from formatters import format_output_lines, print_results


def get_input_file_path():
    """
    Get the input file path from command line arguments or user input.
    
    Returns:
        str: Path to the input file, or None if not found after retries
    """
    if len(sys.argv) > 1:
        input_file_path = sys.argv[1]
    else:
        input_file_path = input("Date data file not found. Please enter the date file path:\n")
    
    # Try to read the file up to 3 times
    for file_read_attempt in range(3):
        period_dates_list = read_periods_list_file(input_file_path)
        if period_dates_list:
            return input_file_path, period_dates_list
        else:
            input_file_path = input("Date data file not found. Please enter the date file path:\n")
    
    return None, None


def get_output_file_path():
    """
    Get the output file path from command line arguments.
    
    Returns:
        str: Path to the output file, or None for console output
    """
    if len(sys.argv) > 2:
        return sys.argv[2]
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

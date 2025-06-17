"""
File I/O operations for the Tahara Calculator.

This module handles reading input files and exporting results.
"""

import os


def read_periods_list_file(file_path: str):
    """
    Read dates from file and return list of date strings.
    
    Args:
        file_path: Path to the input file containing period dates
        
    Returns:
        list: List of date strings, or None if file couldn't be read
    """
    try:
        if os.path.isfile(file_path):
            with open(file_path, "r", encoding='utf-8') as f:
                date_list = f.readlines()
            return [line.strip() for line in date_list if line.strip()]
        return None
    except (IOError, OSError) as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def export_results(file_name, lines):
    """
    Export results to a file.
    
    Args:
        file_name: Name of the output file
        lines: List of lines to write to the file
    """
    try:
        with open(file_name, "w", encoding='utf-8') as f:
            f.writelines(lines)
        print(f"Results exported to {file_name}")
    except (IOError, OSError) as e:
        print(f"Error writing to file {file_name}: {e}")

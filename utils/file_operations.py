"""
File I/O operations for the Tahara Calculator.

This module handles reading input files and exporting results.
"""

import os
import sys

# Add the parent directory to the Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from config.config_db import get_config


def read_periods_list_file(file_path: str):
    """
    Read dates from file and return list of date strings.
    
    Args:
        file_path: Path to the input file containing period dates
        
    Returns:
        list: List of date strings, or None if file couldn't be read
    """
    config = get_config()
    encoding = config.get_encoding()
    
    try:
        if os.path.isfile(file_path):
            with open(file_path, "r", encoding=encoding) as f:
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
    config = get_config()
    encoding = config.get_encoding()
    
    try:
        # Check if file exists and user wants confirmation
        if os.path.exists(file_name) and config.get("interface.confirm_overwrite", True):
            response = input(f"File '{file_name}' already exists. Overwrite? (y/N): ")
            if response.lower() not in ['y', 'yes']:
                print("Export cancelled.")
                return
        
        with open(file_name, "w", encoding=encoding) as f:
            f.writelines(lines)
        print(f"Results exported to {file_name}")
    except (IOError, OSError) as e:
        print(f"Error writing to file {file_name}: {e}")

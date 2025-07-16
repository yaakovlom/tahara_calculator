"""
Date management CLI for the Tahara Calculator.

This module provides command-line tools for adding and managing dates in input files.
"""

import sys
import os
from datetime import datetime

# Add the parent directory to the Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils.date_converter import (
    convert_gregorian_to_hebrew,
    format_hebrew_date_for_input,
    get_date_format_help,
    validate_date_input,
    parse_mixed_date_input
)
from config.config_db import get_config


def add_date_to_file(file_path: str, date_input: str) -> bool:
    """
    Add a date entry to an input file.
    
    Args:
        file_path: Path to the input file
        date_input: Date string to add
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Validate the date input
        if not validate_date_input(date_input):
            print(f"Invalid date format: {date_input}")
            print(get_date_format_help())
            return False
        
        # Parse the date to ensure it's valid
        result = parse_mixed_date_input(date_input)
        if not result:
            print(f"Could not parse date: {date_input}")
            return False
        
        hebrew_date, time_of_day = result
        formatted_entry = format_hebrew_date_for_input(hebrew_date, time_of_day)
        
        # Check if file exists, create if not
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(formatted_entry + '\n')
            print(f"Created new file '{file_path}' with date: {formatted_entry}")
            return True
        
        # Check if date already exists
        with open(file_path, 'r', encoding='utf-8') as f:
            existing_lines = f.readlines()
        
        existing_dates = [line.strip() for line in existing_lines if line.strip()]
        if formatted_entry in existing_dates:
            print(f"Date already exists in file: {formatted_entry}")
            return False
        
        # Add the new date
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(formatted_entry + '\n')
        
        print(f"Added date to '{file_path}': {formatted_entry}")
        print(f"Hebrew date: {hebrew_date.hebrew_date_string()}")
        return True
        
    except Exception as e:
        print(f"Error adding date to file: {e}")
        return False


def interactive_add_date():
    """Interactive mode for adding dates."""
    config = get_config()
    default_file = config.get_default_input_file()
    
    # Get file path
    file_path = input(f"Enter file path (default: {default_file}): ").strip()
    if not file_path:
        file_path = default_file
    
    print(get_date_format_help())
    
    while True:
        date_input = input("\nEnter date (or 'quit' to exit): ").strip()
        if date_input.lower() in ['quit', 'exit', 'q']:
            break
        
        if not date_input:
            continue
        
        if add_date_to_file(file_path, date_input):
            # Show current file contents
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                print(f"\nCurrent file contents ({len(lines)} entries):")
                for i, line in enumerate(lines[-5:], 1):  # Show last 5 entries
                    print(f"  {i}. {line.strip()}")
                if len(lines) > 5:
                    print(f"  ... and {len(lines) - 5} more entries")
            except:
                pass


def list_dates_in_file(file_path: str):
    """List all dates in a file with their Gregorian equivalents."""
    try:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            print(f"File is empty: {file_path}")
            return
        
        print(f"Dates in '{file_path}':")
        print("-" * 60)
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            
            result = parse_mixed_date_input(line)
            if result:
                hebrew_date, time_of_day = result
                gregorian_date = hebrew_date.to_pydate()
                time_str = "Night" if time_of_day == 0 else "Day"
                
                print(f"{i:2d}. {line}")
                print(f"    Hebrew: {hebrew_date.hebrew_date_string()}")
                print(f"    Gregorian: {gregorian_date.strftime('%d/%m/%Y')} ({time_str})")
                print()
            else:
                print(f"{i:2d}. {line} (INVALID FORMAT)")
                print()
        
    except Exception as e:
        print(f"Error listing dates: {e}")


def convert_date_command():
    """Interactive date conversion tool."""
    print("Date Conversion Tool")
    print("=" * 40)
    print(get_date_format_help())
    
    while True:
        date_input = input("\nEnter date to convert (or 'quit' to exit): ").strip()
        if date_input.lower() in ['quit', 'exit', 'q']:
            break
        
        if not date_input:
            continue
        
        # Try to parse as Gregorian first
        gregorian_parts = date_input.split()
        if len(gregorian_parts) >= 2:
            date_part = gregorian_parts[0]
            time_of_day = int(gregorian_parts[1]) if gregorian_parts[1] in ['0', '1'] else 1
            
            hebrew_date = convert_gregorian_to_hebrew(date_part)
            if hebrew_date:
                print(f"  Gregorian: {date_part}")
                print(f"  Hebrew: {hebrew_date.hebrew_date_string()}")
                print(f"  Input format: {format_hebrew_date_for_input(hebrew_date, time_of_day)}")
                continue
        
        # Try to parse as complete date input
        result = parse_mixed_date_input(date_input)
        if result:
            hebrew_date, time_of_day = result
            gregorian_date = hebrew_date.to_pydate()
            time_str = "Night" if time_of_day == 0 else "Day"
            
            print(f"  Input: {date_input}")
            print(f"  Hebrew: {hebrew_date.hebrew_date_string()} ({time_str})")
            print(f"  Gregorian: {gregorian_date.strftime('%d/%m/%Y')} ({time_str})")
        else:
            print(f"  Invalid date format: {date_input}")
            print("  Please check the format and try again.")


def main():
    """Main entry point for date management CLI."""
    if len(sys.argv) < 2:
        print("Usage: python dates_cli.py <command> [arguments]")
        print("Commands:")
        print("  add [file] [date]     - Add a date to file")
        print("  list [file]           - List dates in file")
        print("  convert               - Interactive date conversion")
        print("  interactive           - Interactive date entry mode")
        print("  help                  - Show help")
        return
    
    command = sys.argv[1].lower()
    
    if command == "add":
        if len(sys.argv) >= 4:
            file_path = sys.argv[2]
            date_input = " ".join(sys.argv[3:])
            add_date_to_file(file_path, date_input)
        else:
            interactive_add_date()
    
    elif command == "list":
        if len(sys.argv) >= 3:
            file_path = sys.argv[2]
        else:
            config = get_config()
            file_path = config.get_default_input_file()
        list_dates_in_file(file_path)
    
    elif command == "convert":
        convert_date_command()
    
    elif command == "interactive":
        interactive_add_date()
    
    elif command == "help":
        print(get_date_format_help())
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()

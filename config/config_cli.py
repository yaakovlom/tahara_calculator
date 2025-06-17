"""
Configuration management CLI for the Tahara Calculator.

This module provides command-line interface for managing configuration settings.
"""

import sys
import os

# Add the parent directory to the Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from config.config_db import get_config, save_config


def show_config():
    """Display the current configuration."""
    config = get_config()
    config.print_config()


def set_config_value():
    """Set a configuration value interactively or via command line."""
    config = get_config()
    
    # Check if we have command line arguments for automated setting
    if len(sys.argv) >= 5:  # set category key value
        category = sys.argv[2]
        key = sys.argv[3]
        value = sys.argv[4]
    else:
        print("Available configuration categories:")
        print("1. files - File settings")
        print("2. output - Output formatting")
        print("3. calculations - Calculation options")
        print("4. interface - Interface behavior")
        print("5. hebrew_calendar - Hebrew calendar settings")
        
        category = input("Enter category name: ").strip()
        if not category:
            print("No category specified.")
            return
        
        key = input("Enter setting key: ").strip()
        if not key:
            print("No key specified.")
            return
        
        value = input("Enter new value: ").strip()
        if not value:
            print("No value specified.")
            return
    
    # Try to convert value to appropriate type
    if value.lower() in ['true', 'false']:
        value = value.lower() == 'true'
    elif value.isdigit():
        value = int(value)
    elif value.replace('.', '', 1).isdigit():
        value = float(value)
    
    key_path = f"{category}.{key}"
    config.set(key_path, value)
    
    if config.save_config():
        print(f"Configuration updated: {key_path} = {value}")
    else:
        print("Failed to save configuration.")


def reset_config():
    """Reset configuration to defaults."""
    response = input("Are you sure you want to reset all configuration to defaults? (y/N): ")
    if response.lower() in ['y', 'yes']:
        config = get_config()
        config.reset_to_defaults()
        if config.save_config():
            print("Configuration reset to defaults.")
        else:
            print("Failed to save configuration.")
    else:
        print("Reset cancelled.")


def config_help():
    """Show configuration help."""
    print("""
Configuration Management Commands:

python config_cli.py show                 - Show current configuration
python config_cli.py set                  - Set a configuration value
python config_cli.py reset                - Reset to default configuration
python config_cli.py help                 - Show this help

Common Configuration Settings:

files.default_input_file       - Default input file name
files.default_output_file      - Default output file name
output.auto_export            - Automatically export to file (true/false)
output.show_hebrew_dates      - Show Hebrew date format (true/false)
interface.max_file_retry_attempts - Maximum file retry attempts (number)
interface.confirm_overwrite   - Confirm before overwriting files (true/false)

Example:
python config_cli.py set
  Category: files
  Key: default_input_file
  Value: my_dates.txt
""")


def main():
    """Main configuration CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python config_cli.py <command>")
        print("Commands: show, set, reset, help")
        return
    
    command = sys.argv[1].lower()
    
    if command == "show":
        show_config()
    elif command == "set":
        set_config_value()
    elif command == "reset":
        reset_config()
    elif command == "help":
        config_help()
    else:
        print(f"Unknown command: {command}")
        print("Available commands: show, set, reset, help")


if __name__ == "__main__":
    main()

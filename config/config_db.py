"""
Configuration management for the Tahara Calculator.

This module provides a simple configuration database using JSON
to store user preferences and default settings.
"""

import json
import os
from typing import Any, Dict, Optional


class ConfigDB:
    """Simple JSON-based configuration database."""
    
    def __init__(self, config_file: str = "config.json"):
        """
        Initialize the configuration database.
        
        Args:
            config_file: Path to the configuration file
        """
        self.config_file = config_file
        self.config_data = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default config."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config file: {e}")
                return self._get_default_config()
        else:
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration settings."""
        return {
            "files": {
                "default_input_file": "dates.txt",
                "default_output_file": "tahara_results.txt",
                "sample_file": "sample_dates.txt"
            },
            "output": {
                "auto_export": False,
                "show_hebrew_dates": True,
                "show_cycle_intervals": True,
                "date_separator": "-" * 25,
                "encoding": "utf-8"
            },
            "calculations": {
                "include_or_zarua": True,
                "include_kartyupleity": True,
                "include_standard_cycles": True,
                "include_personal_intervals": True,
                "include_unbroken_patterns": True
            },
            "interface": {
                "max_file_retry_attempts": 3,
                "show_parsing_errors": True,
                "confirm_overwrite": True
            },
            "hebrew_calendar": {
                "default_year": 5785,
                "date_format": "day/month/year"
            }
        }
    
    def save_config(self) -> bool:
        """
        Save current configuration to file.
        
        Returns:
            bool: True if saved successfully, False otherwise
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error saving config file: {e}")
            return False
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.
        
        Args:
            key_path: Dot-separated path to the config value (e.g., "files.default_input_file")
            default: Default value if key is not found
            
        Returns:
            The configuration value or default
        """
        keys = key_path.split('.')
        value = self.config_data
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any) -> None:
        """
        Set a configuration value using dot notation.
        
        Args:
            key_path: Dot-separated path to the config value
            value: Value to set
        """
        keys = key_path.split('.')
        config = self.config_data
        
        # Navigate to the parent of the target key
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # Set the final value
        config[keys[-1]] = value
    
    def get_default_input_file(self) -> str:
        """Get the default input file name."""
        return self.get("files.default_input_file", "dates.txt")
    
    def get_default_output_file(self) -> str:
        """Get the default output file name."""
        return self.get("files.default_output_file", "tahara_results.txt")
    
    def get_sample_file(self) -> str:
        """Get the sample file name."""
        return self.get("files.sample_file", "sample_dates.txt")
    
    def should_auto_export(self) -> bool:
        """Check if auto-export is enabled."""
        return self.get("output.auto_export", False)
    
    def get_max_retry_attempts(self) -> int:
        """Get maximum file retry attempts."""
        return self.get("interface.max_file_retry_attempts", 3)
    
    def get_date_separator(self) -> str:
        """Get the date separator for output formatting."""
        return self.get("output.date_separator", "-" * 25)
    
    def should_show_parsing_errors(self) -> bool:
        """Check if parsing errors should be displayed."""
        return self.get("interface.show_parsing_errors", True)
    
    def get_encoding(self) -> str:
        """Get the file encoding setting."""
        return self.get("output.encoding", "utf-8")
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to default values."""
        self.config_data = self._get_default_config()
    
    def update_config(self, updates: Dict[str, Any]) -> None:
        """
        Update multiple configuration values.
        
        Args:
            updates: Dictionary of key_path -> value pairs
        """
        for key_path, value in updates.items():
            self.set(key_path, value)
    
    def get_all_config(self) -> Dict[str, Any]:
        """Get the entire configuration dictionary."""
        return self.config_data.copy()
    
    def print_config(self) -> None:
        """Print the current configuration in a readable format."""
        print("Current Configuration:")
        print("=" * 50)
        self._print_config_section(self.config_data)
    
    def _print_config_section(self, section: Dict[str, Any], indent: int = 0) -> None:
        """Recursively print configuration sections."""
        for key, value in section.items():
            if isinstance(value, dict):
                print("  " * indent + f"{key}:")
                self._print_config_section(value, indent + 1)
            else:
                print("  " * indent + f"{key}: {value}")


# Global configuration instance
config_db = ConfigDB()


def get_config() -> ConfigDB:
    """Get the global configuration instance."""
    return config_db


def save_config() -> bool:
    """Save the global configuration."""
    return config_db.save_config()

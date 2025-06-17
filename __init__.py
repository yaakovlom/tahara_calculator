"""
Tahara Calculator Package

A modular Hebrew calendar calculator for determining forbidden days
based on menstrual periods and religious observance rules.

Modules:
    models: Core data structures (MenstrualPeriod, ForbiddenDay)
    hebrew_calendar_utils: Hebrew calendar utility functions
    file_operations: File I/O operations
    parsers: Text parsing utilities
    calculations: Core calculation engine
    formatters: Output formatting utilities
    processor: Main processing logic
    cli: Command-line interface
"""

__version__ = "1.0.0"
__author__ = "Yaakov Lombard"

# Import main classes for easy access
from src.models import MenstrualPeriod, ForbiddenDay
from . import main

# Define what gets imported with "from tahara_calculator import *"
__all__ = [
    'MenstrualPeriod',
    'ForbiddenDay', 
    'main'
]

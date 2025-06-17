# Tahara Calculator

A Hebrew calendar-based calculator for determining forbidden days (prohibited periods) in accordance with Jewish religious law (Niddah/Family Purity laws).

## Overview

The Tahara Calculator processes menstrual period data and calculates various types of forbidden days based on Hebrew calendar calculations, including:

- **עונה בינונית** (Standard intervals) - 30 and 31 day cycles
- **וסת החודש** (Monthly cycle) - Based on Hebrew month length
- **הפלגה** (Personal intervals) - Individual cycle patterns
- **אור זרוע** and **כרתי ופלתי** - Additional restrictions based on time of day
- **הפלגות שלא נעקרו** (Unbroken patterns) - Historical interval patterns

## Features

- ✅ **Modular Architecture** - Clean separation of concerns across multiple modules
- ✅ **Hebrew Calendar Support** - Full integration with Hebrew dates via `pyluach`
- ✅ **Multiple Output Formats** - Console display or file export
- ✅ **Error Handling** - Robust parsing and validation of input data
- ✅ **Extensible Design** - Easy to add new calculation rules or output formats

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup

1. Clone or download the project files
2. Navigate to the project directory:
   ```cmd
   cd c:\Users\yaakovl\Documents\python\tahara_calculator
   ```

3. Install required dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

Run the calculator with an input file:

```cmd
python main.py sample_dates.txt
```

### Export to File

Save results to a file:

```cmd
python main.py sample_dates.txt output.txt
```

### Input File Format

Create a text file with one period per line in the format:
```
day/month/year time_of_day
```

Where:
- `day/month/year` - Hebrew calendar date (e.g., `8/12/5785`)
- `time_of_day` - `0` for night (ליל) or `1` for day (יום)

Example (`sample_dates.txt`):
```
8/12/5785 0
9/11/5785 1
10/10/5785 0
11/8/5785 1
```

## Project Structure

```
tahara_calculator/
├── main.py                    # Main entry point
├── cli.py                     # Command-line interface
├── models.py                  # Data model classes
├── parsers.py                 # Input parsing utilities
├── calculations.py            # Core calculation engine
├── processor.py               # Data processing coordination
├── formatters.py              # Output formatting
├── file_operations.py         # File I/O operations
├── hebrew_calendar_utils.py   # Hebrew calendar utilities
├── requirements.txt           # Python dependencies
├── sample_dates.txt          # Example input file
└── README.md                 # This file
```

### Module Descriptions

#### Core Modules

- **`models.py`** - Defines `MenstrualPeriod` and `ForbiddenDay` classes
- **`calculations.py`** - Main calculation logic for forbidden days
- **`parsers.py`** - Converts text input to period objects
- **`processor.py`** - Coordinates data processing workflow

#### Interface Modules

- **`cli.py`** - Command-line interface and user interaction
- **`formatters.py`** - Output formatting and Hebrew text display
- **`file_operations.py`** - File reading and writing operations

#### Utility Modules

- **`hebrew_calendar_utils.py`** - Hebrew calendar helper functions
- **`main.py`** - Application entry point

## Output Format

The calculator produces Hebrew text output showing:

1. **רשימת הפלגות** (List of intervals) - Cycle intervals between periods
2. **Period Details** - For each period:
   - Hebrew date and time of day
   - List of forbidden days with their Hebrew dates and times

Example output:
```
רשימת הפלגות:
[30, 29, 60]
-------------------------
ח׳ אדר תשפ״ה בליל שבת:
  אור זרוע - ז׳ ניסן תשפ״ה ביום שבת
  עונה בינונית 30 - ח׳ ניסן תשפ״ה בליל ראשון
  כרתי ופלתי - ח׳ ניסן תשפ״ה ביום ראשון
  וסת החודש - ח׳ ניסן תשפ״ה בליל ראשון
  עונה בינונית 31 - ט׳ ניסן תשפ״ה בליל שני
-------------------------
```

## Dependencies

- **`pyluach`** (>=2.2.0) - Hebrew calendar library for date calculations and conversions

## Error Handling

The application handles various error conditions:

- **Missing input files** - Prompts user for valid file path (up to 3 attempts)
- **Invalid date formats** - Skips invalid entries with error messages
- **Empty input files** - Exits gracefully with informative message
- **File I/O errors** - Reports specific file operation failures

## Development

### Adding New Calculation Rules

To add new forbidden day calculations:

1. Add the logic to `calculations.py` in the `calculate_forbidden_days()` function
2. Update the `ForbiddenDay` model if new properties are needed
3. Modify output formatting in `formatters.py` if required

### Adding New Output Formats

To support additional output formats:

1. Create new formatting functions in `formatters.py`
2. Add command-line options in `cli.py`
3. Update the main workflow in `processor.py`

### Testing

Test the application with various input scenarios:

```cmd
# Test with sample data
python main.py sample_dates.txt

# Test with invalid data
python main.py test_invalid.txt

# Test export functionality
python main.py sample_dates.txt output.txt
```

## Religious Context

This calculator is designed to assist with the observance of Jewish family purity laws (Hilchot Niddah). The calculations are based on traditional Hebrew calendar rules and rabbinic guidelines for determining prohibited periods.

**Important Note**: This software is provided for educational and convenience purposes only. For actual religious observance, always consult with a qualified rabbi or halachic authority.

## License

This project is provided as-is for educational and personal use.

## Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes following the existing code style
4. Test thoroughly with various input scenarios
5. Submit a pull request with a clear description of changes

## Support

For questions or issues:

- Check the error messages for common problems
- Ensure input files follow the correct format
- Verify that all dependencies are installed
- Review the example files for proper usage patterns

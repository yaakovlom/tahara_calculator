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
- ✅ **Date Conversion Tools** - Convert between Gregorian and Hebrew calendar dates
- ✅ **CLI Date Management** - Interactive tools for adding and managing dates
- ✅ **Multiple Input Formats** - Support for various date formats (DD/MM/YYYY, YYYY-MM-DD, etc.)
- ✅ **Multiple Output Formats** - Console display or file export
- ✅ **Configuration Management** - JSON-based settings with CLI management
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

### Date Management CLI

#### Adding Dates

Add dates to your input file using familiar Gregorian dates:

```cmd
# Add a single date
python cli\dates_cli.py add dates.txt "15/03/2024 1"

# Interactive mode for multiple dates
python cli\dates_cli.py interactive

# View current dates
python cli\dates_cli.py list dates.txt

# Show help
python cli\dates_cli.py help
```

#### Supported Date Formats

The system accepts both Hebrew and Gregorian dates:

**Gregorian Calendar:**
- `15/03/2024 1` (DD/MM/YYYY format)
- `15-03-2024 1` (DD-MM-YYYY format)
- `2024-03-15 1` (YYYY-MM-DD format)

**Hebrew Calendar:**
- `8/12/5785 0` (day/month/year format)

**Special Keywords:**
- `today 1` (Current date, day)
- `today 0` (Current date, night)

**Time of Day:**
- `0` = Night (ליל)
- `1` = Day (יום)

**Examples:**
```cmd
# Add today's date (day)
python cli\dates_cli.py add dates.txt "today 1"

# Add today's date (night)
python cli\dates_cli.py add dates.txt "today 0"

# Add specific Gregorian date
python cli\dates_cli.py add dates.txt "15/03/2024 1"

# Add Hebrew date
python cli\dates_cli.py add dates.txt "8/12/5785 0"
```

#### Configuration Management

Manage application settings:

```cmd
# View current configuration
python config\config_cli.py show

# Update settings
python config\config_cli.py set files.default_input_file "my_dates.txt"
python config\config_cli.py set output.auto_export false

# Reset to defaults
python config\config_cli.py reset
```

### Input File Format

Create a text file with one period per line in the format:
```
day/month/year time_of_day
```

Where:
- `day/month/year` - Hebrew calendar date (e.g., `8/12/5785`)
- `time_of_day` - `0` for night (ליל) or `1` for day (יום)

**Note:** You can now input Gregorian dates which will be automatically converted to Hebrew format.

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
├── cli/                       # Command-line interface tools
│   ├── dates_cli.py          # Date management CLI
│   └── cli.py                # Main CLI interface
├── src/                       # Core application logic
│   ├── models.py             # Data model classes
│   ├── parsers.py            # Input parsing utilities
│   ├── calculations.py       # Core calculation engine
│   └── processor.py          # Data processing coordination
├── utils/                     # Utility modules
│   ├── date_converter.py     # Date conversion utilities
│   ├── formatters.py         # Output formatting
│   ├── file_operations.py    # File I/O operations
│   └── hebrew_calendar_utils.py # Hebrew calendar utilities
├── config/                    # Configuration management
│   ├── config_db.py          # JSON configuration database
│   └── config_cli.py         # Configuration CLI
├── tests/                     # Test files and examples
│   ├── sample_dates.txt      # Example input file
│   └── test_*.txt            # Test data files
├── docs/                      # Documentation
│   └── README.md             # Detailed documentation
├── requirements.txt           # Python dependencies
├── config.json               # Application configuration
└── dates.txt                 # Default input file
```

### Module Descriptions

#### Core Modules (`src/`)

- **`models.py`** - Defines `MenstrualPeriod` and `ForbiddenDay` classes
- **`calculations.py`** - Main calculation logic for forbidden days
- **`parsers.py`** - Converts text input to period objects (supports both Hebrew and Gregorian dates)
- **`processor.py`** - Coordinates data processing workflow

#### CLI Tools (`cli/`)

- **`dates_cli.py`** - Interactive date management, adding dates, format conversion
- **`cli.py`** - Main command-line interface and user interaction

#### Utilities (`utils/`)

- **`date_converter.py`** - Gregorian to Hebrew date conversion
- **`formatters.py`** - Output formatting and Hebrew text display
- **`file_operations.py`** - File reading and writing operations
- **`hebrew_calendar_utils.py`** - Hebrew calendar helper functions

#### Configuration (`config/`)

- **`config_db.py`** - JSON-based configuration database with dot-notation access
- **`config_cli.py`** - Configuration management CLI

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

1. Add the logic to `src/calculations.py` in the `calculate_forbidden_days()` function
2. Update the `ForbiddenDay` model in `src/models.py` if new properties are needed
3. Modify output formatting in `utils/formatters.py` if required

### Adding New Date Formats

To support additional date input formats:

1. Extend the parsing logic in `utils/date_converter.py`
2. Update the `parse_mixed_date_input()` function for new formats
3. Add validation in `validate_date_input()` function
4. Update help text in `get_date_format_help()` function

### Extending CLI Features

To add new CLI commands:

1. Add command logic to `cli/dates_cli.py` or create new CLI modules
2. Update the main command parser in the `main()` function
3. Add help text and usage examples

### Adding New Output Formats

To support additional output formats:

1. Create new formatting functions in `utils/formatters.py`
2. Add command-line options in `cli/cli.py`
3. Update the main workflow in `src/processor.py`

### Configuration Management

To modify application settings:

1. Edit `config.json` directly, or
2. Use the configuration CLI: `python config/config_cli.py`
3. Access settings in code via `config.config_db.get_config()`

### Testing

Test the application with various input scenarios:

```cmd
# Test with sample data
python main.py tests/sample_dates.txt

# Test with mixed date formats (includes "today" keyword)
python main.py tests/test_mixed.txt

# Test with all supported date formats
python main.py tests/test_all_formats_clean.txt

# Test "today" keyword specifically
python main.py tests/test_today_clean.txt

# Test with invalid data
python main.py tests/test_invalid.txt

# Test export functionality
python main.py tests/sample_dates.txt tests/output.txt

# Test date CLI tools
python cli/dates_cli.py add dates.txt "today 1"
python cli/dates_cli.py add dates.txt "15/03/2024 1"
python cli/dates_cli.py list dates.txt

# Test configuration CLI
python config/config_cli.py show
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

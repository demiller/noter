# Noter

A Python script for managing daily notes in [Obsidian](https://obsidian.md/) with timestamp support.

![Version](https://img.shields.io/badge/version-v1.1.2-blue)

## Description

Noter (v1.1.2) is a simple command-line utility designed to help you quickly add timestamped notes to your daily note files in Obsidian. It intelligently integrates with your existing Obsidian templates and adds entries to the "Notes & Observations" section of your daily notes.

The script automatically:
- Creates new daily note files if they don't exist (with full YAML frontmatter)
- Adds timestamped entries to existing daily notes
- Maintains proper spacing and bullet point formatting
- Preserves your existing Obsidian template structure
- Inserts notes in the appropriate section of your daily note

## Requirements

- Python 3.11 or higher
- Windows, macOS, or Linux operating system
- An existing Obsidian vault

## Installation

### Option 1: Run as a Python Script

1. Clone this repository:
   ```
   git clone https://github.com/demiller/noter.git
   cd noter
   ```

2. Create a `config.json` file in the same directory:
   ```json
   {
       "obsidian_vault_path": "C:/Users/DougMiller/OneDrive - Brightworks Group, LLC/Obsidian_Vault/Daily Notes"
   }
   ```

3. Update the vault path in `config.json` to match your Obsidian vault location.

4. Run the script:
   ```
   python noter.py
   ```

### Option 2: Use the Executable (Windows Only)

1. Download the latest release from the [releases page](https://github.com/demiller/noter/releases).
2. Create or copy the `config.json` file to the same directory as noter.exe
3. Update the vault path in `config.json`
4. Run `noter.exe`

### Option 3: Compile Your Own Executable

1. Install PyInstaller:
   ```
   pip install pyinstaller
   ```

2. Compile the script:
   ```
   pyinstaller --onefile noter.py
   ```

3. The executable will be created in the `dist` directory
4. Copy `config.json` to the same directory as the executable

### Adding to System PATH (Windows)

To run noter from any directory:

1. Copy both `noter.exe` and `config.json` to a directory in your PATH (e.g., `C:\Users\DougMiller\bin`)
2. Update the vault path in the copied `config.json`
3. You can now run `noter` from any directory

## Usage

1. Run the script or executable:
   ```
   python noter.py
   ```
   or 
   ```
   .\noter.exe
   ```

2. When prompted, enter the note you want to add:
   ```
   Enter the note you want to append: Had a meeting with the marketing team about Q3 strategy
   ```

3. The note will be added to today's daily note with a timestamp:
   ```
   - [15:42] Had a meeting with the marketing team about Q3 strategy
   ```

## Features

- **Automatic Timestamping**: Each note is automatically prefixed with the current time in `[HH:MM]` format.
- **Daily Organization**: Notes are organized by date in individual daily note files (YYYY-MM-DD.md).
- **YAML Frontmatter**: Automatically adds complete YAML frontmatter for new notes.
- **Template Compatible**: Works with your existing Obsidian daily note templates.
- **Section Awareness**: Intelligently adds notes to the "Notes & Observations" section.
- **Smart Formatting**: 
  - Adds notes directly after existing bullets without extra spacing
  - Only adds empty bullets in empty sections
  - Maintains clean formatting between notes
- **Simple Interface**: Minimalist command-line interface for quick note capture.

## Configuration

### Configuration File

Noter uses a `config.json` file for all configuration settings. This file should be located in the same directory as the script or executable. The first time you run noter without a config file, it will create a default one that you'll need to update.

Example `config.json`:
```json
{
    "obsidian_vault_path": "C:/Users/DougMiller/OneDrive - Brightworks Group, LLC/Obsidian_Vault/Daily Notes"
}
```

Important notes:
- Use forward slashes (/) in the path, even on Windows systems
- The config file must be in the same directory as the script/executable
- You must update the path to match your actual Obsidian vault location
- When moving the executable, always bring the config file with it

If you're using the Windows PATH installation method, make sure to:
1. Keep both the executable and config file in the same directory (e.g., `C:\Users\DougMiller\bin`)
2. Always edit the config file in that location, not in the original directory

## Daily Note Format

The script creates and works with daily note files following this structure:

```markdown
---
title: "Daily Note - YYYY-MM-DD"
status: active
topic: daily-log
reviewed: YYYY-MM-DD
priority: 3
created: YYYY-MM-DD
tags: [dailynotes, log]
aliases: []
---

# 📅️ Weekday, Month DDth YYYY

## ☀️ Summary

> What happened today? What did you think about? What patterns or themes emerged?
- 

## ✅ Tasks

- 

## 🔁 Reviews or Highlights Revisited

\```dataview
list
from ""
where reviewed <= date(today) - dur(30 days)
sort reviewed asc
limit 5
\```

## 📓 Notes Created or Touched Today

\```dataview
table file.name, file.mtime
from ""
where file.mtime >= date(today)
sort file.mtime desc
\```

## ✍️ Notes & Observations

- [HH:MM] Your note content here
- 
```

The script will:
1. Create this complete structure if the file doesn't exist
2. Find the "## ✍️ Notes & Observations" section
3. Add new notes after any existing notes
4. Add an empty bullet only when the section is empty
5. Preserve proper spacing between notes
6. Maintain all other content in the file

## Note Insertion Rules

The script follows these rules when adding notes:

1. **New File**: Creates a complete template with YAML frontmatter and all sections
2. **Empty Section**: Adds the note followed by an empty bullet
3. **Existing Notes**: 
   - Adds the new note directly after the last existing note
   - Maintains single-line spacing between notes
   - Does not add empty bullets after existing content
4. **Formatting**: Always maintains proper spacing and bullet point structure

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development

### Setting Up Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/demiller/noter.git
   cd noter
   ```

2. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

### Running Tests

The project uses pytest for testing. To run the tests:

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=noter

# Run a specific test file
pytest tests/test_note_manager.py

# Run tests matching a pattern
pytest -k "test_append"
```

### Code Style and Linting

The project uses several tools to ensure code quality:

- Black for code formatting
- isort for import sorting
- flake8 for style guide enforcement
- mypy for type checking

To check code style:

```bash
# Format code with black
black .

# Sort imports
isort .

# Run flake8
flake8 .

# Run type checking
mypy noter tests
```

### Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes, ensuring:
   - All tests pass
   - Code is formatted with black
   - Imports are sorted with isort
   - No flake8 warnings
   - Type hints are complete and mypy passes
   - New features have tests
4. Update documentation as needed
5. Submit a pull request

The CI pipeline will automatically:
- Run tests on multiple Python versions
- Check code coverage
- Verify code formatting and style
- Run type checking

### Release Process

1. Update version number in both `setup.py` and `noter/__init__.py`
2. Update CHANGELOG.md
3. Create and push a new tag
4. GitHub Actions will automatically:
   - Run all tests
   - Build the package
   - Create a new release

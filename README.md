# Noter

A Python script for managing daily notes in [Obsidian](https://obsidian.md/) with timestamp support.

## Description

Noter is a simple command-line utility designed to help you quickly add timestamped notes to your daily note files in Obsidian. It intelligently integrates with your existing Obsidian templates and adds entries to the "Notes & Observations" section of your daily notes.

The script automatically:
- Creates new daily note files if they don't exist
- Adds timestamped entries to existing daily notes
- Preserves your existing Obsidian template structure
- Inserts notes in the appropriate section of your daily note

## Requirements

- Python 3.6 or higher
- Windows, macOS, or Linux operating system
- An existing Obsidian vault

## Installation

### Option 1: Run as a Python Script

1. Clone this repository:
   ```
   git clone https://github.com/demiller/noter.git
   cd noter
   ```

2. Configure the Obsidian vault path in `noter.py`:
   ```python
   # Configure your Obsidian Vault Path here
   OBSIDIAN_VAULT_PATH = r"YOUR_OBSIDIAN_VAULT_PATH\Daily Notes"
   ```

3. Run the script:
   ```
   python noter.py
   ```

### Option 2: Use the Executable (Windows Only)

1. Download the latest release from the [releases page](https://github.com/demiller/noter/releases).
2. Run `noter.exe`

### Option 3: Compile Your Own Executable

1. Install PyInstaller:
   ```
   pip install pyinstaller
   ```

2. Compile the script:
   ```
   pyinstaller --onefile noter.py
   ```

3. The executable will be created in the `dist` directory.

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
- **Template Compatible**: Works with your existing Obsidian daily note templates.
- **Section Awareness**: Intelligently adds notes to the "Notes & Observations" section.
- **Simple Interface**: Minimalist command-line interface for quick note capture.

## Configuration

The main configuration is the path to your Obsidian vault's Daily Notes folder. You can modify this in the `noter.py` file:

```python
# Configure your Obsidian Vault Path here
OBSIDIAN_VAULT_PATH = r"C:\Users\DougMiller\OneDrive - Brightworks Group, LLC\Obsidian_Vault\Daily Notes"
```

Replace this with the path to your own Obsidian vault's Daily Notes folder.

## Daily Note Format

The script expects and works with daily note files following this structure:

```markdown
# Daily Note - YYYY-MM-DD

## ✍️ Notes & Observations

- [HH:MM] Your note content here

## ✅ Tasks

...other content...
```

The script will:
1. Create this basic structure if the file doesn't exist
2. Find the "## ✍️ Notes & Observations" section if it exists
3. Add notes before the "## ✅ Tasks" section
4. Preserve all other content in the file

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


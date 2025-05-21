# Top level noter.py file that provides backward compatibility
# while using the new modular structure

import argparse
import logging
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional

# Setup basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("noter")


# Path utilities
def get_script_dir() -> str:
    """Get the directory where the script/executable is located"""
    if getattr(sys, "frozen", False):
        # Running as executable
        return os.path.dirname(sys.executable)
    else:
        # Running as script
        return os.path.dirname(os.path.abspath(__file__))


# Configuration management
class ConfigManager:
    """Manages the noter configuration"""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or os.path.join(get_script_dir(), "config.json")
        self.default_config = {
            "obsidian_vault_path": "C:/Users/YourUsername/Obsidian Vault/Daily Notes",
            "date_format": "%Y-%m-%d",
            "time_format": "%H:%M",
            "template_path": None,
        }

    def load_config(self) -> Optional[Dict]:
        """Load configuration from file or create a default one"""
        import json

        try:
            if not os.path.exists(self.config_path):
                with open(self.config_path, "w", encoding="utf-8") as f:
                    json.dump(self.default_config, f, indent=4)
                logger.info(f"Configuration file created at: {os.path.abspath(self.config_path)}")
                logger.info("Please update the Obsidian vault path in the config file before continuing.")
                return None

            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)

            # Validate the vault path exists
            if not os.path.exists(config["obsidian_vault_path"]):
                logger.error(f"Error: Obsidian vault directory not found at: {config['obsidian_vault_path']}")
                logger.error(f"Please update the path in {self.config_path}")
                return None

            return config

        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return None


# Template management
class TemplateManager:
    """Manages note templates"""

    def __init__(self, config: Dict):
        self.config = config
        self.custom_template_path = config.get("template_path")

    def create_basic_template(self, note_date: str, note_content: str) -> str:
        """Create a basic template for a new daily note"""
        # Use custom template if available
        if self.custom_template_path and os.path.exists(self.custom_template_path):
            try:
                return self._load_custom_template(note_date, note_content)
            except Exception as e:
                logger.error(f"Error loading custom template: {e}")
                # Fall back to default template

        today = datetime.now()
        weekday = today.strftime("%A")

        template = f"""---
title: "Daily Note - {note_date}"
status: active
topic: daily-log
reviewed: {note_date}
priority: 3
created: {note_date}
tags: [dailynotes, log]
aliases: []
---

# 📅️ {weekday}, {today.strftime("%B %d")}th {today.year}

## ☀️ Summary

> What happened today? What did you think about? What patterns or themes emerged?
- 

## ✅ Tasks

- 

## 🔁 Reviews or Highlights Revisited

```dataview
list
from ""
where reviewed <= date(today) - dur(30 days)
sort reviewed asc
limit 5
```

## 📓 Notes Created or Touched Today

```dataview
table file.name, file.mtime
from ""
where file.mtime >= date(today)
sort file.mtime desc
```

## ✍️ Notes & Observations

{note_content}
- """
        return template

    def _load_custom_template(self, note_date: str, note_content: str) -> str:
        """Load and populate a custom template from file"""
        with open(self.custom_template_path, "r", encoding="utf-8") as f:
            template = f.read()

        # Replace template variables
        today = datetime.now()
        variables = {
            "{{note_date}}": note_date,
            "{{weekday}}": today.strftime("%A"),
            "{{month}}": today.strftime("%B"),
            "{{day}}": today.strftime("%d"),
            "{{year}}": str(today.year),
            "{{note_content}}": note_content,
        }

        for var, value in variables.items():
            template = template.replace(var, value)

        return template


# Note management
class NoteManager:
    """Manages notes and their addition to files"""

    def __init__(self, config: Dict, template_manager: TemplateManager):
        self.config = config
        self.template_manager = template_manager

    def get_note_path(self, note_date: str) -> str:
        """Get the full path to a daily note file"""
        return os.path.join(self.config["obsidian_vault_path"], f"{note_date}.md")

    def append_to_note(self, note: str, note_date: str, tags: Optional[List[str]] = None) -> bool:
        """Add a note to the Notes & Observations section of the daily note file"""
        import re

        try:
            note_path = self.get_note_path(note_date)
            timestamp = datetime.now().strftime(self.config.get("time_format", "%H:%M"))

            # Format the note with tags if provided
            tag_str = ""
            if tags and len(tags) > 0:
                tag_str = f" #{' #'.join(tags)}"

            formatted_note = f"- [{timestamp}] {note}{tag_str}\n"

            if not os.path.exists(note_path):
                with open(note_path, "w", encoding="utf-8") as file:
                    file.write(self.template_manager.create_basic_template(note_date, formatted_note.rstrip()))
                logger.info(f"Created new daily note file for {note_date}")
                return True

            with open(note_path, "r", encoding="utf-8") as file:
                lines = file.readlines()

            # Find the Notes & Observations section
            notes_start = -1
            for i, line in enumerate(lines):
                if "## ✍️ Notes & Observations" in line:
                    notes_start = i
                    break

            if notes_start == -1:
                logger.error("Could not find Notes & Observations section")
                return False

            # Find the empty bullet or the end of the section
            section_end = len(lines)
            empty_bullet = -1
            last_bullet = notes_start

            for i in range(notes_start + 1, len(lines)):
                current_line = lines[i].rstrip()

                # Check for next section
                if current_line.startswith("## "):
                    section_end = i
                    break

                # Skip empty lines
                if not current_line:
                    continue

                # Check for bullet points
                if current_line.startswith("- "):
                    if current_line.strip() == "-":  # Empty bullet
                        empty_bullet = i
                        break
                    else:  # Bullet with content
                        last_bullet = i

            # Add the note at the appropriate position
            if last_bullet > notes_start:
                # We have existing bullets, insert after the last one
                insert_at = last_bullet + 1
                # Only add a newline if the next line isn't already empty and isn't the end of the file
                if insert_at < len(lines) and lines[insert_at].strip() and not lines[insert_at].startswith("- "):
                    lines.insert(insert_at, "\n")
                    insert_at += 1
                lines.insert(insert_at, formatted_note)
            else:
                # No existing bullets, add after section header with proper spacing
                # Ensure one blank line after header
                if notes_start + 1 >= len(lines) or lines[notes_start + 1].strip():
                    lines.insert(notes_start + 1, "\n")
                # Add the note
                lines.insert(notes_start + 2, formatted_note)
                # Only add empty bullet if this is the very first bullet in the section
                current_section_lines = lines[notes_start:section_end]
                has_existing_bullets = any(line.strip().startswith("- ") for line in current_section_lines[:-1])
                if not has_existing_bullets:
                    lines.insert(notes_start + 3, "- \n")

            # Remove any trailing empty bullets if we're adding to existing content
            if last_bullet > notes_start:
                i = len(lines) - 1
                while i > last_bullet:
                    if lines[i].strip() == "-":
                        del lines[i]
                    elif lines[i].strip():  # Stop at first non-empty line
                        break
                    i -= 1

            # Write back to file
            with open(note_path, "w", encoding="utf-8") as file:
                file.writelines(lines)

            return True

        except Exception as e:
            logger.error(f"Error appending note: {e}")
            return False


# CLI handler
class NoterCLI:
    """Handles command line interface and user interaction"""

    def __init__(self):
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description="Noter - Manage your Obsidian daily notes")
        parser.add_argument("note", nargs="?", help="Note content to add")
        parser.add_argument("--tags", help="Comma-separated list of tags to add to the note")
        parser.add_argument("--config", help="Path to custom config file")
        parser.add_argument("--version", action="version", version="Noter v1.1.0")
        return parser

    def run(self) -> int:
        """Run the CLI interface"""
        try:
            args = self.parser.parse_args()

            # Load configuration
            config_manager = ConfigManager(args.config)
            config = config_manager.load_config()
            if not config:
                return 1

            # Setup managers
            template_manager = TemplateManager(config)
            note_manager = NoteManager(config, template_manager)

            # Get the note content
            note_content = args.note
            if not note_content:
                note_content = input("Enter the note you want to append: ")
                if not note_content.strip():
                    logger.error("Note cannot be empty. Exiting.")
                    return 1

            # Process tags
            tags = None
            if args.tags:
                tags = [tag.strip() for tag in args.tags.split(",")]

            # Add the note
            note_date = datetime.now().strftime(config.get("date_format", "%Y-%m-%d"))
            success = note_manager.append_to_note(note_content, note_date, tags)

            if success:
                logger.info(f"✓ Note successfully added to {note_manager.get_note_path(note_date)}")
                return 0
            else:
                logger.error(f"✗ Failed to add note to {note_manager.get_note_path(note_date)}")
                return 1

        except KeyboardInterrupt:
            logger.info("\nOperation cancelled by user. Exiting.")
            return 1
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return 1


# Main entry point
def main():
    """Main entry point for the noter application"""
    cli = NoterCLI()
    sys.exit(cli.run())


if __name__ == "__main__":
    main()

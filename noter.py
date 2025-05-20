import os
import re
import json
from datetime import datetime

CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "obsidian_vault_path": "C:/Users/YourUsername/Obsidian Vault/Daily Notes"
}

def load_config():
    """Load configuration from config.json, create if it doesn't exist"""
    try:
        if not os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(DEFAULT_CONFIG, f, indent=4)
            print(f"Configuration file created at: {os.path.abspath(CONFIG_FILE)}")
            print("Please update the Obsidian vault path in the config file before continuing.")
            return None

        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        # Validate the vault path exists
        if not os.path.exists(config["obsidian_vault_path"]):
            print(f"Error: Obsidian vault directory not found at: {config['obsidian_vault_path']}")
            print(f"Please update the path in {CONFIG_FILE}")
            return None
            
        return config

    except Exception as e:
        print(f"Error loading configuration: {e}")
        return None

# Function to get the current note file path based on user input
def get_note_path(note_date, config):
    return os.path.join(config["obsidian_vault_path"], f"{note_date}.md")

# Function to create a basic template for a new note
def create_basic_template(note_date, note_content):
    """Create a basic template for a new daily note"""
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

# Function to extract YAML frontmatter from content
def extract_frontmatter(content):
    """Extract YAML frontmatter from the content if it exists"""
    frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(0)
        content_without_frontmatter = content[len(frontmatter):]
        return frontmatter, content_without_frontmatter
    return None, content


# Function to append a note to the specified note file
def append_to_note(note, note_date, config):
    """Add a note to the Notes & Observations section of the daily note file"""
    try:
        note_path = get_note_path(note_date, config)
        timestamp = datetime.now().strftime('%H:%M')
        formatted_note = f"- [{timestamp}] {note}\n"
        
        if not os.path.exists(note_path):
            with open(note_path, 'w', encoding='utf-8') as file:
                file.write(create_basic_template(note_date, formatted_note.rstrip()))
            print(f"Created new daily note file for {note_date}")
            return True
        
        with open(note_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Find the Notes & Observations section
        notes_start = -1
        for i, line in enumerate(lines):
            if '## ✍️ Notes & Observations' in line:
                notes_start = i
                break
        
        if notes_start == -1:
            print("Could not find Notes & Observations section")
            return False
        
        # Find the empty bullet point or the end of the section
        section_end = len(lines)
        empty_bullet = -1
        last_bullet = notes_start
        
        for i in range(notes_start + 1, len(lines)):
            current_line = lines[i].rstrip()
            
            # Check for next section
            if current_line.startswith('## '):
                section_end = i
                break
            
            # Skip empty lines
            if not current_line:
                continue
            
            # Check for bullet points
            if current_line.startswith('- '):
                if current_line.strip() == '-':  # Empty bullet
                    empty_bullet = i
                    break
                elif '[' in current_line:  # Timestamped bullet
                    last_bullet = i
                else:  # Regular bullet with content
                    last_bullet = i
        
        # Add the note at the appropriate position
        if last_bullet > notes_start:
            # We have existing timestamped bullets, insert after the last one
            insert_at = last_bullet + 1
            # Only add a newline if the next line isn't already empty and isn't the end of the file
            if insert_at < len(lines) and lines[insert_at].strip() and not lines[insert_at].startswith('- '):
                lines.insert(insert_at, '\n')
                insert_at += 1
            lines.insert(insert_at, formatted_note)
        else:
            # No existing bullets, add after section header with proper spacing
            # Ensure one blank line after header
            if notes_start + 1 >= len(lines) or lines[notes_start + 1].strip():
                lines.insert(notes_start + 1, '\n')
            # Add the note
            lines.insert(notes_start + 2, formatted_note)
            # Only add empty bullet if there are no other bullets in the section (check before we add our note)
            if not any(line.strip().startswith('- ') for line in lines[notes_start:section_end]):
                lines.insert(notes_start + 3, '- \n')
                
        # Remove any trailing empty bullet if we're adding to existing content
        if last_bullet > notes_start:
            # Look for and remove trailing empty bullets
            i = len(lines) - 1
            while i > last_bullet:
                if lines[i].strip() == '-':
                    del lines[i]
                elif lines[i].strip():  # Stop at first non-empty line
                    break
                i -= 1
        
        # Write back to file
        with open(note_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)
        
        return True
    
    except Exception as e:
        print(f"Error appending note: {e}")
        return False

# Main script for user interaction
def main():
    try:
        print("Noter - Append notes to your Obsidian daily notes")
        print("=" * 50)
        
        # Load configuration
        config = load_config()
        if not config:
            return
            
        note_date = datetime.now().strftime('%Y-%m-%d')  # Get current date for note file name
        
        note = input("Enter the note you want to append: ")
        if not note.strip():
            print("Note cannot be empty. Exiting.")
            return
        
        success = append_to_note(note, note_date, config)
        if success:
            print(f"✓ Note successfully added to {get_note_path(note_date, config)}")
        else:
            print(f"✗ Failed to add note to {get_note_path(note_date, config)}")
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user. Exiting.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

import os
import re
from datetime import datetime

# Configure your Obsidian Vault Path here
OBSIDIAN_VAULT_PATH = r"C:\Users\DougMiller\OneDrive - Brightworks Group, LLC\Obsidian_Vault\Daily Notes"

# Function to get the current note file path based on user input
def get_note_path(note_date):
    return os.path.join(OBSIDIAN_VAULT_PATH, f"{note_date}.md")

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
def append_to_note(note, note_date):
    """Add a note to the Notes & Observations section of the daily note file"""
    try:
        note_path = get_note_path(note_date)
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
        note_date = datetime.now().strftime('%Y-%m-%d')  # Get current date for note file name
        
        # Check if Obsidian vault directory exists
        if not os.path.exists(OBSIDIAN_VAULT_PATH):
            print(f"Error: Obsidian vault directory not found at: {OBSIDIAN_VAULT_PATH}")
            print("Please check the OBSIDIAN_VAULT_PATH configuration in noter.py")
            return
        
        note = input("Enter the note you want to append: ")
        if not note.strip():
            print("Note cannot be empty. Exiting.")
            return
        
        success = append_to_note(note, note_date)
        if success:
            print(f"✓ Note successfully added to {get_note_path(note_date)}")
        else:
            print(f"✗ Failed to add note to {get_note_path(note_date)}")
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user. Exiting.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

import os
from datetime import datetime

# Configure your Obsidian Vault Path here
OBSIDIAN_VAULT_PATH = r"C:\Users\DougMiller\OneDrive - Brightworks Group, LLC\Obsidian_Vault\Daily Notes"

# Function to get the current note file path based on user input
def get_note_path(note_date):
    return os.path.join(OBSIDIAN_VAULT_PATH, f"{note_date}.md")

# Function to append a note to the specified note file
def append_to_note(note, note_date):
    # Get the path for the specified note
    note_path = get_note_path(note_date)
    
    # If the file does not exist, create it and add a header
    if not os.path.exists(note_path):
        with open(note_path, 'w') as file:
            file.write(f"# Daily Note - {note_date}\n\n")
    
    # Append the note with a timestamp
    timestamp = datetime.now().strftime('%H:%M')
    with open(note_path, 'a') as file:
        file.write(f"- [{timestamp}] {note}\n")

# Main script for user interaction
def main():
    note_date = datetime.now().strftime('%Y-%m-%d')  # Get current date for note file name
    note = input("Enter the note you want to append: ")
    append_to_note(note, note_date)
    print(f"Note added to {get_note_path(note_date)}")

if __name__ == "__main__":
    main()

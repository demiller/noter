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
    
    # Get current timestamp for the note
    timestamp = datetime.now().strftime('%H:%M')
    formatted_note = f"- [{timestamp}] {note}"
    
    # If the file does not exist, create it with a simple header
    if not os.path.exists(note_path):
        with open(note_path, 'w') as file:
            file.write(f"# Daily Note - {note_date}\n\n")
            file.write("## ✍️ Notes & Observations\n\n")
            file.write(f"{formatted_note}\n")
        return
    
    # If file exists, read the content
    with open(note_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Check if the Notes & Observations section exists
    if "## ✍️ Notes & Observations" in content:
        # Split the content at the Notes & Observations section
        before_section, after_section = content.split("## ✍️ Notes & Observations", 1)
        
        # Find the next section (## ✅ Tasks) to know where to insert
        if "## ✅ Tasks" in after_section:
            notes_section, rest_of_content = after_section.split("## ✅ Tasks", 1)
            # Insert the new note at the end of the Notes & Observations section
            updated_content = (
                before_section + 
                "## ✍️ Notes & Observations" + 
                notes_section + 
                f"{formatted_note}\n\n" +
                "## ✅ Tasks" + 
                rest_of_content
            )
        else:
            # If Tasks section doesn't exist, just append to the end of what's there
            updated_content = (
                before_section + 
                "## ✍️ Notes & Observations" + 
                after_section + 
                f"\n{formatted_note}\n"
            )
    else:
        # If the Notes & Observations section doesn't exist, add it before any content
        updated_content = content + f"\n\n## ✍️ Notes & Observations\n\n{formatted_note}\n"
    
    # Write the updated content back to the file
    with open(note_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

# Main script for user interaction
def main():
    note_date = datetime.now().strftime('%Y-%m-%d')  # Get current date for note file name
    note = input("Enter the note you want to append: ")
    append_to_note(note, note_date)
    print(f"Note added to {get_note_path(note_date)}")

if __name__ == "__main__":
    main()

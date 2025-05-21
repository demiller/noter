import pytest
import os
from noter import NoteManager, TemplateManager
from datetime import datetime

@pytest.fixture
def test_note_setup(tmp_path):
    """Setup test environment with config and managers"""
    config = {
        "obsidian_vault_path": str(tmp_path),
        "date_format": "%Y-%m-%d",
        "time_format": "%H:%M"
    }
    template_manager = TemplateManager(config)
    note_manager = NoteManager(config, template_manager)
    return note_manager, config

def test_append_to_new_note(test_note_setup):
    """Test creating a new note file"""
    note_manager, config = test_note_setup
    note_date = datetime.now().strftime(config["date_format"])
    
    success = note_manager.append_to_note("Test note", note_date)
    assert success
    
    note_path = note_manager.get_note_path(note_date)
    assert os.path.exists(note_path)
    with open(note_path, 'r', encoding="utf-8") as f:
        content = f.read()
        assert "Test note" in content
        assert "## ✍️ Notes & Observations" in content

def test_append_to_existing_note(test_note_setup):
    """Test appending to an existing note"""
    note_manager, config = test_note_setup
    note_date = datetime.now().strftime(config["date_format"])
    
    # Add first note
    note_manager.append_to_note("First note", note_date)
    
    # Add second note
    success = note_manager.append_to_note("Second note", note_date)
    assert success
    
    note_path = note_manager.get_note_path(note_date)
    with open(note_path, 'r', encoding="utf-8") as f:
        content = f.readlines()
        notes_section = False
        note_lines = []
        for line in content:
            if "## ✍️ Notes & Observations" in line:
                notes_section = True
                continue
            if notes_section and line.startswith("## "):
                break
            if notes_section and line.strip():
                note_lines.append(line)
    
    assert len(note_lines) >= 2
    assert "First note" in note_lines[0]
    assert "Second note" in note_lines[1]

def test_append_note_with_tags(test_note_setup):
    """Test adding a note with tags"""
    note_manager, config = test_note_setup
    note_date = datetime.now().strftime(config["date_format"])
    tags = ["test", "important"]
    
    success = note_manager.append_to_note("Tagged note", note_date, tags)
    assert success
    
    note_path = note_manager.get_note_path(note_date)
    with open(note_path, 'r', encoding="utf-8") as f:
        content = f.read()
        assert "Tagged note" in content
        assert "#test #important" in content

def test_append_to_missing_section(test_note_setup):
    """Test behavior when Notes & Observations section is missing"""
    note_manager, config = test_note_setup
    note_date = datetime.now().strftime(config["date_format"])
    
    # Create a note file without the Notes section
    note_path = note_manager.get_note_path(note_date)
    with open(note_path, 'w') as f:
        f.write("# Test Note\n\n## Other Section\n\n- Some content")
    
    success = note_manager.append_to_note("Test note", note_date)
    assert not success  # Should fail when section is missing

def test_append_with_empty_tags(test_note_setup):
    """Test behavior with empty tags list"""
    note_manager, config = test_note_setup
    note_date = datetime.now().strftime(config["date_format"])
    tags = []
    
    success = note_manager.append_to_note("Note without tags", note_date, tags)
    assert success
    
    note_path = note_manager.get_note_path(note_date)
    with open(note_path, 'r', encoding="utf-8") as f:
        content = f.readlines()
        notes_section = False
        for line in content:
            if "## ✍️ Notes & Observations" in line:
                notes_section = True
            elif notes_section and line.startswith("## "):
                break
            elif notes_section and "Note without tags" in line:
                assert "#" not in line  # Should not have any tags in the note line

def test_append_with_special_characters(test_note_setup):
    """Test handling of special characters in notes"""
    note_manager, config = test_note_setup
    note_date = datetime.now().strftime(config["date_format"])
    special_note = "Note with *special* characters: & # @ ! $"
    
    success = note_manager.append_to_note(special_note, note_date)
    assert success
    
    note_path = note_manager.get_note_path(note_date)
    with open(note_path, 'r', encoding="utf-8") as f:
        content = f.read()
        assert special_note in content

def test_append_multiple_notes_spacing(test_note_setup):
    """Test proper spacing between multiple notes"""
    note_manager, config = test_note_setup
    note_date = datetime.now().strftime(config["date_format"])
    
    notes = ["First note", "Second note", "Third note"]
    for note in notes:
        success = note_manager.append_to_note(note, note_date)
        assert success
    
    note_path = note_manager.get_note_path(note_date)
    with open(note_path, 'r', encoding="utf-8") as f:
        content = f.readlines()
        notes_section = False
        note_lines = []
        for line in content:
            if "## ✍️ Notes & Observations" in line:
                notes_section = True
                continue
            if notes_section and line.startswith("## "):
                break
            if notes_section and line.startswith("- ["):
                note_lines.append(line.strip())
    
    # Check for proper spacing between notes
    assert len(note_lines) >= len(notes)
    for i, note in enumerate(notes):
        assert note in note_lines[i]

def test_note_timestamp_format(test_note_setup):
    """Test that notes have correctly formatted timestamps"""
    note_manager, config = test_note_setup
    note_date = datetime.now().strftime(config["date_format"])
    time_format = config["time_format"]
    
    success = note_manager.append_to_note("Test note", note_date)
    assert success
    
    note_path = note_manager.get_note_path(note_date)
    with open(note_path, 'r', encoding="utf-8") as f:
        content = f.readlines()
        for line in content:
            if "Test note" in line:
                # Should match format: "- [HH:MM] Test note"
                assert line.startswith("- [")
                timestamp = line[3:8]  # Extract HH:MM
                # Verify it's a valid time
                try:
                    datetime.strptime(timestamp, time_format)
                    assert True
                except ValueError:
                    assert False

def test_empty_bullet_handling(test_note_setup):
    """Test handling of empty bullets"""
    note_manager, config = test_note_setup
    note_date = datetime.now().strftime(config["date_format"])
    
    # Add first note to empty section
    success = note_manager.append_to_note("First note", note_date)
    assert success
    
    note_path = note_manager.get_note_path(note_date)
    with open(note_path, 'r', encoding="utf-8") as f:
        content = f.readlines()
        notes_section = False
        found_empty_bullet = False
        for line in content:
            if "## ✍️ Notes & Observations" in line:
                notes_section = True
                continue
            if notes_section and line.strip() == '-':
                found_empty_bullet = True
                break
    
    assert found_empty_bullet, "Empty bullet should exist after first note"
    
    # Add second note
    success = note_manager.append_to_note("Second note", note_date)
    assert success
    
    # Verify empty bullet is gone
    with open(note_path, 'r', encoding="utf-8") as f:
        content = f.readlines()
        notes_section = False
        empty_bullets = 0
        for line in content:
            if "## ✍️ Notes & Observations" in line:
                notes_section = True
                continue
            if notes_section and line.strip() == '-':
                empty_bullets += 1
    
    assert empty_bullets == 0, "Empty bullets should be removed when adding to existing notes"

def test_note_insertion_order(test_note_setup):
    """Test that notes are inserted in chronological order"""
    note_manager, config = test_note_setup
    note_date = datetime.now().strftime(config["date_format"])
    
    notes = ["First note", "Second note", "Third note"]
    for note in notes:
        success = note_manager.append_to_note(note, note_date)
        assert success
    
    note_path = note_manager.get_note_path(note_date)
    with open(note_path, 'r', encoding="utf-8") as f:
        content = f.readlines()
        notes_section = False
        timestamps = []
        for line in content:
            if "## ✍️ Notes & Observations" in line:
                notes_section = True
                continue
            if notes_section and line.startswith("- ["):
                timestamp = line[3:8]  # Extract HH:MM
                timestamps.append(timestamp)
    
    # Verify timestamps are in chronological order
    sorted_timestamps = sorted(timestamps)
    assert timestamps == sorted_timestamps, "Notes should be in chronological order"

import json
import os
from datetime import datetime
from unittest.mock import patch

import pytest

from noter import ConfigManager, NoteManager, NoterCLI, TemplateManager


@pytest.fixture
def test_environment(tmp_path):
    """Setup a complete test environment"""
    # Create vault directory
    vault_path = tmp_path / "test_vault"
    os.makedirs(vault_path)

    # Create config
    config_file = tmp_path / "config.json"
    config = {
        "obsidian_vault_path": str(vault_path),
        "date_format": "%Y-%m-%d",
        "time_format": "%H:%M",
    }
    config_file.write_text(json.dumps(config), encoding="utf-8")

    return {"vault_path": vault_path, "config_file": config_file, "config": config}


def test_full_workflow(test_environment):
    """Test the complete noter workflow"""
    # Setup environment
    env = test_environment
    note_date = datetime.now().strftime("%Y-%m-%d")

    # Initialize components
    config_manager = ConfigManager(str(env["config_file"]))
    config = config_manager.load_config()
    template_manager = TemplateManager(config)
    note_manager = NoteManager(config, template_manager)

    # Test creating new note
    first_note = "First test note"
    success = note_manager.append_to_note(first_note, note_date)
    assert success

    # Verify file creation
    note_path = os.path.join(env["vault_path"], f"{note_date}.md")
    assert os.path.exists(note_path)

    # Test adding another note with tags
    second_note = "Second note with tags"
    tags = ["test", "important"]
    success = note_manager.append_to_note(second_note, note_date, tags)
    assert success

    # Verify content
    with open(note_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert first_note in content
        assert second_note in content
        assert "#test #important" in content
        assert "## ✍️ Notes & Observations" in content


def test_cli_integration(test_environment):
    """Test the CLI interface end-to-end"""
    env = test_environment
    cli = NoterCLI()

    # Test direct note addition
    with patch(
        "sys.argv", ["noter", "CLI test note", "--config", str(env["config_file"])]
    ):
        result = cli.run()
        assert result == 0

    # Test interactive mode
    with (
        patch("sys.argv", ["noter", "--config", str(env["config_file"])]),
        patch("builtins.input", return_value="Interactive test note"),
    ):
        result = cli.run()
        assert result == 0

    # Verify results
    note_path = os.path.join(
        env["vault_path"], f"{datetime.now().strftime('%Y-%m-%d')}.md"
    )
    with open(note_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "CLI test note" in content
        assert "Interactive test note" in content

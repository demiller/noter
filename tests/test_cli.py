import pytest
import json
from noter import NoterCLI
from datetime import datetime
from unittest.mock import patch

@pytest.fixture
def cli():
    return NoterCLI()

def test_cli_with_direct_note(cli, tmp_path):
    """Test CLI with direct note input"""
    test_config = {
        "obsidian_vault_path": str(tmp_path),
        "date_format": "%Y-%m-%d",
        "time_format": "%H:%M"
    }
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(test_config))
    
    with patch('sys.argv', ['noter', 'Test note', '--config', str(config_file)]):
        result = cli.run()
        assert result == 0

def test_cli_with_tags(cli, tmp_path):
    """Test CLI with tags argument"""
    test_config = {
        "obsidian_vault_path": str(tmp_path),
        "date_format": "%Y-%m-%d",
        "time_format": "%H:%M"
    }
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(test_config))
    
    with patch('sys.argv', ['noter', 'Tagged note', '--tags', 'test,important', '--config', str(config_file)]):
        result = cli.run()
        assert result == 0
        
        # Verify tags in note
        note_path = tmp_path / datetime.now().strftime("%Y-%m-%d.md")
        assert note_path.exists()
        content = note_path.read_text()
        assert "#test #important" in content

def test_cli_with_empty_note(cli):
    """Test CLI with empty note"""
    with patch('sys.argv', ['noter', '']):
        result = cli.run()
        assert result == 1

def test_cli_with_invalid_config(cli, tmp_path):
    """Test CLI with invalid config file"""
    invalid_config = tmp_path / "invalid_config.json"
    invalid_config.write_text("invalid json")
    
    with patch('sys.argv', ['noter', 'Test note', '--config', str(invalid_config)]):
        result = cli.run()
        assert result == 1

def test_cli_interactive_mode(cli, tmp_path):
    """Test CLI in interactive mode"""
    test_config = {
        "obsidian_vault_path": str(tmp_path),
        "date_format": "%Y-%m-%d",
        "time_format": "%H:%M"
    }
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(test_config))
    
    with patch('sys.argv', ['noter', '--config', str(config_file)]), \
         patch('builtins.input', return_value='Interactive note'):
        result = cli.run()
        assert result == 0
        
        # Verify note was added
        note_path = tmp_path / datetime.now().strftime("%Y-%m-%d.md")
        assert note_path.exists()
        content = note_path.read_text()
        assert "Interactive note" in content


import pytest
import os
import json
from noter import ConfigManager, TemplateManager, NoteManager

@pytest.fixture
def test_vault(tmp_path):
    """Create a test vault directory"""
    vault_path = tmp_path / "test_vault"
    os.makedirs(vault_path)
    return vault_path

@pytest.fixture
def test_config(test_vault):
    """Create a test configuration"""
    return {
        "obsidian_vault_path": str(test_vault),
        "date_format": "%Y-%m-%d",
        "time_format": "%H:%M",
        "template_path": None
    }

@pytest.fixture
def test_config_file(test_config, tmp_path):
    """Create a test config file"""
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(test_config))
    return config_file

@pytest.fixture
def test_managers(test_config):
    """Create test instances of template and note managers"""
    template_manager = TemplateManager(test_config)
    note_manager = NoteManager(test_config, template_manager)
    return template_manager, note_manager


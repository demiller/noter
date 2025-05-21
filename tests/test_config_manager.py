import pytest
import json
import os
from noter import ConfigManager

@pytest.fixture
def test_config_file(tmp_path):
    """Create a test config file with valid settings"""
    config_file = tmp_path / "test_config.json"
    vault_path = tmp_path / "test_vault"
    os.makedirs(vault_path)
    
    test_config = {
        "obsidian_vault_path": str(vault_path),
        "date_format": "%Y-%m-%d",
        "time_format": "%H:%M",
        "template_path": None
    }
    config_file.write_text(json.dumps(test_config))
    return config_file

def test_load_valid_config(test_config_file):
    """Test loading a valid configuration file"""
    config_manager = ConfigManager(str(test_config_file))
    config = config_manager.load_config()
    
    assert config is not None
    assert "obsidian_vault_path" in config
    assert os.path.exists(config["obsidian_vault_path"])
    assert config["date_format"] == "%Y-%m-%d"
    assert config["time_format"] == "%H:%M"

def test_create_default_config(tmp_path):
    """Test creation of default config file"""
    config_path = tmp_path / "config.json"
    config_manager = ConfigManager(str(config_path))
    
    # First load should create default config
    config = config_manager.load_config()
    assert config is None  # Returns None when creating default
    assert config_path.exists()
    
    # Check default config content
    with open(config_path, 'r') as f:
        default_config = json.load(f)
    assert "obsidian_vault_path" in default_config
    assert "date_format" in default_config
    assert "time_format" in default_config

def test_invalid_vault_path(tmp_path):
    """Test config with invalid vault path"""
    config_file = tmp_path / "test_config.json"
    test_config = {
        "obsidian_vault_path": str(tmp_path / "nonexistent_vault"),
        "date_format": "%Y-%m-%d",
        "time_format": "%H:%M"
    }
    config_file.write_text(json.dumps(test_config))
    
    config_manager = ConfigManager(str(config_file))
    config = config_manager.load_config()
    assert config is None

def test_invalid_json_config(tmp_path):
    """Test handling of invalid JSON in config file"""
    config_file = tmp_path / "test_config.json"
    config_file.write_text("Invalid JSON content")
    
    config_manager = ConfigManager(str(config_file))
    config = config_manager.load_config()
    assert config is None

def test_missing_required_fields(tmp_path):
    """Test config missing required fields"""
    config_file = tmp_path / "test_config.json"
    test_config = {
        "date_format": "%Y-%m-%d",  # Missing obsidian_vault_path
        "time_format": "%H:%M"
    }
    config_file.write_text(json.dumps(test_config))
    
    config_manager = ConfigManager(str(config_file))
    config = config_manager.load_config()
    assert config is None

def test_custom_date_format(test_config_file):
    """Test loading config with custom date format"""
    # Modify existing config
    with open(test_config_file, 'r') as f:
        config_data = json.load(f)
    
    config_data["date_format"] = "%d-%m-%Y"
    
    with open(test_config_file, 'w') as f:
        json.dump(config_data, f)
    
    config_manager = ConfigManager(str(test_config_file))
    config = config_manager.load_config()
    assert config is not None
    assert config["date_format"] == "%d-%m-%Y"


import pytest
import os
import re
import io
import sys
import logging
from unittest.mock import patch
from noter import TemplateManager


@pytest.fixture
def capture_logs():
    """Fixture to capture log output for testing"""
    # Create a string IO object to capture log output
    log_capture = io.StringIO()
    # Configure a handler to write to our string IO
    handler = logging.StreamHandler(log_capture)
    # Set formatter
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    # Get the logger used by noter
    logger = logging.getLogger("noter")
    # Store the original handlers
    original_handlers = logger.handlers.copy()
    original_level = logger.level
    # Clear existing handlers and add our capture handler
    logger.handlers = [handler]
    logger.setLevel(logging.INFO)
    
    yield log_capture
    
    # Restore original handlers and level
    logger.handlers = original_handlers
    logger.setLevel(original_level)


def test_invalid_template_content(tmp_path, capture_logs):
    """Test handling of invalid template content with malformed variables"""
    # Create a template with malformed variables
    template_file = tmp_path / "invalid_template.md"
    template_file.write_text("Invalid {{template} content with {mismatched} braces", encoding="utf-8")
    
    config = {
        "template_path": str(template_file),
        "date_format": "%Y-%m-%d",
        "time_format": "%H:%M"
    }
    
    template_manager = TemplateManager(config)
    result = template_manager.create_basic_template("2025-05-21", "Test note")
    
    # Should fall back to default template
    assert "Daily Note - 2025-05-21" in result
    assert "## ✍️ Notes & Observations" in result
    assert "Test note" in result
    
    # Check logs for fallback message
    log_content = capture_logs.getvalue()
    assert "WARNING - Template has mismatched variable braces" in log_content
    assert "WARNING - Falling back to default template" in log_content
    assert "Successfully applied custom template" not in log_content


def test_invalid_template_content_another_type(tmp_path, capture_logs):
    """Test handling of invalid template content with unbalanced braces"""
    # Create a template with unbalanced braces
    template_file = tmp_path / "unbalanced_template.md"
    template_file.write_text("Template with {{extra {{ braces}}", encoding="utf-8")
    
    config = {
        "template_path": str(template_file),
        "date_format": "%Y-%m-%d",
        "time_format": "%H:%M"
    }
    
    template_manager = TemplateManager(config)
    result = template_manager.create_basic_template("2025-05-21", "Test note")
    
    # Should fall back to default template
    assert "Daily Note - 2025-05-21" in result
    assert "## ✍️ Notes & Observations" in result
    assert "Test note" in result
    
    # Check logs for fallback message
    log_content = capture_logs.getvalue()
    assert "WARNING - Template has mismatched variable braces" in log_content
    assert "WARNING - Falling back to default template" in log_content
    assert "Successfully applied custom template" not in log_content


def test_utf8_encoding_with_emojis(tmp_path, capture_logs):
    """Test template handling with UTF-8 encoding and emojis"""
    # Create a template with emojis
    template_file = tmp_path / "emoji_template.md"
    template_content = """---
title: "📅 {{note_date}} 📝"
---
# 🌟 Notes for {{weekday}} 🌟
{{note_content}}
⭐ End of template ⭐
"""
    template_file.write_text(template_content, encoding="utf-8")
    
    config = {
        "template_path": str(template_file),
        "date_format": "%Y-%m-%d",
        "time_format": "%H:%M"
    }
    
    template_manager = TemplateManager(config)
    result = template_manager.create_basic_template("2025-05-21", "Test note with 😊 emoji")
    
    # Verify template elements and emojis
    assert "📅 2025-05-21 📝" in result
    assert "🌟 Notes for" in result
    assert "Test note with 😊 emoji" in result
    assert "⭐ End of template ⭐" in result
    
    # Check logs for success message
    log_content = capture_logs.getvalue()
    assert "INFO - Successfully applied custom template" in log_content


def test_successful_template_loading(tmp_path, capture_logs):
    """Test successful loading and application of custom template"""
    template_file = tmp_path / "valid_template.md"
    template_content = """---
title: "Custom Template - {{note_date}}"
tags: [custom, template]
---
# Notes for {{weekday}}

## Content:
{{note_content}}

## Date Details:
- Month: {{month}}
- Day: {{day}}
- Year: {{year}}
"""
    template_file.write_text(template_content, encoding="utf-8")
    
    config = {
        "template_path": str(template_file),
        "date_format": "%Y-%m-%d",
        "time_format": "%H:%M"
    }
    
    template_manager = TemplateManager(config)
    result = template_manager.create_basic_template("2025-05-21", "This is a test note")
    
    # Verify template content
    assert "Custom Template - 2025-05-21" in result
    assert "tags: [custom, template]" in result
    assert "# Notes for" in result
    assert "This is a test note" in result
    
    # Check logs for success message
    log_content = capture_logs.getvalue()
    assert "INFO - Successfully applied custom template" in log_content
    assert "WARNING - Falling back to default template" not in log_content


def test_fallback_to_default_template(tmp_path, capture_logs):
    """Test fallback to default template with unresolved variables"""
    template_file = tmp_path / "unresolved_template.md"
    template_content = """---
title: "{{note_date}}"
---
# Notes for {{weekday}}
{{note_content}}
{{unknown_variable}}
"""
    template_file.write_text(template_content, encoding="utf-8")
    
    config = {
        "template_path": str(template_file),
        "date_format": "%Y-%m-%d",
        "time_format": "%H:%M"
    }
    
    template_manager = TemplateManager(config)
    result = template_manager.create_basic_template("2025-05-21", "Test note")
    
    # Should fall back to default template
    assert "Daily Note - 2025-05-21" in result
    assert "## ✍️ Notes & Observations" in result
    assert "Test note" in result
    
    # Check logs for fallback message
    log_content = capture_logs.getvalue()
    assert "WARNING - Template contains unresolved variables" in log_content
    assert "Successfully applied custom template" not in log_content


def test_template_success_message_only_appears_for_valid_templates(tmp_path, capture_logs):
    """Test that success message only appears for valid templates"""
    # 1. First test with valid template
    valid_template_file = tmp_path / "valid.md"
    valid_template_content = """---
title: "{{note_date}}"
---
{{note_content}}
"""
    valid_template_file.write_text(valid_template_content, encoding="utf-8")
    
    config = {
        "template_path": str(valid_template_file),
        "date_format": "%Y-%m-%d",
        "time_format": "%H:%M"
    }
    
    template_manager = TemplateManager(config)
    template_manager.create_basic_template("2025-05-21", "Test note")
    
    # Check logs
    log_content = capture_logs.getvalue()
    assert "INFO - Successfully applied custom template" in log_content
    
    # Clear log capture
    capture_logs.truncate(0)
    capture_logs.seek(0)
    
    # 2. Now test with invalid template
    invalid_template_file = tmp_path / "invalid.md"
    invalid_template_content = "Invalid {{template}"
    invalid_template_file.write_text(invalid_template_content, encoding="utf-8")
    
    config["template_path"] = str(invalid_template_file)
    
    template_manager = TemplateManager(config)
    template_manager.create_basic_template("2025-05-21", "Test note")
    
    # Check logs again
    log_content = capture_logs.getvalue()
    assert "WARNING - Falling back to default template" in log_content
    assert "INFO - Successfully applied custom template" not in log_content


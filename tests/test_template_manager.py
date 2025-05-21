import pytest
from noter import TemplateManager
from datetime import datetime
import os


@pytest.fixture
def test_template_setup(tmp_path):
    """Basic template manager setup"""
    config = {"template_path": None, "date_format": "%Y-%m-%d", "time_format": "%H:%M"}
    return TemplateManager(config)


def test_default_template_creation(test_template_setup):
    """Test creation of default template"""
    result = test_template_setup.create_basic_template("2025-05-21", "Test note")

    # Check content
    assert "Test note" in result
    current_weekday = datetime.now().strftime("%A")
    assert current_weekday in result

    # Check sections
    assert "## ☀️ Summary" in result
    assert "## ✅ Tasks" in result
    assert "## 🔁 Reviews or Highlights Revisited" in result
    assert "## 📓 Notes Created or Touched Today" in result
    assert "## ✍️ Notes & Observations" in result


def test_template_frontmatter(test_template_setup):
    """Test frontmatter formatting"""
    result = test_template_setup.create_basic_template("2025-05-21", "Test note")

    # Check frontmatter
    assert "---" in result
    assert 'title: "Daily Note - 2025-05-21"' in result
    assert "status: active" in result
    assert "topic: daily-log" in result
    assert "tags: [dailynotes, log]" in result
    assert "aliases: []" in result


def test_template_dataview_blocks(test_template_setup):
    """Test dataview block formatting"""
    result = test_template_setup.create_basic_template("2025-05-21", "Test note")

    # Check dataview blocks
    assert "```dataview" in result
    assert 'from ""' in result
    assert "where reviewed <= date(today) - dur(30 days)" in result
    assert "where file.mtime >= date(today)" in result


def test_custom_template(tmp_path):
    """Test custom template handling"""
    # Create custom template
    template_file = tmp_path / "custom_template.md"
    template_content = """---
title: "{{note_date}}"
---
# Notes for {{weekday}}
{{note_content}}
"""
    template_file.write_text(template_content)

    config = {"template_path": str(template_file), "date_format": "%Y-%m-%d", "time_format": "%H:%M"}

    template_manager = TemplateManager(config)
    result = template_manager.create_basic_template("2025-05-21", "Test note")

    # Check variable substitution
    assert "2025-05-21" in result
    assert "Test note" in result
    current_weekday = datetime.now().strftime("%A")
    assert current_weekday in result


def test_missing_template_fallback(tmp_path):
    """Test fallback to default template"""
    config = {"template_path": str(tmp_path / "nonexistent.md"), "date_format": "%Y-%m-%d", "time_format": "%H:%M"}

    template_manager = TemplateManager(config)
    result = template_manager.create_basic_template("2025-05-21", "Test note")

    # Should use default template
    assert "Daily Note - 2025-05-21" in result
    assert "## ✍️ Notes & Observations" in result
    assert "Test note" in result


def test_invalid_template_content(tmp_path):
    """Test handling of invalid template content"""
    template_file = tmp_path / "invalid.md"
    template_file.write_text("Invalid {{template} content")

    config = {"template_path": str(template_file), "date_format": "%Y-%m-%d", "time_format": "%H:%M"}

    template_manager = TemplateManager(config)
    result = template_manager.create_basic_template("2025-05-21", "Test note")

    # Should fall back to default template
    assert "Daily Note - 2025-05-21" in result
    assert "Test note" in result


def test_date_formatting(test_template_setup):
    """Test date formatting in template"""
    result = test_template_setup.create_basic_template("2025-05-21", "Test note")
    today = datetime.now()

    # Check date formatting
    assert today.strftime("%A") in result  # weekday
    assert today.strftime("%B") in result  # month
    assert str(today.year) in result

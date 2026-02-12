import json
from unittest.mock import patch

from holmes.core.toolset_manager import ToolsetManager


def test_auto_discover_custom_runbook_catalog(tmp_path):
    """Test that ToolsetManager auto-discovers catalog.json from well-known location."""
    # Create catalog directory with catalog.json
    catalog_dir = tmp_path / "custom_runbooks"
    catalog_dir.mkdir()
    catalog_file = catalog_dir / "catalog.json"
    catalog_data = {
        "catalog": [
            {
                "id": "auto-discovered",
                "update_date": "2023-01-01",
                "description": "Auto-discovered runbook",
                "link": "test.md",
            }
        ]
    }
    catalog_file.write_text(json.dumps(catalog_data))

    with patch(
        "holmes.core.toolset_manager.CUSTOM_RUNBOOK_CATALOGS_LOCATION",
        str(catalog_dir),
    ):
        manager = ToolsetManager()
        assert manager.custom_runbook_catalogs is not None
        assert len(manager.custom_runbook_catalogs) == 1
        assert str(manager.custom_runbook_catalogs[0]).endswith("catalog.json")


def test_auto_discover_no_catalog_at_location(tmp_path):
    """Test that missing catalog.json at well-known location is handled gracefully."""
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()

    with patch(
        "holmes.core.toolset_manager.CUSTOM_RUNBOOK_CATALOGS_LOCATION",
        str(empty_dir),
    ):
        manager = ToolsetManager()
        # Should be None (no catalogs found)
        assert manager.custom_runbook_catalogs is None


def test_auto_discover_location_does_not_exist(tmp_path):
    """Test that nonexistent well-known location is handled gracefully."""
    with patch(
        "holmes.core.toolset_manager.CUSTOM_RUNBOOK_CATALOGS_LOCATION",
        str(tmp_path / "nonexistent"),
    ):
        manager = ToolsetManager()
        assert manager.custom_runbook_catalogs is None

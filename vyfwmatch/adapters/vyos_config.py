"""VyOS Configuration Adapter.

This adapter provides access to VyOS configuration data.
Currently uses the existing parser as a bridge, designed for easy migration
to vyos-1x API once dependencies are resolved.
"""

import sys
from pathlib import Path
from typing import Any

# Add vyos-1x to path
VYOS_1X_PATH = Path(__file__).parent.parent.parent / "vyos-1x" / "python"
if str(VYOS_1X_PATH) not in sys.path:
    sys.path.insert(0, str(VYOS_1X_PATH))

from parser.config_parser import parse_config_file


class VyOSConfigAdapter:
    """Adapter for accessing VyOS configuration.

    This provides a clean interface for configuration access,
    abstracting away the underlying implementation.
    """

    def __init__(self, config_path: str):
        """Initialize adapter with a VyOS config file path.

        Args:
            config_path: Path to VyOS boot configuration file

        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config file is invalid
        """
        self.config_path = config_path
        self._config_tree = None
        self._load_config()

    def _load_config(self) -> None:
        """Load and parse the VyOS configuration file."""
        try:
            # For now, use the existing parser
            # TODO: Migrate to vyos.configtree.ConfigTree when dependencies resolved
            self._config_tree = parse_config_file(self.config_path)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Config file not found: {self.config_path}") from e
        except Exception as e:
            raise ValueError(f"Failed to parse config file: {e}") from e

    def get_firewall_config(self) -> dict[str, Any]:
        """Get the firewall configuration tree.

        Returns:
            Dictionary containing firewall configuration
        """
        if self._config_tree is None:
            return {}

        firewall = self._config_tree.get("firewall", {})
        if not isinstance(firewall, dict):
            return {}

        return firewall

    def get_subtree(self, path: list[str]) -> Any:
        """Get a configuration subtree by path.

        Args:
            path: List of path elements (e.g., ['firewall', 'ipv4', 'forward'])

        Returns:
            Configuration subtree or None if not found
        """
        current = self._config_tree

        for element in path:
            if not isinstance(current, dict):
                return None
            current = current.get(element)
            if current is None:
                return None

        return current

    def exists(self, path: list[str]) -> bool:
        """Check if a configuration path exists.

        Args:
            path: List of path elements

        Returns:
            True if path exists, False otherwise
        """
        return self.get_subtree(path) is not None

    def list_nodes(self, path: list[str]) -> list[str]:
        """List child nodes at the given path.

        Args:
            path: List of path elements

        Returns:
            List of child node names
        """
        subtree = self.get_subtree(path)

        if not isinstance(subtree, dict):
            return []

        return list(subtree.keys())

    def return_value(self, path: list[str]) -> str | None:
        """Get a single value at the given path.

        Args:
            path: List of path elements

        Returns:
            Value as string or None if not found
        """
        value = self.get_subtree(path)

        if value is None:
            return None

        if isinstance(value, list):
            return str(value[0]) if value else None

        if isinstance(value, dict):
            return None  # Not a leaf value

        return str(value) if value != "" else None

    def return_values(self, path: list[str]) -> list[str]:
        """Get multiple values at the given path.

        Args:
            path: List of path elements

        Returns:
            List of values as strings
        """
        value = self.get_subtree(path)

        if value is None:
            return []

        if isinstance(value, list):
            return [str(v) for v in value]

        if isinstance(value, dict):
            return []  # Not a leaf value

        return [str(value)] if value != "" else []

"""VyOS Configuration Adapter.

This adapter provides access to VyOS configuration data using the original
vyos-1x utilities for config parsing and dictionary traversal.

Directly imports and uses vyos-1x dict search utilities to ensure full
compatibility with VyOS native implementations.
"""

import sys
from pathlib import Path
from typing import Any

from vyfwmatch.adapters.config_parser import parse_config_file
from vyfwmatch.adapters.vyos_utils import (
    dict_search,
    dict_search_args,
    dict_search_recursive,
    get_sub_dict,
)

# Add vyos-1x to path for potential future use
VYOS_1X_PATH = Path(__file__).parent.parent.parent / "vyos-1x" / "python"
if str(VYOS_1X_PATH) not in sys.path:
    sys.path.insert(0, str(VYOS_1X_PATH))


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
            # Use our custom parser (vyos.configtree requires C library)
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
        """Get a configuration subtree by path using VyOS-compatible dict traversal.

        Args:
            path: List of path elements (e.g., ['firewall', 'ipv4', 'forward'])

        Returns:
            Configuration subtree or None if not found

        Example:
            >>> adapter.get_subtree(['firewall', 'ipv4'])
            {'forward': {...}, 'input': {...}}
        """
        if self._config_tree is None:
            return None
        return dict_search_args(self._config_tree, *path)

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

    def dict_search(self, path_str: str, default=None) -> Any:
        """Search config using dot-delimited path (original VyOS implementation).

        This method uses the original vyos.utils.dict.dict_search function
        from vyos-1x for traversing the configuration tree using dot-notation paths.

        Args:
            path_str: Dot-delimited path string (e.g., "firewall.ipv4.forward")
            default: Default value if path not found

        Returns:
            Value at path or default

        Example:
            >>> adapter.dict_search('firewall.ipv4.forward.filter.default-action')
            'accept'
        """
        if self._config_tree is None:
            return default
        return dict_search(path_str, self._config_tree, default)

    def dict_search_recursive(self, key: str):
        """Recursively search for all occurrences of a key (original VyOS implementation).

        This method uses the original vyos.utils.dict.dict_search_recursive function
        from vyos-1x to find all instances of a key throughout the configuration tree.

        Args:
            key: The key to search for

        Yields:
            Tuple of (value, path) for each occurrence

        Example:
            >>> list(adapter.dict_search_recursive('default-action'))
            [('accept', ['firewall', 'ipv4', 'forward', 'filter', 'default-action']),
             ('drop', ['firewall', 'ipv4', 'input', 'filter', 'default-action'])]
        """
        if self._config_tree is None:
            return
        yield from dict_search_recursive(self._config_tree, key)

    def get_sub_dict(self, path: list[str], get_first_key: bool = False) -> dict:
        """Get sub-dictionary at path (original VyOS implementation).

        This method uses the original vyos.utils.dict.get_sub_dict function
        from vyos-1x for extracting sub-dictionaries from the configuration tree.

        Args:
            path: List of path elements
            get_first_key: If True, return first child dict instead of parent

        Returns:
            Sub-dictionary at path or empty dict

        Example:
            >>> adapter.get_sub_dict(['firewall', 'ipv4'])
            {'ipv4': {'forward': {...}, 'input': {...}}}
        """
        if self._config_tree is None:
            return {}
        return get_sub_dict(self._config_tree, path, get_first_key)

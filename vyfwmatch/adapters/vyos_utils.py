"""Direct imports of VyOS utilities from vyos-1x.

This module provides direct access to vyos-1x utility functions by importing
them directly from the source files, bypassing the vyos.utils.__init__.py
which has heavy dependencies (cracklib, etc).

This approach allows us to use the original VyOS implementations without
modification while avoiding unnecessary dependencies.
"""

import importlib.util
import sys
import types
from pathlib import Path

# Add vyos-1x to path
VYOS_1X_PATH = Path(__file__).parent.parent.parent / "vyos-1x" / "python"
if str(VYOS_1X_PATH) not in sys.path:
    sys.path.insert(0, str(VYOS_1X_PATH))


def _import_vyos_module(module_path: str, module_name: str):
    """Import a VyOS module directly from file path, bypassing __init__.py.

    Args:
        module_path: Relative path to the module file from vyos-1x/python/
        module_name: Name to give the imported module

    Returns:
        The imported module
    """
    full_path = VYOS_1X_PATH / module_path
    spec = importlib.util.spec_from_file_location(module_name, full_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module from {full_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Import vyos dict utilities directly
_vyos_dict = _import_vyos_module("vyos/utils/dict.py", "vyos.utils.dict")

# Pre-register vyos modules in sys.modules to prevent vyos.template from
# triggering problematic __init__.py files when it imports dependencies
sys.modules['vyos.utils.dict'] = _vyos_dict

# Create minimal mock modules for vyos.template's other imports
# These won't be used by is_ipv4/is_ipv6 but are imported at module level

# Mock vyos.defaults
_vyos_defaults = types.ModuleType('vyos.defaults')
_vyos_defaults.directories = {  # type: ignore
    'templates': '/usr/share/vyos/templates/',
    'base': '/usr/libexec/vyos'
}
sys.modules['vyos.defaults'] = _vyos_defaults

# Mock vyos.utils.file
_vyos_utils_file = types.ModuleType('vyos.utils.file')
_vyos_utils_file.makedir = lambda x: None  # type: ignore
sys.modules['vyos.utils.file'] = _vyos_utils_file

# Mock vyos.utils.permission
_vyos_utils_permission = types.ModuleType('vyos.utils.permission')
_vyos_utils_permission.chmod = lambda x, y: None  # type: ignore
_vyos_utils_permission.chown = lambda x, y: None  # type: ignore
sys.modules['vyos.utils.permission'] = _vyos_utils_permission

# Import vyos template utilities directly
_vyos_template = _import_vyos_module("vyos/template.py", "vyos.template")

# Export the dict functions we need
dict_search = _vyos_dict.dict_search
dict_search_args = _vyos_dict.dict_search_args
dict_search_recursive = _vyos_dict.dict_search_recursive
get_sub_dict = _vyos_dict.get_sub_dict
mangle_dict_keys = _vyos_dict.mangle_dict_keys

# Export the template functions we need
is_ipv4 = _vyos_template.is_ipv4
is_ipv6 = _vyos_template.is_ipv6

__all__ = [
    'dict_search',
    'dict_search_args', 
    'dict_search_recursive',
    'get_sub_dict',
    'mangle_dict_keys',
    'is_ipv4',
    'is_ipv6',
]

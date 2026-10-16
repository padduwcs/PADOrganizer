"""Guards that keep file operations away from hidden, system and app-owned files."""

import os
import stat
import sys
from pathlib import Path


# Legacy data files that older builds stored next to the program.
RESERVED_FILENAMES = {"activity.log", "config.json"}

_WINDOWS_HIDDEN_ATTRIBUTES = (
    getattr(stat, "FILE_ATTRIBUTE_HIDDEN", 0x2) | getattr(stat, "FILE_ATTRIBUTE_SYSTEM", 0x4)
)
_WINDOWS_SYSTEM_VARIABLES = (
    "SystemRoot",
    "windir",
    "ProgramFiles",
    "ProgramFiles(x86)",
    "ProgramW6432",
    "ProgramData",
)
# Operating system trees where no subfolder should ever be reorganized.
_POSIX_SYSTEM_TREES = (
    "/bin",
    "/boot",
    "/dev",
    "/etc",
    "/lib",
    "/lib32",
    "/lib64",
    "/proc",
    "/run",
    "/sbin",
    "/sys",
    "/usr",
)
# Top-level folders that are system-owned, while their subfolders may hold user data.
_POSIX_SYSTEM_DIRECTORIES = ("/opt", "/root", "/srv", "/var")


def is_hidden_or_system(path: Path, platform_name=None) -> bool:
    """Return True for dotfiles and, on Windows, files flagged hidden or system."""
    path = Path(path)
    if path.name.startswith("."):
        return True
    platform_name = platform_name or sys.platform
    if platform_name != "win32":
        return False
    try:
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
    except OSError:
        return True
    return bool(attributes & _WINDOWS_HIDDEN_ATTRIBUTES)


def running_executable():
    """Return the frozen application binary, or None when running from source."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve()
    return None


def list_candidate_files(directory: Path, excluded_paths=(), platform_name=None):
    """List direct, regular, visible files that PADOrganizer is allowed to touch."""
    excluded = {Path(path).resolve() for path in excluded_paths if path}
    executable = running_executable()
    if executable is not None:
        excluded.add(executable)

    candidates = []
    for path in Path(directory).iterdir():
        if path.name in RESERVED_FILENAMES or path.is_symlink() or not path.is_file():
            continue
        if is_hidden_or_system(path, platform_name):
            continue
        if path.resolve() in excluded:
            continue
        candidates.append(path)
    return candidates


def _system_locations(platform_name, environment, home):
    """Return (trees, directories): trees are blocked with every descendant."""
    directories = {home}
    if platform_name == "win32":
        trees = {
            Path(environment[variable])
            for variable in _WINDOWS_SYSTEM_VARIABLES
            if environment.get(variable)
        }
    else:
        trees = {Path(value) for value in _POSIX_SYSTEM_TREES}
        directories.update(Path(value) for value in _POSIX_SYSTEM_DIRECTORIES)
    return (
        {tree.resolve() for tree in trees},
        {directory.resolve() for directory in directories},
    )


def classify_target_directory(
    path: Path,
    protected_directories=(),
    platform_name=None,
    environment=None,
    home=None,
):
    """Return "protected", "system" or None for a folder the user wants to organize."""
    platform_name = platform_name or sys.platform
    environment = os.environ if environment is None else environment
    home = Path.home() if home is None else Path(home)
    path = Path(path).resolve()

    if path in {Path(directory).resolve() for directory in protected_directories}:
        return "protected"
    if path.parent == path:
        return "system"
    trees, directories = _system_locations(platform_name, environment, home)
    if path in directories or any(path == tree or tree in path.parents for tree in trees):
        return "system"
    return None

"""Platform-aware locations for application resources and user data."""

import os
import sys
from dataclasses import dataclass
from pathlib import Path


APP_NAME = "PADOrganizer"


@dataclass(frozen=True)
class ApplicationPaths:
    application_dir: Path
    resource_dir: Path
    config_dir: Path
    data_dir: Path
    state_dir: Path

    @property
    def config_file(self):
        return self.config_dir / "config.json"

    @property
    def log_dir(self):
        return self.state_dir / "logs"

    @property
    def trash_dir(self):
        return self.data_dir / "PADOrganizer_Trash"


def _xdg_path(environment, variable, fallback, app_name):
    configured = environment.get(variable)
    base = Path(configured).expanduser() if configured else fallback
    return base / app_name


def resolve_application_paths(
    platform_name=None,
    environment=None,
    home=None,
    frozen=None,
    executable=None,
    bundle_dir=None,
):
    """Resolve paths with injectable inputs so platform behavior is testable."""
    platform_name = platform_name or sys.platform
    environment = os.environ if environment is None else environment
    home = Path.home() if home is None else Path(home)
    frozen = getattr(sys, "frozen", False) if frozen is None else frozen
    executable = Path(sys.executable) if executable is None else Path(executable)
    source_root = Path(__file__).resolve().parent.parent
    application_dir = executable.resolve().parent if frozen else source_root

    if bundle_dir is not None:
        resource_dir = Path(bundle_dir)
    elif frozen and hasattr(sys, "_MEIPASS"):
        resource_dir = Path(sys._MEIPASS)
    else:
        resource_dir = source_root

    if platform_name.startswith("linux"):
        config_dir = _xdg_path(environment, "XDG_CONFIG_HOME", home / ".config", APP_NAME)
        data_dir = _xdg_path(environment, "XDG_DATA_HOME", home / ".local" / "share", APP_NAME)
        state_dir = _xdg_path(environment, "XDG_STATE_HOME", home / ".local" / "state", APP_NAME)
    else:
        # Preserve the existing Windows portable and installer data layout.
        config_dir = application_dir
        data_dir = application_dir
        state_dir = application_dir

    return ApplicationPaths(
        application_dir=application_dir,
        resource_dir=resource_dir,
        config_dir=config_dir,
        data_dir=data_dir,
        state_dir=state_dir,
    )


PATHS = resolve_application_paths()
APPLICATION_DIR = PATHS.application_dir
RESOURCE_DIR = PATHS.resource_dir
CONFIG_DIR = PATHS.config_dir
DATA_DIR = PATHS.data_dir
STATE_DIR = PATHS.state_dir
CONFIG_FILE = PATHS.config_file
LOG_DIR = PATHS.log_dir
PAD_TRASH_DIR = PATHS.trash_dir

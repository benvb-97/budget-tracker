from pathlib import Path

# Get the directory where this file (paths.py) is located
_this_file_dir = Path(__file__).resolve().parent

# Get the root directory, which is 1 level up
ROOT_DIR = _this_file_dir.parent

# Define other important paths relative to the root
LOGS_DIR = ROOT_DIR / "logs"
RESOURCES_DIR = ROOT_DIR / "resources"
TESTS_DIR = ROOT_DIR / "tests"
SOURCE_DIR = ROOT_DIR / "src"
ICONS_DIR = RESOURCES_DIR / "icons"
APP_SETTINGS_FILEPATH = ROOT_DIR / "settings.json"

class IconPaths:
    FOLDER = ICONS_DIR / "folder"
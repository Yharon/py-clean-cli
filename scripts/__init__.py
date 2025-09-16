from pathlib import Path
from sys import path as sys_path
from logging import getLogger, basicConfig, INFO


PROJECT_ROOT = str(Path.cwd())
if PROJECT_ROOT not in sys_path:
    sys_path.insert(0, PROJECT_ROOT)

basicConfig(
    level=INFO,
    format="%(asctime)s - %(name)s - %(levelname)s:\n * %(message)s\n",
    datefmt="%H:%M:%S",
)
LOGGER = getLogger(__name__)

__all__ = ["LOGGER", "PROJECT_ROOT"]

from logging import getLogger, basicConfig, INFO, DEBUG

basicConfig(
    level=INFO,
    format="%(asctime)s - %(name)s - %(levelname)s:\n * %(message)s\n",
    datefmt="%H:%M:%S",
)


LOGGER = getLogger(__name__)
__all__ = ["LOGGER"]

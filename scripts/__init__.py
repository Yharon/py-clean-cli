from logging import basicConfig, INFO, getLogger

basicConfig(
    level=INFO,
    format="%(asctime)s - %(name)s - %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)

LOGGER_CLI = getLogger("py_clean_cli")


__all__ = ["LOGGER_CLI"]

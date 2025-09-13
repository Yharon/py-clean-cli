from simple_parsing import ArgumentParser

from py_clean_cli.helpers import discover_commands
from py_clean_cli.services import CommandsFactory


def main():
    discover_commands("scripts")

    parser = ArgumentParser()
    factory = CommandsFactory.get_instance(parser)

    factory.register_all_commands()
    factory.parse_and_execute()


if __name__ == "__main__":
    main()

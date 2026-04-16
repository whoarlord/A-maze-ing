#!/usr/bin/env python3

from Parser import Parser
from errors import ParseError, PerfectError, InvalidValueError
from typing import Any


def main():

    parser = Parser()
    dictionary: dict[str: Any] = {}

    with open("config.txt", "r") as file:
        for line in file.readlines():
            try:
                parser.parse_line(line.strip(), dictionary)

            except (ParseError, PerfectError, InvalidValueError,
                    Exception) as e:
                print(f"{e}")
                exit(1)

    print(f"{dictionary}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

from Parser import Parser
from errors import ParseError, PerfectError, InvalidValueError
from typing import Any
from maze import Maze
from Prim import Prim


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
    dictionary = dict(
        map(lambda item: (item[0].lower(), item[1]),
            dictionary.items()))
    maze = Maze(**dictionary)
    prim = Prim()
    prim.create_map(maze)
    maze.print_map()


if __name__ == "__main__":
    main()

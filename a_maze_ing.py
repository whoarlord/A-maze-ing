#!/usr/bin/env python3

from MazeProgram import Parser
from MazeProgram import ParseError, PerfectError, InvalidValueError
from MazeProgram import Maze
from MazeProgram import Algorithms
from MazeProgram.Graphics import Graphics
from MazeProgram import solve_maze
from typing import Any
import sys


def main():

    parser = Parser()
    dictionary: dict[str: Any] = {}
    argc: int = len(sys.argv)

    try:
        if (argc != 2):
            raise Exception(
                "a config file must be given and only one config file")
        with open(sys.argv[1], "r") as file:
            for line in file.readlines():
                parser.parse_line(line.strip(), dictionary)
    except (ParseError, PerfectError, InvalidValueError,
            Exception) as e:
        print(f"{e}")
        print("An error has been found on the configuration file, "
              "the program will now close.")
        exit(1)
    dictionary = parser.complete_dictionary(dictionary)
    dictionary = dict(
        map(lambda item: (item[0].lower(), item[1]),
            dictionary.items()))
    maze = Maze(**dictionary)
    limits: int = maze.width * maze.height * 10
    sys.setrecursionlimit(limits)
    if (limits > 640):
        sys.set_int_max_str_digits(maze.width * maze.height * 10)
    algorithms = Algorithms()
    algorithms.create_map(maze)
    solve_maze(maze)
    Graphics(maze)


if __name__ == "__main__":
    main()

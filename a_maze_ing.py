#!/usr/bin/env python3

from MazeGen import Parser, Config, RawConfig
from MazeGen import ParseError, PerfectError, InvalidValueError
from MazeGen import Maze
from MazeGen import Algorithms
from MazeGen import Graphics
from MazeGen import solve_maze
import sys


def main() -> None:

    parser = Parser()
    dictionary: RawConfig = {}
    argc: int = len(sys.argv)

    try:
        if (argc != 2):
            raise Exception(
                "a config file must be given and only one config file")
        with open(sys.argv[1], "r") as file:
            for line in file.readlines():
                parser.parse_line(line.strip(), dictionary)
        parser.entry_checker(dictionary)
    except (ParseError, PerfectError, InvalidValueError,
            Exception) as e:
        print(f"{e}")
        print("An error has been found on the configuration file, "
              "the program will now close.")
        exit(1)
    dictionary_output: Config = parser.complete_dictionary(dictionary)
    maze = Maze(**dictionary_output)
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

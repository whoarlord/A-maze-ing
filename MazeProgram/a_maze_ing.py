#!/usr/bin/env python3

from Parser import Parser
from errors import ParseError, PerfectError, InvalidValueError
from typing import Any
from maze import Maze
from Algorithms import Algorithms
from Graphics import Graphics
import maze_solver as maze_solver
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
    algorithms = Algorithms()
    algorithms.create_map(maze)
    maze_solver.solve_maze(maze)
    graphics = Graphics(maze)
    graphics.display_menu(maze, algorithms)


if __name__ == "__main__":
    main()

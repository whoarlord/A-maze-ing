#!/usr/bin/env python3

from MazeGen import Parser, Config, RawConfig
from MazeGen import ParseError, PerfectError, InvalidValueError
from MazeGen import Maze
from MazeGen import Algorithms
from MazeGen import Graphics
from MazeGen import solve_maze
import sys
import os


def check_output_file(dictionary_output: Config) -> None:
    """function for checking the output file"""
    if os.path.isdir('outputs'):
        print("is_dir\n")
        if os.access('outputs', os.X_OK | os.W_OK | os.R_OK):
            print("access\n")
        else:
            os.chmod("outputs", 0o777)
            print("changing permissionsg\n")
    else:
        if os.path.exists('outputs'):
            print("exists")
            os.rmdir('outputs')
        print("creating\n")
        os.mkdir("outputs")
    output: str = 'outputs/' + dictionary_output.get("output_file")
    if os.path.isfile(output):
        if os.access(output, os.W_OK):
            return
    if os.path.exists(output):
        print(f"Invalid file cause of permissions or type: {output}")
        exit(1)


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
    if (dictionary_output["width"] * dictionary_output["height"] > 1000000):
        print("the multiplicating between width and height cannot be bigger "
              "than 1000000")
        exit(1)
    check_output_file(dictionary_output)
    maze = Maze(**dictionary_output)
    sys.setrecursionlimit(maze.width * maze.height * 10)
    algorithms = Algorithms()
    algorithms.create_maze(maze)
    solve_maze(maze)
    Graphics(maze)


if __name__ == "__main__":
    main()

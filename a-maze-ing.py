#!/usr/bin/env python3

from Parser import Parser
from errors import ParseError, PerfectError, InvalidValueError
from typing import Any
from maze import Maze
from Prim import Prim
from mlx import Mlx


def close_hook(params: tuple[Any, Any, Any]) -> int:
    m: Mlx
    m, _, mlx_ptr = params
    m.mlx_loop_exit(mlx_ptr)
    return (1)


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
    m: Mlx = Mlx()
    mlx_ptr = m.mlx_init()
    win_ptr = m.mlx_new_window(mlx_ptr, 1000, 1000, "Maze")
    params = (m, win_ptr, mlx_ptr)
    m.mlx_hook(win_ptr, 33, 0, close_hook, params)
    m.mlx_loop(mlx_ptr)
    m.mlx_destroy_window(mlx_ptr, win_ptr)


if __name__ == "__main__":
    main()

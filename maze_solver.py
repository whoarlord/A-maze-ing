from maze import Maze


def solve_maze(maze: Maze) -> None:

    floodfill_map(maze)


def apply_floodfill(cell: tuple[int, int], maze: Maze) -> None:

    x, y = cell

    if maze.is_exit(cell):
        maze.get_cell(x, y).weight = 0

        cel = maze.get_cell(x+1, y)
        if cel:
            cel.weight = 1
            apply_floodfill((x+1, y), maze)

        cel = maze.get_cell(x-1, y)
        if cel:
            cel.weight = 1
            apply_floodfill((x-1, y), maze)

        cel = maze.get_cell(x, y+1)
        if cel:
            cel.weight = 1
            apply_floodfill((x, y+1), maze)

        cel = maze.get_cell(x, y-1)
        if cel:
            cel.weight = 1
            apply_floodfill((x, y-1), maze)

    else:
        cel = maze.get_cell(x+1, y)
        if cel and not cel.visited:
            cel.weight = maze.get_cell(x, y).weight + 1
            apply_floodfill((x+1, y), maze)

        cel = maze.get_cell(x-1, y)
        if cel and not cel.visited:
            cel.weight = maze.get_cell(x, y).weight + 1
            apply_floodfill((x-1, y), maze)

        cel = maze.get_cell(x, y)+1
        if cel and not cel.visited:
            cel.weight = maze.get_cell(x, y).weight + 1
            apply_floodfill((x, y+1), maze)

        cel = maze.get_cell(x, y-1)
        if cel and not cel.visited:
            cel.weight = maze.get_cell(x, y).weight + 1
            apply_floodfill((x, y-1), maze)


def floodfill_map(maze: Maze) -> None:

    flood_maze = Maze(maze.width, maze.height, maze.entry,
                      maze.exit, maze.output_file, maze.perfect)
    apply_floodfill(maze.exit, flood_maze)
    maze.print_wight_map()

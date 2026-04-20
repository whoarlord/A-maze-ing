from maze import Maze


def solve_maze(maze: Maze) -> None:

    floodfill_map(maze)


def apply_floodfill_neighbours(cell: tuple[int, int], maze: Maze) -> None:

    x, y = cell

    if (x+1) < maze.width:
        apply_floodfill((x+1, y), maze)

    if (x-1) >= 0:
        apply_floodfill((x-1, y), maze)

    if (y+1) < maze.height:
        apply_floodfill((x, y+1), maze)

    if (y-1) >= 0:
        apply_floodfill((x, y-1), maze)


def apply_floodfill(cell: tuple[int, int], maze: Maze) -> None:

    x, y = cell

    maze.get_cell(x, y).visited = True

    if maze.is_exit(cell):

        maze.get_cell(x, y).weight = 0

        if (x+1) < maze.width:
            cel = maze.get_cell(x+1, y)
            if not cel.visited:
                cel.weight = 1
                cel.visited = True

        if (x-1) >= 0:
            cel = maze.get_cell(x-1, y)
            if not cel.visited:
                cel.weight = 1
                cel.visited = True

        if (y+1) < maze.height:
            cel = maze.get_cell(x, y+1)
            if not cel.visited:
                cel.weight = 1
                cel.visited = True

        if (y-1) >= 0:
            cel = maze.get_cell(x, y-1)
            if not cel.visited:
                cel.weight = 1
                cel.visited = True

    else:
        if (x+1) < maze.width:
            cel = maze.get_cell(x+1, y)
            if not cel.visited:
                cel.weight = maze.get_cell(x, y).weight + 1
                cel.visited = True

        if (x-1) >= 0:
            cel = maze.get_cell(x-1, y)
            if not cel.visited:
                cel.weight = maze.get_cell(x, y).weight + 1
                cel.visited = True

        if (y+1) < maze.height:
            cel = maze.get_cell(x, y+1)
            if not cel.visited:
                cel.weight = maze.get_cell(x, y).weight + 1
                cel.visited = True

        if (y-1) >= 0:
            cel = maze.get_cell(x, y-1)
            if not cel.visited:
                cel.weight = maze.get_cell(x, y).weight + 1
                cel.visited = True

    apply_floodfill_neighbours(cell, maze)


def floodfill_map(maze: Maze) -> None:

    flood_maze = Maze(maze.width, maze.height, maze.entry,
                      maze.exit, maze.output_file, maze.perfect)
    apply_floodfill(maze.exit, flood_maze)
    flood_maze.print_wight_map()

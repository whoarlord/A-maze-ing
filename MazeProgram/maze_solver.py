from maze import Maze, Player


def solve_maze(maze: Maze) -> None:
    """This function finds the shortest path from the entry to the exit of the
      maze.

    This function finds the shortest path from the entry to the exit of the
    maze using the flood fill algorithm. It first creates a copy of the
    original maze without any walls and starts to apply the flood fill from
    the exit to get a first weight map. Then, as the player moves in the maze
    it adds the walls it finds to the copied maze and reapplys the flood fill
    again, taking inot acount the walls found untill that point.

    Args:
    - maze (Maze): the object with the representation of the maze we created.
    """
    all_not_visited(maze)
    apply_floodfill(maze.exit, maze)
    maze.print_wight_map()
    """ from Graphics import Graphics
    from Algorithms import Algorithms
    graphics = Graphics(flood_maze)
    algorithms = Algorithms()
    graphics.display_menu(flood_maze, algorithms)
    exit(1)
    return """

    player = Player(maze.entry)

    exit_x, exit_y = maze.exit
    paso = 0

    while True:

        x, y = move_player(flood_maze, maze, player)

        paso += 1

        if x == exit_x and y == exit_y:
            print(f"A path has been found from {maze.entry} to {maze.exit}")
            print("The path is the folowing: ", end="")
            player.print_path()
            print("\n")
            break
    maze.result_to_output(player.path_tostring())


def apply_floodfill_neighbours_start(
        cell: tuple[int, int],
        maze: Maze) -> None:

    x, y = cell

    if ((x+1) < maze.width and not maze.get_cell(x+1, y).visited and
            maze.get_cell(x, y).E == 0):
        apply_floodfill_start((x+1, y), maze)

    if ((x-1) >= 0 and not maze.get_cell(x-1, y).visited and
            maze.get_cell(x, y).W == 0):
        apply_floodfill_start((x-1, y), maze)

    if ((y+1) < maze.height and not maze.get_cell(x, y+1).visited and
            maze.get_cell(x, y).S == 0):
        apply_floodfill_start((x, y+1), maze)

    if ((y-1) >= 0 and not maze.get_cell(x, y-1).visited and
            maze.get_cell(x, y).N == 0):
        apply_floodfill_start((x, y-1), maze)


def apply_floodfill_start(cell: tuple[int, int], maze: Maze) -> None:

    x, y = cell

    maze.get_cell(x, y).visited = True

    if (x+1) < maze.width and maze.get_cell(x, y).E == 0:
        cel = maze.get_cell(x+1, y)
        if not cel.visited:
            if cel.weight != 0:
                cel.weight = min(cel.weight, maze.get_cell(x, y).weight + 1)
            else:
                cel.weight = maze.get_cell(x, y).weight + 1
        elif cel.weight > maze.get_cell(x, y).weight + 1:
            cel.weight = maze.get_cell(x, y).weight + 1

    if (x-1) >= 0 and maze.get_cell(x, y).W == 0:
        cel = maze.get_cell(x-1, y)
        if not cel.visited:
            if cel.weight != 0:
                cel.weight = min(cel.weight, maze.get_cell(x, y).weight + 1)
            else:
                cel.weight = maze.get_cell(x, y).weight + 1
        elif cel.weight > maze.get_cell(x, y).weight + 1:
            cel.weight = maze.get_cell(x, y).weight + 1

    if (y+1) < maze.height and maze.get_cell(x, y).S == 0:
        cel = maze.get_cell(x, y+1)
        if not cel.visited:
            if cel.weight != 0:
                cel.weight = min(cel.weight, maze.get_cell(x, y).weight + 1)
            else:
                cel.weight = maze.get_cell(x, y).weight + 1
        elif cel.weight > maze.get_cell(x, y).weight + 1:
            cel.weight = maze.get_cell(x, y).weight + 1

    if (y-1) >= 0 and maze.get_cell(x, y).N == 0:
        cel = maze.get_cell(x, y-1)
        if not cel.visited:
            if cel.weight != 0:
                cel.weight = min(cel.weight, maze.get_cell(x, y).weight + 1)
            else:
                cel.weight = maze.get_cell(x, y).weight + 1
        elif cel.weight > maze.get_cell(x, y).weight + 1:
            cel.weight = maze.get_cell(x, y).weight + 1

    apply_floodfill_neighbours_start(cell, maze)


def apply_floodfill_neighbours(cell: tuple[int, int], maze: Maze) -> None:
    """This function will apply the flood fill algorithm to the adjacent cells
    of the given cell, in the given map.

    This function takes a cell and applies the flood fill algorithm to the
    adjacent cells. To do this first it will check if the adjacent cell is
    accesible(if it's inside the maze's bounds and there is no wall between
    them). Then it will apply the flood fill to each adjacent cell.


    Args:
    - maze (Maze): the maze in witch we will apply the flood fill, which has
        all the weighs and visited for each cell.
    - cell (tuple[int, int]): the coordenates of the cell in the maze from
        where we will search the adjacent cells.
    """

    x, y = cell

    if ((x+1) < maze.width and not maze.get_cell(x+1, y).visited and
            maze.get_cell(x, y).E == 0):
        apply_floodfill((x+1, y), maze)

    if ((x-1) >= 0 and not maze.get_cell(x-1, y).visited and
            maze.get_cell(x, y).W == 0):
        apply_floodfill((x-1, y), maze)

    if ((y+1) < maze.height and not maze.get_cell(x, y+1).visited and
            maze.get_cell(x, y).S == 0):
        apply_floodfill((x, y+1), maze)

    if ((y-1) >= 0 and not maze.get_cell(x, y-1).visited and
            maze.get_cell(x, y).N == 0):
        apply_floodfill((x, y-1), maze)


def apply_floodfill(cell: tuple[int, int], maze: Maze) -> None:
    """This function will apply the flood fill algorithm to the given cell, in
    the given map.

    This function takes a cell and applies the flood fill algorithm. First, it
    will mark the cell as visited. Next, it will update the weigth of the
    adjacent cells. To do this, first it will check if the adjacent cell is
    accesible(if it's inside the maze's bounds and there is no wall between
    them). Then it will check if the adjacent cell has already been visited(
    the flood fill has already been applied to it). If it isn't visited, and
    the weight of the adjacent cell is not 0, the new weigth of that cell will
    be the minimum between the original cell's and that adjacent cell's weight.
    If the adjacent cell's weight was 0, it's new weight will be the origina
    cell's weight + 1. If the adjacent cell was visited, but it's weight is
    bigger than the original cell's weight + 1, that last weight will be the
    adjacent cell's new weight. After applying this in the four directions(
    North, South, West and East) then it will apply the flood fill starting
    from each adjacent cell.


    Args:
    - maze (Maze): the maze in witch we will apply the flood fill, which has
        all the weighs and visited for each cell.
    - cell (tuple[int, int]): the coordenates of the cell in the maze where we
        will apply the flood fill from.
    """

    x, y = cell

    maze.get_cell(x, y).visited = True

    if (x+1) < maze.width and maze.get_cell(x, y).E == 0:
        cel = maze.get_cell(x+1, y)

        if not cel.visited:
            if cel.weight != 0:
                cel.weight = min(cel.weight, maze.get_cell(x, y).weight + 1)
            else:
                cel.weight = maze.get_cell(x, y).weight + 1
        elif cel.weight > maze.get_cell(x, y).weight + 1:
            cel.weight = maze.get_cell(x, y).weight + 1

    if (x-1) >= 0 and maze.get_cell(x, y).W == 0:
        cel = maze.get_cell(x-1, y)

        if not cel.visited:
            if cel.weight != 0:
                cel.weight = min(cel.weight, maze.get_cell(x, y).weight + 1)
            else:
                cel.weight = maze.get_cell(x, y).weight + 1
        elif cel.weight > maze.get_cell(x, y).weight + 1:
            cel.weight = maze.get_cell(x, y).weight + 1

    if (y+1) < maze.height and maze.get_cell(x, y).S == 0:
        cel = maze.get_cell(x, y+1)

        if not cel.visited:
            if cel.weight != 0:
                cel.weight = min(cel.weight, maze.get_cell(x, y).weight + 1)
            else:
                cel.weight = maze.get_cell(x, y).weight + 1
        elif cel.weight > maze.get_cell(x, y).weight + 1:
            cel.weight = maze.get_cell(x, y).weight + 1

    if (y-1) >= 0 and maze.get_cell(x, y).N == 0:
        cel = maze.get_cell(x, y-1)

        if not cel.visited:
            if cel.weight != 0:
                cel.weight = min(cel.weight, maze.get_cell(x, y).weight + 1)
            else:
                cel.weight = maze.get_cell(x, y).weight + 1
        elif cel.weight > maze.get_cell(x, y).weight + 1:
            cel.weight = maze.get_cell(x, y).weight + 1

    apply_floodfill_neighbours(cell, maze)


def move_player(maze: Maze, player: Player
                ) -> tuple[int, int]:
    """This function will move the player to the next most optimal position.

    This function takes the player's actual position and moves it to the
    nearest cell with the smallest weigth possible. To do so, first we will
    update the walls of the flood_maze, taking into account if the player's
    current position and its posible movements. Then we will reset the
    flood_maze(put all weights to zero and all cells to not visited). Then,
    with the walls updated we will again apply the flood fill algorithm to the
    flood_maze to get the new cell weights. Finally, we will move the player
    to the next cell, searching for the cell with the smallest weight in the
    flood_maze.

    Args:
    - flood_maze (Maze): the copy of our original maze, with the weights of
        each cell.
    - original_maze (Maze): the object with the representation of the original
        maze we created.
    - player (Player): the object that has all the information of the player,
        such as his actual position in the maze.
    """

    move_to_lowest(player, maze)

    return (player.x, player.y)


def all_not_visited(maze: Maze) -> None:
    """This function puts all the cells from the given map to not visited.

    This function restets the cells of the given map, putting their visited
    atribute to False.

    Args:
    - maze (Maze): the object with the representation of the maze we want to
        reset.
    """

    for i in range(maze.height):
        for j in range(maze.width):
            maze.get_cell(j, i).visited = False


def all_weights_zero(maze: Maze) -> None:
    """This function puts all the weights from the given map to 0.

    This function restets the weights of the given map, putting the weight of
    each cell to 0.

    Args:
    - maze (Maze): the object with the representation of the maze we want to
        reset.
    """

    for i in range(maze.height):
        for j in range(maze.width):
            maze.get_cell(j, i).weight = 0


def all_weights_zero(maze: Maze) -> None:
    """This function puts all the weights from the given map to 0.

    This function restets the weights of the given map, putting the weight of
    each cell to 0.

    Args:
    - maze (Maze): the object with the representation of the maze we want to
        reset.
    """

    for i in range(maze.height):
        for j in range(maze.width):
            maze.get_cell(j, i).weight = 0

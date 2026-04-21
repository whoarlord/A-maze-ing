from maze import Maze, Player


def solve_maze(maze: Maze) -> None:

    floodfill_map(maze)


def apply_floodfill_neighbours_start(cell: tuple[int, int], maze: Maze) -> None:

    x, y = cell

    if (x+1) < maze.width and not maze.get_cell(x+1, y).visited and maze.get_cell(x, y).E == 0:
        apply_floodfill_start((x+1, y), maze)

    if (x-1) >= 0 and not maze.get_cell(x-1, y).visited and maze.get_cell(x, y).W == 0:
        apply_floodfill_start((x-1, y), maze)

    if (y+1) < maze.height and not maze.get_cell(x, y+1).visited and maze.get_cell(x, y).S == 0:
        apply_floodfill_start((x, y+1), maze)

    if (y-1) >= 0 and not maze.get_cell(x, y-1).visited and maze.get_cell(x, y).N == 0:
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

    x, y = cell

    # print(f" ===== FloodFill on neighbours of cell: ({x}, {y}) ====== ")

    if (x+1) < maze.width and not maze.get_cell(x+1, y).visited and maze.get_cell(x, y).E == 0:
        apply_floodfill((x+1, y), maze)

    if (x-1) >= 0 and not maze.get_cell(x-1, y).visited and maze.get_cell(x, y).W == 0:
        apply_floodfill((x-1, y), maze)

    if (y+1) < maze.height and not maze.get_cell(x, y+1).visited and maze.get_cell(x, y).S == 0:
        apply_floodfill((x, y+1), maze)

    if (y-1) >= 0 and not maze.get_cell(x, y-1).visited and maze.get_cell(x, y).N == 0:
        apply_floodfill((x, y-1), maze)


def apply_floodfill(cell: tuple[int, int], maze: Maze) -> None:

    x, y = cell

    maze.get_cell(x, y).visited = True

    # print(f"FloodFill on cell: ({x}, {y})")

    if (x+1) < maze.width and maze.get_cell(x, y).E == 0:
        cel = maze.get_cell(x+1, y)
        # print(f"Cell ({x+1}, {y}) - Weight = {cel.weight}")
        if not cel.visited:
            if cel.weight != 0:
                cel.weight = min(cel.weight, maze.get_cell(x, y).weight + 1)
            else:
                cel.weight = maze.get_cell(x, y).weight + 1
        elif cel.weight > maze.get_cell(x, y).weight + 1:
            cel.weight = maze.get_cell(x, y).weight + 1
            # print(f"Pasa por elif celda: ({x}, {y}) para rellenar {x+1}, {y}")
        # maze.print_wight_map()

    if (x-1) >= 0 and maze.get_cell(x, y).W == 0:
        cel = maze.get_cell(x-1, y)
        # print(f"Cell ({x-1}, {y}) - Weight = {cel.weight}")
        if not cel.visited:
            if cel.weight != 0:
                cel.weight = min(cel.weight, maze.get_cell(x, y).weight + 1)
            else:
                cel.weight = maze.get_cell(x, y).weight + 1
        elif cel.weight > maze.get_cell(x, y).weight + 1:
            cel.weight = maze.get_cell(x, y).weight + 1
            # print(f"Pasa por elif celda: ({x}, {y}) para rellenar {x-1}, {y}")
        # maze.print_wight_map()

    if (y+1) < maze.height and maze.get_cell(x, y).S == 0:
        cel = maze.get_cell(x, y+1)
        # print(f"Cell ({x}, {y+1}) - Weight = {cel.weight}")
        if not cel.visited:
            if cel.weight != 0:
                cel.weight = min(cel.weight, maze.get_cell(x, y).weight + 1)
            else:
                cel.weight = maze.get_cell(x, y).weight + 1
        elif cel.weight > maze.get_cell(x, y).weight + 1:
            cel.weight = maze.get_cell(x, y).weight + 1
            # print(f"Pasa por elif celda: ({x}, {y}) para rellenar {x}, {y+1}")
        # maze.print_wight_map()

    if (y-1) >= 0 and maze.get_cell(x, y).N == 0:
        cel = maze.get_cell(x, y-1)
        # print(f"Cell ({x}, {y-1}) - Weight = {cel.weight}")
        if not cel.visited:
            if cel.weight != 0:
                cel.weight = min(cel.weight, maze.get_cell(x, y).weight + 1)
            else:
                cel.weight = maze.get_cell(x, y).weight + 1
        elif cel.weight > maze.get_cell(x, y).weight + 1:
            cel.weight = maze.get_cell(x, y).weight + 1
            # print(f"Pasa por elif celda: ({x}, {y}) para rellenar {x}, {y-1}")
        # maze.print_wight_map()

    apply_floodfill_neighbours(cell, maze)


def update_walls(
        player: Player,
        original_maze: Maze, flood_maze: Maze) -> None:

    if not player.can_move_to("N", original_maze):
        flood_maze.get_cell(player.x, player.y).N = 1
    if not player.can_move_to("S", original_maze):
        flood_maze.get_cell(player.x, player.y).S = 1
    if not player.can_move_to("W", original_maze):
        flood_maze.get_cell(player.x, player.y).W = 1
    if not player.can_move_to("E", original_maze):
        flood_maze.get_cell(player.x, player.y).E = 1


def move_to_lowest(player: Player, flood_maze: Maze) -> None:

    x, y = flood_maze.find_lowest_neighbour((player.x, player.y), player)
    print(f"Direction to move: {player.get_direction((x, y))}")
    player.move_to(player.get_direction((x, y)))
    print(f"Player pos after move: X={player.x}, Y={player.y}")


def move_player(flood_maze: Maze, original_maze: Maze, player: Player) -> tuple[int, int]:

    print("Funcion move_player")
    update_walls(player, original_maze, flood_maze)
    print(
        f"Updated walls of cell:{player.x}, {player.y}: N:{flood_maze.get_cell(player.x, player.y).N}, E:{flood_maze.get_cell(player.x, player.y).E}"
        f" S:{flood_maze.get_cell(player.x, player.y).S}, W:{flood_maze.get_cell(player.x, player.y).W}")
    all_weights_zero(flood_maze)
    all_not_visited(flood_maze)
    apply_floodfill(original_maze.exit, flood_maze)
    print("Flood_maze with walls")
    flood_maze.print_wight_map()
    move_to_lowest(player, flood_maze)

    return (player.x, player.y)


def all_not_visited(maze: Maze) -> None:

    for i in range(maze.height):
        for j in range(maze.width):
            maze.get_cell(j, i).visited = False


def all_weights_zero(maze: Maze) -> None:

    for i in range(maze.height):
        for j in range(maze.width):
            maze.get_cell(j, i).weight = 0


def floodfill_map(maze: Maze) -> None:

    flood_maze = Maze(maze.width, maze.height, maze.entry,
                      maze.exit, maze.output_file, maze.perfect)
    apply_floodfill_start(maze.exit, flood_maze)
    all_not_visited(flood_maze)

    flood_maze.print_wight_map()

    player = Player(maze.entry)

    exit_x, exit_y = maze.exit
    while True:
        x, y = move_player(flood_maze, maze, player)
        print(f"move_x={x}, move_y={y}; exit_x={exit_x}, exit_y={exit_y}")

        if x == exit_x and y == exit_y:
            break

from typing import Any
from maze import Player
from functools import reduce
from random import randint, shuffle, seed


class MazeGenerator:

    maze: "Maze"

    def __init__(self, dictionary: dict[str: Any]):
        self.maze = MazeGenerator.Maze(**dictionary)
        self.create_map()

    # def get_maze(self) -> "Maze":

    def create_map(self) -> None:
        """This function creates the maze based on the config file

        This function creates a seed or uses the seed from the maze if it is
        greater than 0, and then create a maze based on that seed and the
        algorithm specified at the maze.algorithm

        Args:
        - maze (Maze): the object with the specified configuration of the maze
        """
        if self.maze.seed <= 0:
            self.create_seed()
        else:
            seed(self.maze.seed)
        if self.maze.algorithm == "kruskal":
            self.create_map_kruskal()
        elif self.maze.algorithm == "prim":
            self.create_map_prim()

    def create_seed(self) -> None:
        """Function for creating a random seed for the maze"""
        number: int = 0
        for i in range(self.maze.height):
            for j in range(self.maze.width):
                number = (number + randint(0, 15)) * 16
        self.maze.seed = number
        seed(number)

    def create_map_kruskal(self) -> None:
        """Function for creating a map using the kruskal algorithm

        This function put up all the walls of the maze and then it gives to
        each of them a group, the objective is to change the group of all the
        cells by destroying walls.

        It selects a random direction from one cell to an adyacent cell which
        is not at the same group and destroys the wall between them changing
        all the cells group to the same group

        Args:
        - maze (Maze): the class where the maze is gonna be placed
        """
        print("Executing kruskal algorithm\n")
        cell_list: list[tuple[int, int]] = []
        cell_group: list[int] = []
        group_id: int = 0
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                cell: MazeGenerator.Cell = self.maze.get_cell(x, y)
                if cell.block_42:
                    continue
                cell.cover_all()
                cell_list.append((x, y))
                cell_group.append(group_id)
                group_id += 1
        shuffle(cell_list)
        while (self.check_group(cell_group)):
            for i in range(len(cell_list)):
                x, y = cell_list[i]
                directions: list[int] = self.not_same_group_cells(
                    self.maze, x, y, i, cell_list, cell_group)
                if len(directions) == 0:
                    continue
                rand_dir = randint(0, len(directions) - 1)
                temp_x, temp_y = self.maze.get_coord_by_dir(
                    x, y, directions[rand_dir])
                actual_cell = self.maze.get_cell(x, y)
                temp_cell = self.maze.get_cell(temp_x, temp_y)
                actual_cell.uncover_dir_flex(
                    temp_cell, directions[rand_dir])
                self.update_group(temp_x, temp_y, cell_group,
                                  cell_list, cell_group[i])
        if not self.maze.perfect:
            self.create_multiple_routes(
                self.maze, min(self.maze.width, self.maze.height))

    def update_group(self, x: int, y: int, cell_group: list[int],
                     cell_list: list[tuple[int, int]], new_group: int) -> None:
        """Function for updating the group of a cell"""
        group_id_to_update: int = self.get_group_from_cell(
            x, y, cell_group, cell_list)
        for i in range(len(cell_group)):
            if cell_group[i] == group_id_to_update:
                cell_group[i] = new_group

    @staticmethod
    def check_group(cell_group: list[int]) -> bool:
        """Function if all cells corresponds to the same group"""
        group_id: int = cell_group[0]
        for group in cell_group:
            if group != group_id:
                return True
        return False

    @staticmethod
    def get_group_from_cell(
            x: int, y: int, cell_group: list[int],
            cell_list: list[tuple[int, int]]) -> int:
        """Function for getting the group of a cell"""
        for i in range(len(cell_list)):
            if cell_list[i] == (x, y):
                return cell_group[i]
        return (0)

    def not_same_group_cells(
            self, maze: "Maze", x: int, y: int, i: int,
            cell_list: list[tuple[int, int]],
            cell_group: list[int]) -> list[int]:
        """Function for checking adyacents cells group

        This function checks if adyacents cells are from a diferent group
        and if they are it adds that direction to the list so the main
        kruskal function can choose one direction randomly

        Args:
        - maze (Maze): the object representing the maze is gonna be created
        - x (int): the x coordinate of the actual cell in the maze
        - y (int): the y coordinate of the actual cell in the maze
        - i (int): the index of the actual cell group at the cell_group
        - cell_list (list[tuple[int, int]]): the list with the tuples
        corresponding to the coordinates of each cell
        - cell_group (list[int]): the list containing the group of each cell

        Returns:
        - directions (list[int]): the list with the posible directions to
        destroy walls
        """
        directions: list[int] = []
        if (y - 1 >= 0
                and self.get_group_from_cell(x, y - 1, cell_group, cell_list)
                != cell_group[i] and not maze.get_cell(x, y - 1).block_42):
            directions.append(0)
        if (y + 1 < maze.height
                and self.get_group_from_cell(x, y + 1, cell_group, cell_list)
                != cell_group[i] and not maze.get_cell(x, y + 1).block_42):
            directions.append(2)
        if (x + 1 < maze.width
                and self.get_group_from_cell(x + 1, y, cell_group, cell_list)
                != cell_group[i] and not maze.get_cell(x + 1, y).block_42):
            directions.append(1)
        if (x - 1 >= 0
                and self.get_group_from_cell(x - 1, y, cell_group, cell_list)
                != cell_group[i] and not maze.get_cell(x - 1, y).block_42):
            directions.append(3)
        return directions

    def create_map_prim(self) -> None:
        """Function for creating a maze based on prim algorithm

        This function receives creates a maze based on the prim algorithm
        for that it start from the entry covering it by walls and select
        a random direction which it has not being visited,
        then it destroy the wall for that direction and creates new walls
        around the new cell.

        It continue iterating until it have visited all the cells
        In the case that we are looking for a non perfect maze we call a
        function for destroying walls

        Args:
        - maze (Maze): the object representing the parameters for the maze
        we are gonna create
        """
        print("Executing prim algorithm\n")
        stack: list[tuple[int, int]] = [self.maze.entry]
        x, y = stack[-1]
        self.maze.maze_map[y][x].cover_all()
        while (len(stack) > 0):
            x, y = stack[-1]
            actual_cell: MazeGenerator.Cell = self.maze.get_cell(x, y)
            directions: list[int] = self.maze.not_visited_neighbours(x, y)
            if len(directions) == 0:
                stack.pop()
                continue
            rand_dir = randint(0, len(directions) - 1)
            temp_x, temp_y = self.maze.get_coord_by_dir(
                x, y, directions[rand_dir])
            temp_cell = self.maze.get_cell(temp_x, temp_y)
            actual_cell.uncover_dir(temp_cell, directions[rand_dir])

            stack.append((temp_x, temp_y))
        if not self.maze.perfect:
            self.create_multiple_routes(
                self.maze, min(self.maze.width, self.maze.height))

    def check_neighbours_for_routes(
            self, maze: "Maze", threshold: int, x: int, y: int) -> None:
        """Checks the distance between a cell and their adyacent

        This function receive a position of a cell a maze where the cell is
        and a threshold and checks if a specific cell is further from an
        adyacent cell than the threshold and destroys the wall between them
        to make an non perfect maze

        Args:
        - maze (Maze): the object representing the maze is gonna be created
        - threshold (int): the threshold to make decisions about destroying
        the walls
        - x (int): the x coordinate of the actual cell
        - y (int): the y coordinate fo the actual cell
        """
        if (y - 1 >= 0 and not maze.get_cell(x, y - 1).block_42
                and maze.distance_between_cells(x, y, x, y - 1)
                > threshold):
            maze.get_cell(x, y).uncover_dir_flex(maze.get_cell(x, y - 1), 0)
        if (y + 1 < maze.height and not maze.get_cell(x, y + 1).block_42
                and maze.distance_between_cells(x, y, x, y + 1)
                > threshold):
            maze.get_cell(x, y).uncover_dir_flex(maze.get_cell(x, y + 1), 2)
        if (x + 1 < maze.width and not maze.get_cell(x + 1, y).block_42
                and maze.distance_between_cells(x, y, x + 1, y)
                > threshold):
            maze.get_cell(x, y).uncover_dir_flex(maze.get_cell(x + 1, y), 1)
        if (x - 1 >= 0 and not maze.get_cell(x - 1, y).block_42
                and maze.distance_between_cells(x, y, x - 1, y)
                > threshold):
            maze.get_cell(x, y).uncover_dir_flex(maze.get_cell(x - 1, y), 1)

    def create_multiple_routes(
            self, maze: "Maze", threshold: int = 10) -> None:
        """This function destroys walls between cells based on the threshold"""
        for y in range(maze.height):
            for x in range(maze.width):
                self.check_neighbours_for_routes(maze, threshold, x, y)

    class Maze:

        def __init__(
                self, width: int, height: int, entry: tuple[int, int],
                exit: tuple[int, int],
                output_file: str, perfect: bool, animation: bool,
                algorithm: str, seed: int):
            self.width = width
            self.height = height
            self.entry = entry
            self.exit = exit
            self.output_file = output_file
            self.perfect = perfect
            self.animation = animation
            self.algorithm = algorithm
            self.seed = seed
            self.maze_map: list[list[MazeGenerator.Cell]] = self.create_map()
            if (self.create_42()):
                self.maze_map = self.create_map()
            self.route: str = ""

        def create_map(self) -> list[list["MazeGenerator.Cell"]]:
            result: list[list[MazeGenerator.Cell]] = []
            for i in range(self.height):
                row: list[MazeGenerator.Cell] = []
                for j in range(self.width):
                    row.append(MazeGenerator.Cell())
                result.append(row)
            return result

        def get_cell(self, x: int, y: int) -> "MazeGenerator.Cell":
            return self.maze_map[y][x]

        def re_generate(self):
            self.seed = 0
            self.maze_map = self.create_map()
            if (self.create_42()):
                self.maze_map = self.create_map()

        def not_visited_neighbours(self, x: int, y: int) -> list[int]:
            """
            dir = 0: move N
            dir = 1: move E
            dir = 2: move S
            dir = 3: move W
            """
            result: list[int] = []
            if (y - 1 >= 0 and not self.get_cell(x, y - 1).visited):
                result.append(0)
            if (x + 1 < self.width and not self.get_cell(x + 1, y).visited):
                result.append(1)
            if (y + 1 < self.height and not self.get_cell(x, y + 1).visited):
                result.append(2)
            if (x - 1 >= 0 and not self.get_cell(x - 1, y).visited):
                result.append(3)
            return result

        def get_adyacents(self, x: int, y: int, checked_cells:
                          list[tuple[int, int]]) -> list[tuple[int, int]]:
            result: list[tuple[int, int]] = []
            actual_cell: MazeGenerator.Cell = self.get_cell(x, y)
            if not actual_cell.N and not (x, y - 1) in checked_cells:
                result.append((x, y - 1))
            if not actual_cell.S and not (x, y + 1) in checked_cells:
                result.append((x, y + 1))
            if not actual_cell.W and not (x - 1, y) in checked_cells:
                result.append((x - 1, y))
            if not actual_cell.E and not (x + 1, y) in checked_cells:
                result.append((x + 1, y))
            return result

        def get_coord_by_dir(self, x: int, y: int, dir: int) -> tuple[int, int]:
            if dir == 0:
                return x, y - 1
            elif dir == 1:
                return x + 1, y
            elif dir == 2:
                return x, y + 1
            elif dir == 3:
                return x - 1, y
            else:
                raise ValueError("Unknow direction")

        def check_42_collisiones(self, x: int, y: int):
            return ((self.entry[0] == x and self.entry[1] == y)
                    or (self.exit[0] == x and self.exit[1] == y))

        def create_42(self) -> int:
            """The 42 must have a width of 7 and a height of 5"""
            x1: int = int(self.width / 2 - 3)
            y1: int = int(self.height / 2 - 2)
            x2: int = x1 + 7
            y2: int = y1 + 5
            if (x1 < 0 or x2 >= self.width or y1 < 0 or y2 >= self.height):
                print("The number 42 cannot be printed cause of space")
                return (0)
            moving_y: int = y1
            while (moving_y < y2):
                moving_x: int = x1
                while (moving_x < x2):
                    if (moving_x == x1 and moving_y - y1 < 3):
                        if self.check_42_collisiones(moving_x, moving_y):
                            print("The number 42 cannot be printed cause of "
                                  "collision")
                            return (1)
                        self.get_cell(moving_x, moving_y).cell_42(
                            moving_x, moving_y, self)
                    elif (moving_x == x1 + 1 and moving_y - y1 == 2):
                        if self.check_42_collisiones(moving_x, moving_y):
                            print("The number 42 cannot be printed cause of "
                                  "collision")
                            return (1)
                        self.get_cell(moving_x, moving_y).cell_42(
                            moving_x, moving_y, self)
                    elif (moving_x == x1 + 2 and moving_y - y1 >= 2):
                        if self.check_42_collisiones(moving_x, moving_y):
                            print("The number 42 cannot be printed cause of "
                                  "collision")
                            return (1)
                        self.get_cell(moving_x, moving_y).cell_42(
                            moving_x, moving_y, self)
                    elif ((moving_y == y1 or moving_y == y1 + 2
                           or moving_y == y1 + 4)
                          and moving_x - x1 > 3):
                        if self.check_42_collisiones(moving_x, moving_y):
                            print("The number 42 cannot be printed cause of "
                                  "collision")
                            return (1)
                        self.get_cell(moving_x, moving_y).cell_42(
                            moving_x, moving_y, self)
                    elif (moving_y == y1 + 1 and moving_x - x1 == 6):
                        if self.check_42_collisiones(moving_x, moving_y):
                            print("The number 42 cannot be printed cause of "
                                  "collision")
                            return (1)
                        self.get_cell(moving_x, moving_y).cell_42(
                            moving_x, moving_y, self)
                    elif (moving_y == y1 + 3 and moving_x - x1 == 4):
                        if self.check_42_collisiones(moving_x, moving_y):
                            print("The number 42 cannot be printed cause of "
                                  "collision")
                            return (1)
                        self.get_cell(
                            moving_x, moving_y).cell_42(
                            moving_x, moving_y, self)
                    moving_x += 1
                moving_y += 1
            return (0)

        def distance_between_cells(
                self, x1: int, y1: int, x2: int, y2: int) -> int:
            cells_list: list[tuple[int, int]] = [(x1, y1)]
            checked_cells: list[tuple[int, int]] = []
            distance: int = 0
            while (len(cells_list)) > 0:
                distance += 1
                for i in range(len(cells_list)):
                    x, y = cells_list.pop(0)
                    cells_list.extend(self.get_adyacents(x, y, checked_cells))
                    checked_cells.append((x, y))
                if (x2, y2) in cells_list:
                    break
            return distance

        def map_to_str(self) -> str:
            result: str = ""
            for i in range(self.height):
                for j in range(self.width):
                    result += self.maze_map[i][j].__str__()
                result += "\n"
            result += "\n"
            return result

        def is_exit(self, cell: tuple[int, int]) -> bool:
            return self.exit == cell

        def is_entry(self, cell: tuple[int, int]) -> bool:
            return self.entry == cell

        def find_lowest_neighbour(self, cell: tuple[int, int],
                                  player: Player) -> tuple[int, int]:

            x, y = cell
            posible_moves: dict[tuple[int, int], int] = {}
            cel = self.get_cell(x, y)

            if not cel.has_wall("N") and y > 0:
                posible_moves.update({(x, y-1): self.get_cell(x, y-1).weight})

            if not cel.has_wall("S") and y < self.height - 1:
                posible_moves.update({(x, y+1): self.get_cell(x, y+1).weight})

            if not cel.has_wall("E") and x < self.width - 1:
                posible_moves.update(
                    {(x + 1, y): self.get_cell(x+1, y).weight})

            if not cel.has_wall("W") and x > 0:
                posible_moves.update({(x-1, y): self.get_cell(x-1, y).weight})

            min_weight = reduce(min, posible_moves.values())

            result = {
                key: value for key, value in posible_moves.items()
                if value <= min_weight}

            return_x: int
            return_y: int

            all_routed: bool = True
            for coords in result.keys():
                return_x, return_y = coords
                if not self.get_cell(return_x, return_y).routed:
                    all_routed = False
                    break

            if all_routed:
                last_movement = player.last_coordenate()
                print(f"Last movement: {last_movement}")
                test_x, test_y = list(result.keys())[0]
                print(f"{result}, {self.get_cell(test_x, test_y).routed}")
                if len(player.movements) == 0:
                    self.print_wight_map()
                    from Graphics import Graphics
                    from MazeProgram.Maze_Generator import Algorithms
                    self.route = player.path_tostring()
                    print(f"Player position: {self.get_cell(3, 18).routed}")
                    graphics = Graphics(self)
                    algorithms = Algorithms()
                    graphics.display_menu(self, algorithms)
                    exit(1)
                    return self.exit
                player.backtracking()
                if player.contador == 5:
                    from Graphics import Graphics
                    from MazeProgram.Maze_Generator import Algorithms
                    self.route = player.path_tostring()
                    print(f"Player position: {self.get_cell(3, 18).routed}")
                    graphics = Graphics(self)
                    algorithms = Algorithms()
                    graphics.display_menu(self, algorithms)
                if test_x == 4 and test_y == 18:
                    player.contador += 1
                return player.x, player.y

            self.get_cell(return_x, return_y).routed = True
            return return_x, return_y

        def result_to_output(self, solution: str):
            self.route = solution
            print(self.route)
            with open(self.output_file, "w") as f:
                f.write(self.map_to_str())
                f.write(f"{self.entry[0]},{self.entry[1]}\n")
                f.write(f"{self.exit[0]},{self.exit[1]}\n")
                f.write(f"{solution}\n\n")
            print(f"Seed:{self.seed}\n")

        def print_wight_map(self):

            # Metodo de testeo, luego borrar

            print("Weight Map:")
            for i in range(self.height):
                for j in range(self.width):
                    print(self.maze_map[i][j].weight, " ", end="")
                print("")
            print()

    class Cell:
        def __init__(self):
            self.visited: bool = False
            self.block_42: bool = False
            self.routed: bool = False
            self.weight = 0
            self.N = 0
            self.S = 0
            self.E = 0
            self.W = 0

        def cover_all(self):
            self.visited = True
            self.N = 1
            self.S = 1
            self.E = 1
            self.W = 1

        def cell_42(self, x: int, y: int, maze: "MazeGenerator.Maze") -> None:
            self.block_42 = True
            self.cover_all()
            maze.get_cell(x+1, y).W = 1
            maze.get_cell(x-1, y).E = 1
            maze.get_cell(x, y+1).N = 1
            maze.get_cell(x, y-1).S = 1

        def uncover_dir_flex(
                self, visiting_cell: "MazeGenerator.Cell", dir: int) -> None:
            if dir == 0:
                self.N = 0
                visiting_cell.S = 0
            elif dir == 1:
                self.E = 0
                visiting_cell.W = 0
            elif dir == 2:
                self.S = 0
                visiting_cell.N = 0
            elif dir == 3:
                self.W = 0
                visiting_cell.E = 0
            else:
                raise ValueError("Unknow direction")

        def uncover_dir(
                self, visiting_cell: "MazeGenerator.Cell", dir: int) -> None:
            visiting_cell.cover_all()
            self.uncover_dir_flex(visiting_cell, dir)

        def calculate_walls(self) -> int:
            return self.N * 1 + self.E * 2 + self.S * 4 + self.W * 8

        def has_wall(self, direction: str) -> bool:

            match direction:
                case "N":
                    return self.N == 1
                case "E":
                    return self.E == 1
                case "S":
                    return self.S == 1
                case "W":
                    return self.W == 1

        def __str__(self):
            hexadeimal: str = "0123456789ABCDEF"
            return f"{hexadeimal[self.calculate_walls()]}"

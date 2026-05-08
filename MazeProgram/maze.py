from functools import reduce
from .Player import Player


class Cell:
    """A class representing a cell

    Attributes:
        visited (bool): boolean specifying if the cell was visited
        block_42 (bool): boolean specfying if the cell is part of 42 block
        routed (bool): boolean specfying if the route pass through that way
        N (int): int representing the wall on the North
        S (int): int representing the wall on the South
        E (int): int representing the wall on the East
        W (int): int representing the wall on the West
    """

    def __init__(self) -> None:
        self.visited: bool = False
        self.block_42: bool = False
        self.routed: bool = False
        self.weight = 0
        self.N = 0
        self.S = 0
        self.E = 0
        self.W = 0

    def cover_all(self) -> None:
        """This function raise all the walls of the cell"""
        self.visited = True
        self.N = 1
        self.S = 1
        self.E = 1
        self.W = 1

    def cell_42(self, x: int, y: int, maze: "Maze") -> None:
        """This function raise the walls for the 42"""
        self.block_42 = True
        self.cover_all()
        maze.get_cell(x+1, y).W = 1
        maze.get_cell(x-1, y).E = 1
        maze.get_cell(x, y+1).N = 1
        maze.get_cell(x, y-1).S = 1

    def uncover_dir_flex(self, visiting_cell: "Cell", dir: int) -> None:
        """This function destroys a wall from a cell based on direction"""
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

    def uncover_dir(self, visiting_cell: "Cell", dir: int) -> None:
        """This function uncover"""
        visiting_cell.cover_all()
        self.uncover_dir_flex(visiting_cell, dir)

    def calculate_walls(self) -> int:
        """calculates the number representing the walls of the cell"""
        return self.N * 1 + self.E * 2 + self.S * 4 + self.W * 8

    def has_wall(self, direction: str) -> bool:
        """checks if a cell have a wall in a specific direction"""
        match direction:
            case "N":
                return self.N == 1
            case "E":
                return self.E == 1
            case "S":
                return self.S == 1
            case "W":
                return self.W == 1
        return False

    def __str__(self) -> str:
        hexadeimal: str = "0123456789ABCDEF"
        return f"{hexadeimal[self.calculate_walls()]}"


class Maze:
    """Class representing the maze

    Attributes:
        width (int): the width of the maze
        height (int): the height of the maze
        entry (tuple[int, int]): the tuple representing the entry cell
        exit (tuple[int, int]): the tuple representing the exit cell
        output_file (str): the name of the file to write the output
        perfect (bool): boolean specifying if is a perfect maze or not
        animation (bool): boolean specifying if the display is gonna be
                animated
        algorithm (str): the specific algorithm is gonna be used to make the
                maze
        seed (int): the seed to make the maze
        maze_map (list[list[Cell]]): the matrix representing the whole maze
    """

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
        self.maze_map: list[list[Cell]] = self.create_map()
        if (self.create_42()):
            self.maze_map = self.create_map()
        self.route: str = ""

    def create_map(self) -> list[list[Cell]]:
        """Function for initializing the cells"""
        result: list[list[Cell]] = []
        for i in range(self.height):
            row: list[Cell] = []
            for j in range(self.width):
                row.append(Cell())
            result.append(row)
        return result

    def get_cell(self, x: int, y: int) -> Cell:
        """function for getting the cells with the x and y coordinates"""
        return self.maze_map[y][x]

    def re_generate(self) -> None:
        """function for re-generating the whole maze"""
        self.seed = 0
        self.maze_map = self.create_map()
        if (self.create_42()):
            self.maze_map = self.create_map()

    def not_visited_neighbours(self, x: int, y: int) -> list[int]:
        """Function for obteining the not visite cell neighbours

        this function checks if the cells around the one gived have been
        visited and adds them to the result list if they are not visited.

        Directionss:
        - dir = 0: move N
        - dir = 1: move E
        - dir = 2: move S
        - dir = 3: move W

        Args:
            x (int): the x coordinate of the actual cell
            y (int):_the y coordinate of the actual cell

        Returns:
            list[int]: list fo directions for not visited neighbours
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
        """returns a list of directions with the non-checked cells

        This function takes the coordinates of the actual cell and the
        list of the checked cells and then returns the adyacents cells
        that are not at the checked cells

        Args:
            x (int): the x coordinate of the actual cell
            y (int): the y coordinate of the actual cell
            checked_cells (list[tuple[int, int]]): the list of the checked
                    cells

        Returns:
            list[tuple[int, int]]: the list of the adyacent cells which are
                    not in the checked_cells list
        """
        result: list[tuple[int, int]] = []
        actual_cell: Cell = self.get_cell(x, y)
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
        """This function takes a direction and return the corresponding cell"""
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

    def check_42_collisiones(self, x: int, y: int) -> bool:
        """This function checks if the entry or exit collide with the 42"""
        return ((self.entry[0] == x and self.entry[1] == y)
                or (self.exit[0] == x and self.exit[1] == y))

    def create_42(self) -> int:
        """This functions tries to create a 42 in the middle of the maze

        The 42 must have a width greater or equal than 9 and
        a height greater or equal than 7,
        and must not collide with the entry or exit

        Returns
            int: 0 if the 42 can be created and 1 if not
        """
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
        """This function checks the distance between 2 cells

        This functions makes aa BFS search for checking the distance between
        2 cells, by expanding the initial cell until getting into end cell
        and return the distance

        Args:
            x1 (int): the x coordinate of the initial cell
            y1 (int): the y coordinate of the initial cell
            x2 (int): the x coordinate of the end cell
            y2 (int): the y coordiante of the end cell

        Returns:
            int: the distance between both cells
        """
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
        """Makes the string based on the map for the output file"""
        result: str = ""
        for i in range(self.height):
            for j in range(self.width):
                result += self.maze_map[i][j].__str__()
            result += "\n"
        result += "\n"
        return result

    def find_lowest_neighbour(self, cell: tuple[int, int],
                              player: Player) -> tuple[int, int]:
        """Calculates the lowest cost neighbour for the floodfill"""
        x, y = cell
        posible_moves: dict[tuple[int, int], int] = {}
        cel = self.get_cell(x, y)

        if not cel.has_wall("N") and y > 0:
            posible_moves.update({(x, y-1): self.get_cell(x, y-1).weight})

        if not cel.has_wall("S") and y < self.height - 1:
            posible_moves.update({(x, y+1): self.get_cell(x, y+1).weight})

        if not cel.has_wall("E") and x < self.width - 1:
            posible_moves.update({(x + 1, y): self.get_cell(x+1, y).weight})

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
            player.backtracking()
            return player.x, player.y

        self.get_cell(return_x, return_y).routed = True
        return return_x, return_y

    def result_to_output(self, solution: str) -> None:
        """puts the corresponding information in the ourput file"""
        self.route = solution
        with open(self.output_file, "w") as f:
            f.write(self.map_to_str())
            f.write(f"{self.entry[0]},{self.entry[1]}\n")
            f.write(f"{self.exit[0]},{self.exit[1]}\n")
            f.write(f"{solution}\n\n")
        print(f"Seed:{self.seed}\n")

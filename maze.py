from functools import lru_cache


class Cell:
    def __init__(self):
        self.visited: bool = False
        self.block_42: bool = False
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

    def cell_42(self):
        self.block_42 = True
        self.cover_all()

    def uncover_dir_flex(self, visiting_cell: "Cell", dir: int) -> None:
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
        visiting_cell.cover_all()
        self.uncover_dir_flex(visiting_cell, dir)

    def calculate_walls(self) -> int:
        return self.N * 1 + self.E * 2 + self.S * 4 + self.W * 8

    def __str__(self):
        hexadeimal: str = "0123456789ABCDEF"
        return f"{hexadeimal[self.calculate_walls()]}"


class Maze:

    def __init__(
            self, width: int, height: int, entry: tuple[int, int],
            exit: tuple[int, int], output_file: str, perfect: bool):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.output_file = output_file
        self.perfect = perfect
        self.maze_map: list[list[Cell]] = self.create_map()
        if (self.create_42()):
            self.maze_map = self.create_map()

    def create_map(self) -> list[list[Cell]]:
        result: list[list[Cell]] = []
        for i in range(self.height):
            row: list[Cell] = []
            for j in range(self.width):
                row.append(Cell())
            result.append(row)
        return result

    def get_cell(self, x: int, y: int) -> Cell:
        return self.maze_map[y][x]

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
                    self.get_cell(moving_x, moving_y).cell_42()
                elif (moving_x == x1 + 1 and moving_y - y1 == 2):
                    if self.check_42_collisiones(moving_x, moving_y):
                        print("The number 42 cannot be printed cause of "
                              "collision")
                        return (1)
                    self.get_cell(moving_x, moving_y).cell_42()
                elif (moving_x == x1 + 2 and moving_y - y1 >= 2):
                    if self.check_42_collisiones(moving_x, moving_y):
                        print("The number 42 cannot be printed cause of "
                              "collision")
                        return (1)
                    self.get_cell(moving_x, moving_y).cell_42()
                elif ((moving_y == y1 or moving_y == y1 + 2
                       or moving_y == y1 + 4)
                      and moving_x - x1 > 3):
                    if self.check_42_collisiones(moving_x, moving_y):
                        print("The number 42 cannot be printed cause of "
                              "collision")
                        return (1)
                    self.get_cell(moving_x, moving_y).cell_42()
                elif (moving_y == y1 + 1 and moving_x - x1 == 6):
                    if self.check_42_collisiones(moving_x, moving_y):
                        print("The number 42 cannot be printed cause of "
                              "collision")
                        return (1)
                    self.get_cell(moving_x, moving_y).cell_42()
                elif (moving_y == y1 + 3 and moving_x - x1 == 4):
                    if self.check_42_collisiones(moving_x, moving_y):
                        print("The number 42 cannot be printed cause of "
                              "collision")
                        return (1)
                    self.get_cell(moving_x, moving_y).cell_42()
                moving_x += 1
            moving_y += 1
        return (0)

    @lru_cache
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

    def print_map(self):
        print("Map:")
        for i in range(self.height):
            for j in range(self.width):
                print(self.maze_map[i][j], end="")
            print("")
        print()

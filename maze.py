class Cell:
    def __init__(self):
        self.visited: bool = False
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

    def uncover_dir(self, visiting_cell: "Cell", dir: int) -> None:
        visiting_cell.cover_all()
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

    def print_map(self):
        print("Map:")
        for i in range(self.height):
            for j in range(self.width):
                print(self.maze_map[i][j], end="")
            print("")
        print()

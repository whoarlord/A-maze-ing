class Cell:
    def __init__(self):
        self.visited: bool = False
        self.N = 0
        self.S = 0
        self.E = 0
        self.W = 0


class Maze:

    def __init__(
            self, width: int, height: int, entry: tuple[int, int],
            exit: tuple[int, int], perfect: bool):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
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

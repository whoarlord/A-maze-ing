from maze import Maze, Cell
from random import randint


class Prim:
    def create_map(self, maze: Maze) -> None:
        stack: list[tuple[int, int]] = [maze.entry]
        x, y = stack[-1]
        maze.maze_map[y][x].cover_all()
        while (len(stack) > 0):
            x, y = stack[-1]
            actual_cell: Cell = maze.get_cell(x, y)
            directions: list[int] = maze.not_visited_neighbours(x, y)
            if len(directions) == 0:
                stack.pop()
                continue
            rand_dir = randint(0, len(directions) - 1)
            temp_x, temp_y = maze.get_coord_by_dir(x, y, directions[rand_dir])
            temp_cell = maze.get_cell(temp_x, temp_y)
            actual_cell.uncover_dir(temp_cell, directions[rand_dir])

            stack.append((temp_x, temp_y))
        if not maze.perfect:
            self.create_multiple_routes(maze, min(maze.width, maze.height))

    def check_neighbours_for_routes(
            self, maze: Maze, threshold: int, x: int, y: int):
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

    def create_multiple_routes(self, maze: Maze, threshold: int = 10) -> None:
        for y in range(maze.height):
            for x in range(maze.width):
                self.check_neighbours_for_routes(maze, threshold, x, y)


if __name__ == "__main__":
    maze = Maze(20, 15, tuple([0, 0]), tuple([19, 14]), True)
    prim = Prim()
    prim.create_map(maze)
    maze.print_map()

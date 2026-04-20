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
            # maze.print_map()


if __name__ == "__main__":
    maze = Maze(20, 15, tuple([0, 0]), tuple([19, 14]), True)
    prim = Prim()
    prim.create_map(maze)
    maze.print_map()

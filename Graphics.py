from mlx import Mlx
from math import sqrt
from maze import Maze, Cell


class Graphics:
    def __init__(self):
        self.m: Mlx = Mlx()
        self.mlx_ptr = self.m.mlx_init()
        self.win_ptr = self.m.mlx_new_window(self.mlx_ptr, 640, 360, "Maze")
        self.m.mlx_hook(self.win_ptr, 33, 0, self.close_hook, self)

    @staticmethod
    def close_hook(self: "Graphics") -> int:
        self.m.mlx_loop_exit(self.mlx_ptr)
        return (1)

    def loop(self) -> None:
        self.m.mlx_loop(self.mlx_ptr)
        self.m.mlx_destroy_window(self.mlx_ptr, self.win_ptr)

    def draw_pixel_multiplied(self, pixel_x: int, pixel_y: int,
                              color: int, multiplier: int = 3):
        for i in range(multiplier):
            for j in range(multiplier):
                self.m.mlx_pixel_put(self.mlx_ptr, self.win_ptr,
                                     pixel_x + i, pixel_y + j, color)

    def draw_line(
            self, x1: int, y1: int, x2: int, y2: int, color: int = 0xFFFFFFFF):
        delta_x: int = x2 - x1
        delta_y: int = y2 - y1
        delta_pixels: int = sqrt((delta_x * delta_x) + (delta_y * delta_y))

        delta_x = int(delta_x / delta_pixels)
        delta_y = int(delta_y / delta_pixels)
        pixel_x = x1
        pixel_y = y1
        delta_pixels = round(delta_pixels)

        while (delta_pixels):
            self.m.mlx_pixel_put(self.mlx_ptr, self.win_ptr,
                                 pixel_x, pixel_y, color)
            pixel_x += delta_x
            pixel_y += delta_y
            delta_pixels -= 1
        self.m.mlx_sync(self.mlx_ptr, 2, self.win_ptr)

    def create_cell(self, x1: int, y1: int, x2: int, y2: int, walls: int):
        """This function is gonna create a cell with the specified walls

        Args:
        - x1 (int): coordinate x for the top-left of the square
        - y1 (int): coordinate y for the top-left of the square
        - x2 (int): coordinate x for the bottom-right of the square
        - y2 (int): coordinate y for the bottom-right of the square
        - walls (int): an integer defining the walls at the cell

        This function is gonna take the coordinates and generate walls by the
        integer the cell class has: for example: walls = 3 it gonna have the
        north and east walls up
        """
        if (walls >= 8):
            walls -= 8
            self.draw_line(x1, y1, x1, y2)
        if (walls >= 4):
            walls -= 4
            self.draw_line(x1, y2, x2, y2)
        if (walls >= 2):
            walls -= 2
            self.draw_line(x2, y1, x2, y2)
        if (walls == 1):
            self.draw_line(x1, y1, x2, y1)
        pass

    def display_maze(self, maze: Maze):
        initial_x: int = 10
        actual_y: int = 10
        increment: int = 20

        for i in range(maze.height):
            actual_x: int = initial_x
            for j in range(maze.width):
                if maze.entry == (j, i):
                    self.draw_pixel_multiplied(actual_x + 2,
                                               actual_y + 2,
                                               0xFF00FF00, increment - 3)
                elif maze.exit == (j, i):
                    self.draw_pixel_multiplied(actual_x + 2,
                                               actual_y + 2,
                                               0xFFFF0000, increment - 3)
                cell: Cell = maze.maze_map[i][j]
                self.create_cell(
                    actual_x, actual_y, actual_x + increment, actual_y +
                    increment, cell.calculate_walls())
                actual_x += increment
            actual_y += increment

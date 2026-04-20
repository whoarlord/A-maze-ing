from mlx import Mlx
from math import sqrt
from maze import Maze, Cell
from screeninfo import get_monitors, Monitor
from collections import deque


class Graphics:
    """Class for making the graphic representation of the """

    def __init__(self):
        self.m: Mlx = Mlx()
        self.mlx_ptr = self.m.mlx_init()
        monitor: Monitor = get_monitors()[0]
        self.win_height: int = int(monitor.height * 2 / 3)
        self.win_width: int = int(monitor.width * 2 / 3)
        self.win_ptr = self.m.mlx_new_window(
            self.mlx_ptr, self.win_width, self.win_height, "Maze")
        self.wall_multiplier: int = 5
        self.m.mlx_hook(self.win_ptr, 33, 0, self.close_hook, self)
        self.colors: deque[dict[int]] = deque([
            {
                "entry": 0xFFFF6B6B,
                "exit": 0xFF4ECDC4,
                "walls": 0xFFFFD93D,
                "42": 0xFF1A535C
            },
            {
                "entry": 0xFFFFADAD,
                "exit": 0xFFCAFFBF,
                "walls": 0xFFA0C4FF,
                "42": 0xFFFFD6A5
            },
            {
                "entry": 0xFF2E3440,
                "exit": 0xFF88C0D0,
                "walls": 0xFFA3BE8C,
                "42": 0xFFEBCB8B
            },
            {
                "entry": 0xFFE63946,
                "exit": 0xFF457B9D,
                "walls": 0xFF2A9D8F,
                "42": 0xFFF4A261
            }])

    @staticmethod
    def close_hook(self: "Graphics") -> int:
        self.m.mlx_loop_exit(self.mlx_ptr)
        return (1)

    def rotate_colors(self) -> None:
        self.colors.rotate()

    def loop(self) -> None:
        self.m.mlx_loop(self.mlx_ptr)
        self.m.mlx_destroy_window(self.mlx_ptr, self.win_ptr)

    def draw_box(self, pixel_x: int, pixel_y: int,
                 color: int, multiplier_x: int, multiplier_y):
        for i in range(multiplier_y):
            for j in range(multiplier_x):
                self.m.mlx_pixel_put(self.mlx_ptr, self.win_ptr,
                                     pixel_x + j, pixel_y + i, color)

    def draw_pixel_multiplied(self, pixel_x: int, pixel_y: int,
                              color: int):
        for i in range(self.wall_multiplier):
            for j in range(self.wall_multiplier):
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
            self.draw_pixel_multiplied(pixel_x, pixel_y, color)
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
            self.draw_line(x1, y1, x1, y2, color=self.colors[0]["walls"])
        if (walls >= 4):
            walls -= 4
            self.draw_line(x1, y2, x2, y2, color=self.colors[0]["walls"])
        if (walls >= 2):
            walls -= 2
            self.draw_line(x2, y1, x2, y2, color=self.colors[0]["walls"])
        if (walls == 1):
            self.draw_line(x1, y1, x2, y1, color=self.colors[0]["walls"])
        pass

    def display_menu(self, maze: Maze):
        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")

        choice: int = 0
        while (choice < 1 or choice > 4):
            try:
                choice = int(input("Choice? (1-4) "))
                if (choice < 1 or choice > 4):
                    print("The choice should be between 1 and 4")
            except ValueError:
                print("The input should be a number")
                choice = 0
        if choice == 1:
            print("Functionality under construction")
            self.display_menu(maze)
        elif choice == 2:
            print("Functionality under construction")
            self.display_menu(maze)
        elif choice == 3:
            self.rotate_colors()
            self.display_maze(maze)
            self.display_menu(maze)

    def display_maze(self, maze: Maze):
        initial_x: int = 10
        actual_y: int = 10
        increment_x: int = int((self.win_width - 20) / maze.width)
        increment_y: int = int((self.win_height - 20) / maze.height)

        for i in range(maze.height):
            actual_x: int = initial_x
            for j in range(maze.width):
                if maze.entry == (j, i):
                    self.draw_box(actual_x, actual_y, self.colors[0]["entry"],
                                  increment_x, increment_y)
                elif maze.exit == (j, i):
                    self.draw_box(actual_x, actual_y, self.colors[0]["exit"],
                                  increment_x, increment_y)
                cell: Cell = maze.maze_map[i][j]
                if cell.block_42:
                    self.draw_box(
                        actual_x, actual_y, self.colors[0]["42"],
                        increment_x, increment_y)
                self.create_cell(
                    actual_x, actual_y, actual_x + increment_x, actual_y +
                    increment_y, cell.calculate_walls())
                actual_x += increment_x
            actual_y += increment_y

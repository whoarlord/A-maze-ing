from mlx import Mlx
from math import sqrt
from maze import Maze, Cell
from screeninfo import get_monitors, Monitor
from collections import deque
from Algorithms import Algorithms
from maze_solver import solve_maze
from typing import Any


class Graphics:
    """Class for making the graphic representation of the maze

    Atributtes:
    - m (Mlx): the main class of the minilibx
    - mlx_ptr: the pointer to the mlx
    - win_height (int): the height of the window base on the monitor
    - win_width (int): the width of the window base on the monitor
    - win_ptr: A pointer to the window we are gonna display
    - maze_img_ptr: A pointer to the image containing the maze
    - maze_buffer: The buffer of the maze image
    - route_img_ptr: A pointer to the image containing the route
    - route_buffer: The buffer of the route image
    - wall_multiplier (int): the number for making the walls thicker
    - colors (deque[dict[int]]): the set of colors for the maze
    """

    colors: deque[dict[int]] = deque([
        {
            "entry": 0xFFFF6B6B,
            "exit": 0xFF4ECDC4,
            "walls": 0xFFFFD93D,
            "42": 0xFF1A535C,
            "route": 0xFFFFFFFF
        },
        {
            "entry": 0xFFFFADAD,
            "exit": 0xFFCAFFBF,
            "walls": 0xFFA0C4FF,
            "42": 0xFFFFD6A5,
            "route": 0xFF6A4C93
        },
        {
            "entry": 0xFF2E3440,
            "exit": 0xFF88C0D0,
            "walls": 0xFFA3BE8C,
            "42": 0xFFEBCB8B,
            "route": 0xFFFF00FF
        },
        {
            "entry": 0xFFE63946,
            "exit": 0xFF457B9D,
            "walls": 0xFF2A9D8F,
            "42": 0xFFF4A261,
            "route": 0xFF00FFFF
        }])

    def __init__(self, maze: Maze):
        self.m: Mlx = Mlx()
        self.mlx_ptr = self.m.mlx_init()
        monitor: Monitor = get_monitors()[0]
        self.win_height: int = int(monitor.height * 2 / 3)
        self.win_width: int = int(monitor.width * 2 / 3)
        self.maze_img_ptr = self.m.mlx_new_image(
            self.mlx_ptr, self.win_width, self.win_height)
        self.maze_buffer = self.m.mlx_get_data_addr(self.maze_img_ptr)
        self.route_img_ptr = self.m.mlx_new_image(
            self.mlx_ptr, self.win_width, self.win_height)
        self.route_buffer = self.m.mlx_get_data_addr(self.route_img_ptr)
        self.route_visible: bool = False
        self.wall_multiplier: int = 5
        self.generate_black_window()
        self.display_maze(maze)
        self.display_route(maze)
        self.win_ptr = self.m.mlx_new_window(
            self.mlx_ptr, self.win_width + 1, self.win_height + 1, "Maze")
        self.m.mlx_put_image_to_window(
            self.mlx_ptr, self.win_ptr, self.maze_img_ptr, 0, 0)
        self.m.mlx_sync(self.mlx_ptr, 2, self.win_ptr)
        self.m.mlx_hook(self.win_ptr, 2, 1, self.key_hook, self)
        self.m.mlx_hook(self.win_ptr, 33, 0, self.close_hook, self)
        self.loop()

    def generate_black_window(self) -> None:
        """This function generate a completely black window"""
        for i in range(self.win_height):
            for j in range(self.win_width):
                self.put_pixels_at_img(j, i, 0x00000000, self.maze_buffer)

    def generate_invisible_window(self) -> None:
        """This function generate a completely invisible window"""
        for i in range(self.win_height):
            for j in range(self.win_width):
                self.put_pixels_at_img(j, i, 0x00000000, self.route_buffer)

    def close_hook(self, param: Any) -> int:
        """Hook for exiting the loop"""
        self.m.mlx_loop_exit(self.mlx_ptr)
        return (1)

    def key_hook(self, keycode: int, param: Any) -> int:
        """Hook for continuing the program"""
        self.m.mlx_loop_exit(self.mlx_ptr)
        return (1)

    def loop(self) -> None:
        """The main loop of the window"""
        self.m.mlx_loop(self.mlx_ptr)

    def rotate_colors(self) -> None:
        """Function for rotating colors of the maze"""
        self.colors.rotate()

    def put_pixels_at_img(
            self, pixel_x: int, pixel_y: int, color: int,
            buffer: tuple[memoryview,
                          int, int, int]) -> None:
        """Function for putting specific pixel at the image

        Args:
        - pixel_x (int): coordinates on x for the pixel
        - pixel_y (int): coordinates on y for the pixel
        - color (int): the color is gonna be used at the pixel

        This functions checks the if image use little or big endian
        and writes the colors at the specified pixel based on the image
        line length
        """
        endian: int = buffer[3]
        pixel: int = (pixel_y * buffer[2]) + (pixel_x * 4)
        buffer_pixels = buffer[0]
        if endian == 1:
            buffer_pixels[pixel] = (color >> 24)
            buffer_pixels[pixel + 1] = (color >> 16) & 0xFF
            buffer_pixels[pixel + 2] = (color >> 8) & 0xFF
            buffer_pixels[pixel + 3] = (color) & 0xFF
        else:
            buffer_pixels[pixel] = (color) & 0xFF
            buffer_pixels[pixel + 1] = (color >> 8) & 0xFF
            buffer_pixels[pixel + 2] = (color >> 16) & 0xFF
            buffer_pixels[pixel + 3] = (color >> 24)

    def draw_box(
            self, pixel_x: int, pixel_y: int, color: int, multiplier_x: int,
            multiplier_y, buffer: tuple[memoryview, int, int, int]) -> None:
        """A function for drawing a box"""
        for i in range(multiplier_y):
            for j in range(multiplier_x):
                self.put_pixels_at_img(pixel_x + j, pixel_y + i, color, buffer)

    def draw_pixel_multiplied(
            self, pixel_x: int, pixel_y: int, color: int,
            buffer: tuple[memoryview, int, int, int]) -> None:
        """A function for drawing thicker wall"""
        for i in range(self.wall_multiplier):
            for j in range(self.wall_multiplier):
                self.put_pixels_at_img(pixel_x + j, pixel_y + i, color, buffer)

    def draw_line(
            self, x1: int, y1: int, x2: int, y2: int,
            buffer: tuple[memoryview, int, int, int],
            color: int = 0xFFFFFFFF) -> None:
        """Main function for drawing lines

        Args:
        - x1 (int): the x coordinates where the line starts
        - y1 (int): the y coordinates where the line starts
        - x2 (int): the x coordinates where the line ends
        - y2 (int): the y coordinates where the line ends
        - color (int): the color of the line

        This function calculates the delta_pixels for the line, so he can
        increment the pixel_x and the pixel_y to make it
        """
        delta_x: int = x2 - x1
        delta_y: int = y2 - y1
        delta_pixels: int = sqrt((delta_x * delta_x) + (delta_y * delta_y))

        delta_x = int(delta_x / delta_pixels)
        delta_y = int(delta_y / delta_pixels)
        pixel_x = x1
        pixel_y = y1
        delta_pixels = round(delta_pixels)

        while (delta_pixels):
            self.draw_pixel_multiplied(pixel_x, pixel_y, color, buffer)
            pixel_x += delta_x
            pixel_y += delta_y
            delta_pixels -= 1

    def create_cell(
            self, x1: int, y1: int, x2: int, y2: int, walls: int,
            buffer: tuple[memoryview, int, int, int]) -> None:
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
            self.draw_line(x1, y1, x1, y2, buffer,
                           color=self.colors[0]["walls"])
        if (walls >= 4):
            walls -= 4
            self.draw_line(x1, y2, x2, y2, buffer,
                           color=self.colors[0]["walls"])
        if (walls >= 2):
            walls -= 2
            self.draw_line(x2, y1, x2, y2, buffer,
                           color=self.colors[0]["walls"])
        if (walls == 1):
            self.draw_line(x1, y1, x2, y1, buffer,
                           color=self.colors[0]["walls"])

    def display_menu(self, maze: Maze, algorithms: Algorithms) -> None:
        """Function for displaying the menu

        Args:
        - maze (Maze): the maze to be displayed or changed
        - algorithms (Algorithms): the object for executing the algorithms
        to create the maze

        This functiions displays a menu for the user, so he can
        make 4 different choices, based on the input number between
        1 and 4:
        - 1. Re-generate a new maze
        - 2. Show/Hide path from entry to exit
        - 3. Rotate maze colors
        - 4. Quit
        """
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
            maze.re_generate()
            algorithms.create_map(maze)
            solve_maze(maze)
            self.generate_black_window()
            self.generate_invisible_window()
            self.display_maze(maze)
            self.display_route(maze)
            self.route_visible = False
            self.m.mlx_clear_window(self.mlx_ptr, self.win_ptr)
            self.m.mlx_put_image_to_window(
                self.mlx_ptr, self.win_ptr, self.maze_img_ptr, 0, 0)
            self.m.mlx_sync(self.mlx_ptr, 2, self.win_ptr)
            self.loop()
            self.display_menu(maze, algorithms)
        elif choice == 2:
            if self.route_visible:
                self.m.mlx_clear_window(self.mlx_ptr, self.win_ptr)
                self.m.mlx_put_image_to_window(
                    self.mlx_ptr, self.win_ptr, self.maze_img_ptr, 0, 0)
                self.route_visible = False
            else:
                self.m.mlx_put_image_to_window(
                    self.mlx_ptr, self.win_ptr, self.route_img_ptr, 0, 0)
                self.route_visible = True
            self.loop()
            self.display_menu(maze, algorithms)
        elif choice == 3:
            self.rotate_colors()
            self.display_maze(maze)
            self.m.mlx_put_image_to_window(
                self.mlx_ptr, self.win_ptr, self.maze_img_ptr, 0, 0)
            self.m.mlx_sync(self.mlx_ptr, 2, self.win_ptr)
            self.display_menu(maze, algorithms)

    def display_maze(self, maze: Maze):
        """This is the main function for displaying the maze

        Args:
        - maze (Maze): the maze to be displayed

        This function calculates the increment of x and y, so it covers
        all the window. Then it draws the 4 different elements that we have:
        - entry box: for displaying where the maze start
        - exit box: for displaying where the maze ends
        - block_42 boxes: for displaying the unique 42 cells
        - cell boxes: for displaying the walls of each cell
        """
        initial_x: int = 0
        actual_y: int = 0
        increment_x: int = int(
            ((self.win_width - self.wall_multiplier) / maze.width))
        increment_y: int = int(
            (self.win_height - self.wall_multiplier) / maze.height)

        for i in range(maze.height):
            actual_x: int = initial_x
            for j in range(maze.width):
                if maze.entry == (j, i):
                    self.draw_box(actual_x, actual_y, self.colors[0]["entry"],
                                  increment_x, increment_y, self.maze_buffer)
                elif maze.exit == (j, i):
                    self.draw_box(actual_x, actual_y, self.colors[0]["exit"],
                                  increment_x, increment_y, self.maze_buffer)
                cell: Cell = maze.maze_map[i][j]
                if cell.block_42:
                    self.draw_box(
                        actual_x, actual_y, self.colors[0]["42"],
                        increment_x, increment_y, self.maze_buffer)
                self.create_cell(
                    actual_x, actual_y, actual_x + increment_x, actual_y +
                    increment_y, cell.calculate_walls(), self.maze_buffer)
                actual_x += increment_x
            actual_y += increment_y

    def display_route(self, maze: Maze):
        increment_x: int = int(
            ((self.win_width - self.wall_multiplier) / maze.width))
        increment_y: int = int(
            (self.win_height - self.wall_multiplier) / maze.height)
        actual_x: int = int(maze.entry[0] * increment_x + increment_x / 2)
        actual_y: int = int(maze.entry[1] * increment_y + increment_y / 2)
        print(f"initial_x: {actual_x}, initial_y: {actual_y}")
        print(maze.route)
        for i in range(len(maze.route)):
            direction = maze.route[i]
            if direction == "N":
                self.draw_line(actual_x, actual_y, actual_x,
                               actual_y - increment_y, self.route_buffer,
                               self.colors[0]["route"])
                actual_y -= increment_y
            elif direction == "S":
                self.draw_line(actual_x, actual_y, actual_x,
                               actual_y + increment_y, self.route_buffer,
                               self.colors[0]["route"])
                actual_y += increment_y
            elif direction == "W":
                self.draw_line(actual_x, actual_y, actual_x - increment_x,
                               actual_y, self.route_buffer,
                               self.colors[0]["route"])
                actual_x -= increment_x
            elif direction == "E":
                self.draw_line(actual_x, actual_y, actual_x + increment_x,
                               actual_y, self.route_buffer,
                               self.colors[0]["route"])
                actual_x += increment_x

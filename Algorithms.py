from maze import Maze, Cell
from random import randint, shuffle, seed


class Algorithms:
    def create_map(self, maze: Maze) -> None:
        """This function creates the maze based on the config file

        This function creates a seed or uses the seed from the maze if it is
        greater than 0, and then create a maze based on that seed and the
        algorithm specified at the maze.algorithm

        Args:
        - maze (Maze): the object with the specified configuration of the maze

        """
        if maze.seed <= 0:
            self.create_seed(maze)
        else:
            seed(maze.seed)
        if maze.algorithm == "kruskal":
            self.create_map_kruskal(maze)
        elif maze.algorithm == "prim":
            self.create_map_prim(maze)

    def create_seed(self, maze: Maze) -> None:
        """Function for creating a random seed for the maze"""
        number: int = 0
        for i in range(maze.height):
            for j in range(maze.width):
                number = (number + randint(0, 15)) * 16
        maze.seed = number
        seed(number)

    def create_map_kruskal(self, maze: Maze) -> None:
        print("Executing kruskal algorithm\n")
        cell_list: list[tuple[int, int]] = []
        cell_group: list[int] = []
        group_id: int = 0
        for y in range(maze.height):
            for x in range(maze.width):
                cell: Cell = maze.get_cell(x, y)
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
                    maze, x, y, i, cell_list, cell_group)
                if len(directions) == 0:
                    continue
                rand_dir = randint(0, len(directions) - 1)
                temp_x, temp_y = maze.get_coord_by_dir(
                    x, y, directions[rand_dir])
                actual_cell = maze.get_cell(x, y)
                temp_cell = maze.get_cell(temp_x, temp_y)
                actual_cell.uncover_dir_flex(
                    temp_cell, directions[rand_dir])
                self.update_group(temp_x, temp_y, cell_group,
                                  cell_list, cell_group[i])
        if not maze.perfect:
            self.create_multiple_routes(maze, min(maze.width, maze.height))

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
            self, maze: Maze, x: int, y: int, i: int, cell_list: list[int],
            cell_group: list[int]) -> list[int]:
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

    def create_map_prim(self, maze: Maze) -> None:
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
        """Checks the distance between a cell and their adyacent

        This function receive a position of a cell a maze where the cell is
        and a threshold and checks if a specific cell is further from an
        adyacent cell than the threshold and destroys the wall between them
        to make an non perfect maze
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

    def create_multiple_routes(self, maze: Maze, threshold: int = 10) -> None:
        """This function destroys walls between cells based on the threshold"""
        for y in range(maze.height):
            for x in range(maze.width):
                self.check_neighbours_for_routes(maze, threshold, x, y)

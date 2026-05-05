class Player:

    def __init__(self, position: tuple[int, int]) -> None:
        x, y = position
        self.x = x
        self.y = y
        self.movements: list[str] = []

    def can_move_to(self, direction: str, maze: Maze) -> bool:

        player_cell = maze.get_cell(self.x, self.y)
        match direction:
            case "E":
                if not player_cell.has_wall("E"):
                    return True
                else:
                    return False

            case "W":
                if not player_cell.has_wall("W"):
                    return True
                else:
                    return False

            case "N":
                if not player_cell.has_wall("N"):
                    return True
                else:
                    return False

            case "S":
                if not player_cell.has_wall("S"):
                    return True
                else:
                    return False

    def get_direction(self, coords: tuple[int, int]) -> str:

        x, y = coords
        if self.x < x:
            return "E"
        elif self.x > x:
            return "W"
        elif self.y < y:
            return "S"
        elif self.y > y:
            return "N"

    def move_to(self, direction: str) -> None:

        match direction:
            case "E":
                self.x += 1
                self.movements.append("E")

            case "W":
                self.x -= 1
                self.movements.append("W")

            case "N":
                self.y -= 1
                self.movements.append("N")

            case "S":
                self.y += 1
                self.movements.append("S")

    def get_last_movement(self) -> str:

        if len(self.movements) > 0:
            return self.movements[len(self.movements) - 1]
        else:
            return "No movements yet"

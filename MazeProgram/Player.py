class Player:

    def __init__(self, position: tuple[int, int]) -> None:
        x, y = position
        self.x = x
        self.y = y
        self.movements: list[str] = []

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
        return "N"

    def move_to(self, direction: str) -> None:

        match direction:
            case "E":
                self.x += 1
                if (self.movements and self.movements[len(self.movements) - 1]
                        == "W"):
                    self.movements.pop()
                else:
                    self.movements.append("E")

            case "W":
                self.x -= 1
                if (self.movements and self.movements[len(self.movements) - 1]
                        == "E"):
                    self.movements.pop()
                else:
                    self.movements.append("W")

            case "N":
                self.y -= 1
                if (self.movements and self.movements[len(self.movements) - 1]
                        == "S"):
                    self.movements.pop()
                else:
                    self.movements.append("N")

            case "S":
                self.y += 1
                if (self.movements and self.movements[len(self.movements) - 1]
                        == "N"):
                    self.movements.pop()
                else:
                    self.movements.append("S")

    def get_last_movement(self) -> str:

        if len(self.movements) > 0:
            return self.movements[len(self.movements) - 1]
        return "No movements yet"

    def last_coordenate(self) -> tuple[int, int]:

        match self.get_last_movement():
            case "N":
                return self.x, (self.y + 1)
            case "S":
                return self.x, (self.y - 1)
            case "E":
                return (self.x - 1), self.y
            case "W":
                return (self.x + 1), self.y
        return (self.x + 1), self.y

    def print_path(self) -> None:

        for elem in self.movements:
            print(f"{elem}", end="")

    def path_tostring(self) -> str:

        string = ""
        for elem in self.movements:
            string += elem

        return string

    def backtracking(self) -> None:

        direction = self.movements.pop()
        match direction:
            case "N":
                self.y += 1
            case "S":
                self.y -= 1
            case "E":
                self.x -= 1
            case "W":
                self.x += 1

class Player:
    """Class representing the player which is gonna move to make the route

    Attributes:
        x (int): the x coordinate of the player
        y (int): the y coordinate of the player
        movements (list[str]): the list of movements done by the player
    """

    def __init__(self, position: tuple[int, int]) -> None:
        x, y = position
        self.x: int = x
        self.y: int = y
        self.movements: list[str] = []

    def get_direction(self, coords: tuple[int, int]) -> str:
        """function for getting the movements its doing the player"""
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
        """Function for moving the player

        This function checks what movement have be done, its add it to
        the movements list, but if the last movement was from the
        opposite direction it just pop that movement

        Args:
            direction (int): the direction the player is gonna move to
        """

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
        """Returns the last movement done by the player if 1 was done"""
        if len(self.movements) > 0:
            return self.movements[len(self.movements) - 1]
        return "No movements yet"

    def last_coordenate(self) -> tuple[int, int]:
        """Returns the last coordinate were the player was"""
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

    def path_tostring(self) -> str:
        """returns the path in a single string"""
        string = ""
        for elem in self.movements:
            string += elem

        return string

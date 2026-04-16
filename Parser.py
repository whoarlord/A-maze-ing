#!/usr/bin/env python3

from errors import ParseError, PerfectError, InvalidValueError
from typing import Any


class Parser:

    def parse_line(self, line: str, dictionary: dict[str: Any]) -> None:

        if "=" in line:

            if len(line.split("=")) != 2:
                print(f"Syntax error on line {line}")
                raise Exception

            parameter, value = line.split("=")

            match parameter:
                case ("WIDTH" | "HEIGHT"):

                    try:
                        number = int(value)
                        if number <= 0:
                            raise InvalidValueError(line, number)
                        dictionary.update({parameter: number})

                    except ValueError as e:
                        print(f"{e}")

                case ("ENTRY" | "EXIT"):

                    x, y = value.split(",")

                    try:
                        x_int = int(x)
                        y_int = int(y)

                        if x_int < 0 or x_int > dictionary.get("WIDTH"):
                            raise InvalidValueError(line, x_int)
                        elif y_int < 0 or y_int > dictionary.get("HEIGHT"):
                            raise InvalidValueError(line, y_int)

                        dictionary.update({parameter: (x_int, y_int)})

                    except ValueError as e:
                        print(f"{e}")

                case "OUTPUT_FILE":

                    dictionary.update({parameter: value})

                case "PERFECT":

                    if value == "True":
                        dictionary.update({parameter: True})
                    elif value == "False":
                        # Si no me llega true y me llega cualquier otra cosa lo mando default a false?
                        dictionary.update({parameter: False})
                    else:
                        raise PerfectError(line)

                case _:
                    print(f"Unknown value on line: {line}")
                    raise Exception
        else:
            raise ParseError(line)

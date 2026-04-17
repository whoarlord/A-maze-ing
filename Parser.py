#!/usr/bin/env python3

from errors import ParseError, PerfectError, InvalidValueError
from typing import Any


class Parser:

    def parse_line(self, line: str, dictionary: dict[str: Any]) -> None:

        if "=" in line:

            parameter, value = line.split("=")

            if value == "":
                raise Exception(
                    f"Syntax error on line '{line}'. Please follow the next "
                    "format: <NAME>=<value>")

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
                            raise InvalidValueError(
                                line, x_int, dictionary.get("WIDTH"), "WIDTH")
                        elif y_int < 0 or y_int > dictionary.get("HEIGHT"):
                            raise InvalidValueError(
                                line, y_int, dictionary.get("HEIGHT"),
                                "HEIGHT")

                        dictionary.update({parameter: (x_int, y_int)})

                    except ValueError as e:
                        raise Exception(
                            f"Error on line: '{line}'. {e}. Please follow the "
                            "next format for the ENTRY and EXIT: <NAME>=x,y")
                case "OUTPUT_FILE":

                    dictionary.update({parameter: value})

                case "PERFECT":

                    if value == "True":
                        dictionary.update({parameter: True})
                    elif value == "False":
                        dictionary.update({parameter: False})
                    else:
                        raise PerfectError(line)

                case _:
                    raise Exception(f"Unknown value on line: {line}")
        else:
            raise ParseError(line)

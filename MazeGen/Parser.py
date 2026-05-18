#!/usr/bin/env python3

from .errors import (
    ParseError, PerfectError, InvalidValueError, DisplayModeError,
    AlgorithmError, SeedError, OrderError, MandatoryParameterError)
from typing import TypedDict
import sys


class RawConfig(TypedDict, total=False):
    """TypedDict for the Raw config with null posible

    Attributes:
        WIDTH (int)
        HEIGHT (int)
        ENTRY (tuple[int, int])
        EXIT (tuple[int, int])
        OUTPUT_FILE (str)
        PERFECT (bool)
        ANIMATION (bool)
        ALGORITHM (str)
        SEED (int)
    """

    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool
    ANIMATION: bool
    ALGORITHM: str
    SEED: int


class Config(TypedDict):
    """TypedDict for the Raw config with null posible

    Attributes:
        width (int)
        height (int)
        entry (tuple[int, int])
        exit (tuple[int, int])
        output_file (str)
        perfect (bool)
        animation (bool)
        algorithm (str)
        seed (int)
    """
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    animation: bool
    algorithm: str
    seed: int


class Parser:
    """Class representing the object for making the parsing of the file"""

    def parse_line(self, line: str, dictionary: RawConfig) -> None:
        """Function for parsing the entry

        This function receive a line and checks if the format and values of
        the line are correct

        Args:
            line (str): the line which is being readed from the config file
            dictionary (RawConfig): the dictionary representing the parameters
                of the maze
        """

        if len(line) == 0:
            raise ParseError(line)
        elif line[0] == '#':
            return
        elif "=" in line:
            parameter, value = line.split("=")
            parameter = parameter.upper()
            if value == "":
                raise Exception(
                    f"Syntax error on line '{line}'. Please follow the next "
                    "format: <NAME>=<value>")

            match parameter:
                case ("WIDTH" | "HEIGHT"):

                    try:
                        number = int(value)
                        if number <= 0:
                            raise InvalidValueError(
                                line, number, 0, parameter)

                        if parameter == "WIDTH":
                            dictionary.update({parameter: number})
                        else:
                            dictionary.update({parameter: number})

                    except ValueError as e:
                        raise Exception(f"Error in line: {line}, {e}")

                case ("ENTRY" | "EXIT"):

                    x, y = value.split(",")

                    try:
                        x_int = int(x)
                        y_int = int(y)

                        if x_int < 0 or x_int >= dictionary.get("WIDTH", 0):
                            raise InvalidValueError(
                                line, x_int, dictionary.get("WIDTH", 0),
                                "WIDTH")
                        elif y_int < 0 or y_int >= dictionary.get("HEIGHT", 0):
                            raise InvalidValueError(
                                line, y_int, dictionary.get("HEIGHT", 0),
                                "HEIGHT")

                        if parameter == "ENTRY":
                            dictionary.update({parameter: (x_int, y_int)})
                            if dictionary.get("EXIT") is not None:
                                if dictionary.get("EXIT") == dictionary.get(
                                        "ENTRY"):
                                    raise Exception(
                                        f"error in line {line}, it collides "
                                        "with the EXIT")
                        else:
                            dictionary.update({parameter: (x_int, y_int)})
                            if dictionary.get("ENTRY") is not None:
                                if dictionary.get("ENTRY") == dictionary.get(
                                        "EXIT"):
                                    raise Exception(
                                        f"error in line {line}, it collides "
                                        "with the ENTRY")

                    except ValueError as e:
                        raise Exception(
                            f"Error on line: '{line}'. {e}. Please follow the "
                            "next format for the ENTRY and EXIT: <NAME>=x,y")
                case "OUTPUT_FILE":
                    extensions = value.split(".")
                    if extensions[-1] == "txt":
                        dictionary.update({parameter: value})
                    elif len(extensions) == 1:
                        raise Exception(
                            f"Error on line: '{line}'. The given output file "
                            "has to have the .txt extension.")
                    else:
                        raise Exception(
                            f"Error on line: '{line}'. The given output file "
                            "has to have the .txt extension, not the "
                            f".{extensions[-1]} extension.")

                case "SEED":
                    try:
                        if (dictionary.get("WIDTH") is None
                                or dictionary.get("WIDTH") is None):
                            raise OrderError(line)
                        limits: int = dictionary.get(
                            "WIDTH", 0) * dictionary.get("WIDTH", 0) * 10
                        if limits > 640:
                            sys.set_int_max_str_digits(limits)
                        seed = int(value)
                        if seed <= 0:
                            raise SeedError(line)
                        dictionary.update({parameter: seed})
                    except ValueError as e:
                        raise Exception(
                            f"Error on line: '{line}'. {e}. Please follow the "
                            "next format for the SEED: <NAME>=seed")

                case "PERFECT":

                    capitalized = value.capitalize()
                    if capitalized == "True" or capitalized == "1":
                        dictionary.update({parameter: True})
                    elif capitalized == "False" or capitalized == "0":
                        dictionary.update({parameter: False})
                    else:
                        raise PerfectError(line)

                case "DISPLAY_MODE":
                    if value.capitalize() == "Normal":
                        dictionary.update({"ANIMATION": False})
                    elif value.capitalize() == "Animated":
                        dictionary.update({"ANIMATION": True})
                    else:
                        raise DisplayModeError(line)
                case "ALGORITHM":
                    if value.lower() == "kruskal" or value.lower() == "prim":
                        dictionary.update({parameter: value.lower()})
                    else:
                        raise AlgorithmError(line)
                case _:
                    raise Exception(f"Unknown value on line: {line}")
        else:
            raise ParseError(line)

    def entry_checker(self, dictionary: RawConfig) -> None:
        """checks if any of the mandatory parameters is missing"""
        if dictionary.get("WIDTH") is None:
            raise MandatoryParameterError("WIDTH")
        elif dictionary.get("HEIGHT") is None:
            raise MandatoryParameterError("HEIGHT")
        elif dictionary.get("ENTRY") is None:
            raise MandatoryParameterError("ENTRY")
        elif dictionary.get("EXIT") is None:
            raise MandatoryParameterError("EXIT")
        elif dictionary.get("OUTPUT_FILE") is None:
            raise MandatoryParameterError("OUTPUT_FILE")
        elif dictionary.get("PERFECT") is None:
            raise MandatoryParameterError("PERFECT")

    def complete_dictionary(self, dictionary: RawConfig) -> Config:
        """This function completes the dictionary with the 3 optional values"""
        return {
            "width": dictionary.get("WIDTH", 0),
            "height": dictionary.get("HEIGHT", 0),
            "entry": dictionary.get("ENTRY", (0, 0)),
            "exit": dictionary.get("EXIT", (0, 0)),
            "output_file": dictionary.get("OUTPUT_FILE", ""),
            "perfect": dictionary.get("PERFECT", True),
            "animation": dictionary.get("ANIMATION", False),
            "algorithm": dictionary.get("ALGORITHM", "prim"),
            "seed": dictionary.get("SEED", 0)
        }

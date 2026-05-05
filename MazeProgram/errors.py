#!/usr/bin/env python3

class ParseError(Exception):
    """Exception for parsing errors

    Atributtes:
    - line (str): the specific line were the error is
    """

    def __init__(self, line: str) -> None:
        super().__init__(
            f"Error on line: '{line}'. Line should have the next format:"
            "<Attribute>=<Value>")


class DisplayModeError(Exception):
    """Exception for Display mode parameter errors

    Atributtes:
    - line (str): the specific line were the error is
    """

    def __init__(self, line: str) -> None:
        super().__init__(
            f"Error on line: '{line}'. Line should have the next format:"
            "DISPLAY_MODE=Normal or DISPLAY_MODE=Animated")


class PerfectError(Exception):
    """Exception for Perfect parameter errors

    Atributtes:
    - line (str): the specific line were the error is
    """

    def __init__(self, line: str) -> None:
        super().__init__(
            f"Error on line: '{line}'. Line should have the next format:"
            "PERFECT=True or PERFECT=False")


class AlgorithmError(Exception):
    """Exception for Algorithm parameter errors

    Atributtes:
    - line (str): the specific line were the error is
    """

    def __init__(self, line: str) -> None:
        super().__init__(
            f"Error on line: '{line}'. Line should have the next format:"
            "ALGORITHM=kruskal or ALGORITHM=prim")


class InvalidValueError(Exception):
    """Exception for Invalid Value errors

    Atributtes:
    - line (str): the specific line were the error is
    """

    def __init__(
            self, line: str, value: int, limit, limit_name: str) -> None:

        if value >= limit:
            message = f" The value: {value} can't be bigger or equal than the {
                limit_name}."
        elif value < 0:
            message = f" The value: {value} can't be smaller than 0."
        super().__init__(
            f"Error on line: '{line}'. The value {value}  is incorrect." +
            message)


class SeedError(Exception):
    """Exception for Seed parameter errors

    Atributtes:
    - line (str): the specific line were the error is
    """

    def __init__(self, line: str) -> None:
        super().__init__(
            f"Error on line: '{line}'. the value must be superior than 0")

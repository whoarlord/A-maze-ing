#!/usr/bin/env python3

class ParseError(Exception):

    def __init__(self, line: str) -> None:
        super().__init__(
            f"Error on line: '{line}'. Line should have the next format:"
            "<Attribute>=<Value>")


class PerfectError(Exception):

    def __init__(self, line: str) -> None:
        super().__init__(
            f"Error on line: '{line}'. Line should have the next format:"
            "PERFECT=True or PERFECT=False")


class InvalidValueError(Exception):

    def __init__(
            self, line: str, value: int, limit: int, limit_name: str) -> None:

        if value > limit:
            message = f" The value: {value} can't be bigger than the {
                limit_name}."
        elif value < 0:
            message = f" The value: {value} can't be smaller than 0."
        super().__init__(
            f"Error on line: '{line}'. The value {value}  is incorrect." +
            message)

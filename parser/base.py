"""
This module contains the abstract base classes for implementing parsers.

A parser is a class that can parse a given line of input and return a Login
object.

Classes:
    Parser (ABC): An abstract base class for implementing parsers. It has one
        abstract method: `parse`.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Login:
    """
    A dataclass that represents a login event.

    Attributes:
        user (str): The user who logged in.
        ip_addr (str): The IP address from which the user logged in.
    """
    user: str
    ip_addr: str


# pylint: disable=R0903
class Parser(ABC):
    """
    An abstract base class for implementing parsers.

    A parser is a class that can parse a given line of input and return a Login
    object.

    Methods:
        parse(self, line: str) -> Login | None: This method takes a line of input
            and returns a Login object if a login event is found, otherwise it
            returns None.
    """

    @abstractmethod
    def parse(self, line: str) -> Login | None:
        """
        Parse a given line of input and return a Login object.

        Args:
            line (str): The line of input to be parsed.

        Returns:
            Login: A Login object representing the parsed data from the input line.
        """

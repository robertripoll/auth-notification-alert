"""
This module contains the abstract base classes for implementing locators to
geolocate IP addresses.

A locator can take an IP address as input and return a Location object,
which contains the city and the country of the IP address.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Location:
    """
    Represents a location with a city and a country.

    Attributes:
        city (str): The name of the city.
        country (str): The name of the country.
    """
    city: str
    country: str


# pylint: disable=R0903
class Locator(ABC):
    """
    This is an abstract base class that defines the interface for a Locator.
    A Locator is a class that can take an IP address as input and return a Location object.

    Attributes:
        ABC: This class is an abstract base class.

    Methods:
        locate(ip_addr: str) -> Location: This method takes an IP address as a string and
        returns a Location object.
    """

    @abstractmethod
    def locate(self, ip_addr: str) -> Location:
        """
        This is an abstract method that takes an IP address as a string and returns a
        Location object.

        It is a part of the Locator class and must be implemented by any class that
        inherits from it.

        Parameters:
            ip_addr (str): The IP address to locate.

        Returns:
            Location: The location of the given IP address.
        """

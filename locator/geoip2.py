"""
This module contains the GeoIP locator class.

A GeoIP locator is a locator that uses the GeoIP2 database to get the
location information of an IP address.
"""

from geoip2 import database
from locator.base import Location, Locator


# pylint: disable=R0903
class GeoIP(Locator):
    """
    This class represents a GeoIP locator.

    A GeoIP locator is a locator that uses the GeoIP2 database to get the
    location information of an IP address.

    Attributes:
        database (geoip2.database.Reader): The GeoIP2 database reader.

    Methods:
        locate(ip_addr: str) -> Location: Locates the given IP address and returns
            a Location object containing the city and country.
    """

    def __init__(self, path_to_db: str):
        self.database = database.Reader(path_to_db)

    def locate(self, ip_addr: str) -> Location:
        response = self.database.city(ip_addr)

        city = response.city.names['en']
        country = response.country.names['en']

        return Location(city=city, country=country)

"""
This module contains the abstract base classes for implementing notifiers.

A notifier is a class that can send notifications to a user about a successful login
event.

Attributes:
    Notification (dataclass): A dataclass that represents a notification. It contains the
        user, IP address, and location information.

Classes:
    Notifier (ABC): An abstract base class for implementing notifiers. It has two
        abstract methods: `is_excluded` and `notify`.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from socket import gethostbyaddr, herror
from locator.base import Location


@dataclass
class Notification:
    """
    Represents a notification.

    Attributes:
        user (str): The username of the user.
        ip_addr (str): The IP address of the user.
        location (Location): The location of the user.
    """
    user: str
    ip_addr: str
    location: Location


class Notifier(ABC):
    """
    An abstract base class for implementing notifiers.

    A notifier is a class that can send notifications to a user about a successful login
    event. It has two abstract methods: `is_excluded` and `notify`.

    Attributes:
        excluded_ips (set[str]): A set of IP addresses to be excluded from notifications.
    """

    def __init__(self, excluded_ips: set[str] = None):
        excluded_ips = excluded_ips or set()

        for ip in excluded_ips:
            try:
                resolved_ip = gethostbyaddr(ip)[0]

                excluded_ips.discard(ip)
                excluded_ips.add(resolved_ip)
            except herror:
                pass

        self.excluded_ips = excluded_ips

    def is_excluded(self, ip_addr: str) -> bool:
        """
        Check if the given IP address is excluded from notifications.

        Args:
            ip_addr (str): The IP address to check.

        Returns:
            bool: True if the IP address is excluded, False otherwise.
        """
        return ip_addr in self.excluded_ips

    @abstractmethod
    def generate_message(self, notification: Notification) -> str:
        """
        Generate a message that contains the user, IP address, and location information.

        Args:
            notification (Notification): The notification object containing the user,
            IP address, and location information.

        Returns:
            str: A string that contains the user, IP address, and location information.
        """

    @abstractmethod
    def notify(self, notification: Notification) -> bool:
        """
        Notify the user about a successful login event.

        Args:
            notification (Notification): The notification object containing the user,
            IP address, and location information.

        Returns:
            bool: True if the notification was successful, False otherwise.
        """

"""
This module contains the main function of the program.

The main function reads input lines from `sys.stdin` and for each line, it parses it using the
`parser` instance.
If the parsed `login` object is not `None`, it locates the IP address using the `locator`
instance and creates a `Notification` object.
Finally, it sends the notification using the `notifier` instance.

The program expects the following environment variables:
- `GEOIP2_DB_PATH`: The path to the GeoIP2 database.
- `TELEGRAM_TOKEN`: The token of the Telegram bot.
- `TELEGRAM_CHAT_ID`: The chat ID of the recipient.
- `EXCLUDED_IPS`: A list of IP addresses or resolvable domains to be excluded from notifications,
separated by commas.
"""

import sys
from os import getenv
# pylint: disable=W4901
from parser.auditd import AuditD
# pylint: disable=W4901
from parser.base import Parser
from dotenv import load_dotenv
from locator.base import Locator
from locator.geoip2 import GeoIP
from notifier.base import Notification, Notifier
from notifier.telegram import Telegram


def main():
    """
    The main function of the program.

    This function loads environment variables using the `dotenv` module.
    It then creates instances of the `parser` class, `locator` class, and the `notifier` class.
    The `parser` instance is used to parse the input lines, the `locator` instance is used to locate
    the IP addresses, and the `notifier` instance is used to send notifications.

    The function reads input lines from `sys.stdin` and for each line, it parses it using the
    `parser` instance.
    If the parsed `login` object is not `None`, it locates the IP address using the `locator`
    instance and creates a `Notification` object.
    Finally, it sends the notification using the `notifier` instance.

    Parameters:
        None

    Returns:
        None
    """
    load_dotenv()

    parser: Parser = AuditD()
    locator: Locator = GeoIP(getenv('GEOIP2_DB_PATH'))

    excluded_ips = getenv('EXCLUDED_IPS').split(',')
    notifier: Notifier = Telegram(
        getenv('TELEGRAM_TOKEN'), getenv('TELEGRAM_CHAT_ID'), set(excluded_ips))

    for line in sys.stdin:
        login = parser.parse(line)

        if login is None:
            continue

        location = locator.locate(login.ip_addr)
        notification = Notification(login.user, login.ip_addr, location)
        notifier.notify(notification)


if __name__ == "__main__":
    main()

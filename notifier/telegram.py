"""
This module contains the Telegram notifier class.

A Telegram notifier is a class that can send notifications to a user about a successful login
event using the Telegram Bot API.

Classes:
    Telegram: A class that represents a Telegram notifier.
"""

from requests import post
from notifier.base import Notification, Notifier


class Telegram(Notifier):
    """
    This class represents a Telegram notifier.

    A Telegram notifier is a class that can send notifications to a user about a successful login
    event using the Telegram Bot API.

    Attributes:
        bot_token (str): The token of the Telegram bot.
        chat_id (str): The chat ID of the recipient.
        excluded_ips (set[str]): A set of IP addresses to be excluded from notifications.

    Methods:
        notify(self, notification: Notification) -> bool: Sends a notification to the user
            about a successful login event.
    """

    def __init__(self, bot_token: str, chat_id: str, excluded_ips: set[str] = None):
        super().__init__(excluded_ips)

        self.url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        self.params = {"chat_id": chat_id, "parse_mode": "Markdown"}

    def generate_message(self, notification: Notification) -> str:
        ip_addr = notification.ip_addr

        city = notification.location.city
        country = notification.location.country

        user = notification.user

        message = f"""
*💻 ROBERTSERVER 💻*
-----------
*✅ Successful login*
-----------
🛜 `{ip_addr}`
🌍 {city}, {country}

👤 `{user}`
"""

        return message

    def notify(self, notification: Notification) -> bool:
        ip_addr = notification.ip_addr

        if self.is_excluded(ip_addr):
            return True

        params = self.params | {"text": self.generate_message(notification)}
        response = post(self.url, json=params, timeout=30)

        # TODO: remove
        print("Telegram API response:", response.json())

        return response.ok

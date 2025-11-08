"""
Telegram notification module.
Handles sending error notifications to Telegram.
"""

import requests
from typing import Optional
from src.config import TELEGRAM_API_KEY, TELEGRAM_CHAT_ID, TELEGRAM_ENABLED
from src.utils import setup_logger

logger = setup_logger(__name__)


class TelegramNotifier:
    """Handles Telegram notifications."""

    def __init__(self):
        self.api_key = TELEGRAM_API_KEY
        self.chat_id = TELEGRAM_CHAT_ID
        self.enabled = TELEGRAM_ENABLED

        if not self.enabled:
            logger.warning("Telegram notifications are disabled. Set TELEGRAM_API_KEY and TELEGRAM_CHAT_ID in .env")

    def send_message(self, message: str) -> bool:
        """
        Send a message to Telegram.

        Args:
            message: Message text to send

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            logger.debug(f"Telegram disabled. Would have sent: {message}")
            return False

        try:
            url = f"https://api.telegram.org/bot{self.api_key}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            logger.debug("Telegram notification sent successfully")
            return True
        except requests.RequestException as e:
            logger.error(f"Failed to send Telegram notification: {e}")
            return False

    def send_error(self, error_message: str) -> bool:
        """
        Send an error notification to Telegram.

        Args:
            error_message: Error message to send

        Returns:
            True if successful, False otherwise
        """
        formatted_message = f"🚨 <b>Error Alert</b>\n\n{error_message}"
        return self.send_message(formatted_message)

    def send_info(self, info_message: str) -> bool:
        """
        Send an info notification to Telegram.

        Args:
            info_message: Info message to send

        Returns:
            True if successful, False otherwise
        """
        formatted_message = f"ℹ️ <b>Info</b>\n\n{info_message}"
        return self.send_message(formatted_message)


# Global notifier instance
notifier = TelegramNotifier()

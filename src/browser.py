"""
Browser automation module using Playwright.
Handles browser operations to find JSON endpoints.
"""

from typing import Optional
from playwright.sync_api import sync_playwright, Browser, Page
from src.config import (
    BOT_NAME,
    AUTOSCOUT_SEARCH_URL,
    BROWSER_HEADLESS,
    BROWSER_TIMEOUT,
    SORT_DROPDOWN_SELECTOR,
    SORT_OPTION,
    JSON_ENDPOINT_PATTERN
)
from src.utils import setup_logger
from src.notifier import notifier

logger = setup_logger(__name__)


class BrowserAutomation:
    """Handles browser automation to extract JSON endpoints."""

    def __init__(self):
        self.headless = BROWSER_HEADLESS
        self.timeout = BROWSER_TIMEOUT
        self.search_url = AUTOSCOUT_SEARCH_URL

    def find_json_endpoint(self) -> Optional[str]:
        """
        Find the JSON endpoint by monitoring network requests.

        Returns:
            JSON endpoint URL if found, None otherwise
        """
        json_endpoint = None

        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=self.headless)
                context = browser.new_context()
                page = context.new_page()

                # Set up response handler to capture JSON endpoint
                def handle_response(response):
                    nonlocal json_endpoint
                    if JSON_ENDPOINT_PATTERN in response.url:
                        json_endpoint = response.url
                        logger.debug(f"Found JSON endpoint: {response.url}")

                page.on("response", handle_response)

                # Navigate to the search page
                try:
                    logger.info("Loading AutoScout24 search page...")
                    page.goto(self.search_url, timeout=self.timeout)
                except Exception as e:
                    error_message = f"{BOT_NAME} - Page loading error: {str(e)}"
                    logger.error(error_message)
                    notifier.send_error(error_message)
                    browser.close()
                    return None

                # Select sort option and wait for network to be idle
                try:
                    logger.info("Selecting sort option...")
                    page.select_option(SORT_DROPDOWN_SELECTOR, SORT_OPTION)
                    page.wait_for_load_state("networkidle", timeout=self.timeout)
                except Exception as e:
                    error_message = f"{BOT_NAME} - Dropdown selection error: {str(e)}"
                    logger.error(error_message)
                    notifier.send_error(error_message)
                    browser.close()
                    return None

                browser.close()

                if json_endpoint is None:
                    error_message = f"{BOT_NAME} - JSON endpoint not found in network requests"
                    logger.error(error_message)
                    notifier.send_error(error_message)
                else:
                    logger.info("JSON endpoint found successfully")

                return json_endpoint

        except Exception as e:
            error_message = f"{BOT_NAME} - Browser automation error: {str(e)}"
            logger.error(error_message)
            notifier.send_error(error_message)
            return None


# Global browser automation instance
browser_automation = BrowserAutomation()

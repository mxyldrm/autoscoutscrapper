"""
Configuration module for AutoScout24 scraper.
Contains all configuration settings and constants.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
BOT_NAME = "AutoScout Bot"
SCRAPE_INTERVAL = 60  # seconds

# AutoScout24 settings
AUTOSCOUT_BASE_URL = "https://www.autoscout24.de"
AUTOSCOUT_SEARCH_URL = (
    "https://www.autoscout24.de/lst?atype=C&cy=D&damaged_listing=exclude&"
    "desc=0&ocs_listing=include&powertype=kw&search_id=26fztiow6l9&"
    "sort=leasing_rate&source=homepage_search-mask&ustate=N%2CU"
)

# Browser settings
BROWSER_HEADLESS = True
BROWSER_TIMEOUT = 60000  # milliseconds
SORT_DROPDOWN_SELECTOR = "#sort-dropdown-select"
SORT_OPTION = "age-descending"

# Scraping settings
PAGES_TO_SCRAPE = [1, 2]
JSON_ENDPOINT_PATTERN = "lst.json"

# User-Agent rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
]

# Telegram settings
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_ENABLED = bool(TELEGRAM_API_KEY and TELEGRAM_CHAT_ID)

# Database settings
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///autoscout.db")
DB_TABLE_NAME = "car_listings"

# Logging settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "autoscout_scraper.log"

"""
Utility functions and logging setup.
"""

import logging
from src.config import LOG_LEVEL, LOG_FORMAT, LOG_FILE

def setup_logger(name: str) -> logging.Logger:
    """
    Set up and configure logger.

    Args:
        name: Logger name

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL))
    console_formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(console_formatter)

    # File handler
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(getattr(logging, LOG_LEVEL))
    file_formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(file_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def format_price(price_dict: dict) -> str:
    """
    Format price from API response.

    Args:
        price_dict: Price dictionary from API

    Returns:
        Formatted price string
    """
    return price_dict.get('priceFormatted', 'Unknown price') if price_dict else 'Unknown price'


def extract_vehicle_features(vehicle_details: list) -> dict:
    """
    Extract vehicle features from details list.

    Args:
        vehicle_details: List of vehicle detail dictionaries

    Returns:
        Dictionary of features
    """
    features = {}
    for detail in vehicle_details:
        icon_name = detail.get('iconName')
        data = detail.get('data', 'Unknown')
        if icon_name:
            features[icon_name] = data
    return features


def build_car_url(listing_url: str) -> str:
    """
    Build full car URL from listing URL.

    Args:
        listing_url: Relative URL from listing

    Returns:
        Full URL
    """
    from src.config import AUTOSCOUT_BASE_URL
    return f"{AUTOSCOUT_BASE_URL}{listing_url}"

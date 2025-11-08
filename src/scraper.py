"""
Main scraping module.
Handles fetching and processing car listings from AutoScout24.
"""

import requests
import random
from typing import Optional, List, Dict
from src.config import USER_AGENTS, PAGES_TO_SCRAPE, BOT_NAME
from src.utils import (
    setup_logger,
    format_price,
    extract_vehicle_features,
    build_car_url
)
from src.database import db_manager
from src.notifier import notifier

logger = setup_logger(__name__)


class AutoScoutScraper:
    """Main scraper class for AutoScout24 listings."""

    def __init__(self):
        self.user_agents = USER_AGENTS
        self.pages_to_scrape = PAGES_TO_SCRAPE

    def _get_random_headers(self) -> Dict[str, str]:
        """
        Get random headers for request.

        Returns:
            Dictionary of HTTP headers
        """
        return {
            "User-Agent": random.choice(self.user_agents)
        }

    def _parse_listing(self, listing: Dict) -> Dict:
        """
        Parse a single listing into structured car information.

        Args:
            listing: Raw listing data from API

        Returns:
            Structured car information dictionary
        """
        car_id = listing['id']
        vehicle = listing.get('vehicle', {})

        # Extract basic info
        make = vehicle.get('make', 'Unknown make')
        model = vehicle.get('model', 'Unknown model')
        model_version = vehicle.get('modelVersionInput', '')
        model_and_brand = f"{make} {model} {model_version}".strip()

        # Extract price
        price_text = format_price(listing.get('price'))

        # Extract images
        images = listing.get('images', [])
        img_src = images[0] if images else 'Image not available'

        # Build car URL
        car_link = build_car_url(listing.get('url', ''))

        # Extract features
        vehicle_details = listing.get('vehicleDetails', [])
        features = extract_vehicle_features(vehicle_details)

        return {
            'ID': car_id,
            'Image': img_src,
            'Model and Make': model_and_brand,
            'Link': car_link,
            'Price': price_text,
            'Company': 'autoscout24',
            'Features': features,
            'Transmission': features.get('transmission', 'Unknown')
        }

    def scrape_listings(self, json_url: str) -> int:
        """
        Scrape car listings from the JSON endpoint.

        Args:
            json_url: JSON endpoint URL

        Returns:
            Number of new cars found
        """
        new_car_count = 0

        try:
            for page_num in self.pages_to_scrape:
                logger.info(f"Scraping page {page_num}...")

                # Update page number in URL
                paged_url = json_url.replace("page=1", f"page={page_num}")

                # Make request
                headers = self._get_random_headers()
                response = requests.get(paged_url, headers=headers, timeout=30)
                response.raise_for_status()

                # Parse JSON response
                json_data = response.json()
                listings = json_data.get('pageProps', {}).get('listings', [])

                logger.info(f"Found {len(listings)} listings on page {page_num}")

                # Process each listing
                for listing in listings:
                    try:
                        car_info = self._parse_listing(listing)
                        is_new = db_manager.insert_car(car_info)
                        if is_new:
                            new_car_count += 1
                    except Exception as e:
                        logger.error(f"Error parsing listing: {e}")
                        continue

            logger.info(f"Scraping completed. Found {new_car_count} new cars")
            return new_car_count

        except requests.RequestException as e:
            error_message = f"{BOT_NAME} - HTTP request error: {e}"
            logger.error(error_message)
            notifier.send_error(error_message)
            return 0
        except KeyError as e:
            error_message = f"{BOT_NAME} - JSON parsing error - missing key: {e}"
            logger.error(error_message)
            notifier.send_error(error_message)
            return 0
        except Exception as e:
            error_message = f"{BOT_NAME} - Unexpected error: {e}"
            logger.error(error_message)
            notifier.send_error(error_message)
            return 0


# Global scraper instance
scraper = AutoScoutScraper()

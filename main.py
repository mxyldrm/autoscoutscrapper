"""
Main entry point for AutoScout24 scraper.
Orchestrates the scraping process and runs the main loop.
"""

import time
from src.config import BOT_NAME, SCRAPE_INTERVAL
from src.utils import setup_logger
from src.browser import browser_automation
from src.scraper import scraper
from src.database import db_manager
from src.notifier import notifier

logger = setup_logger(__name__)


def run_scraper_cycle():
    """Run a single scraping cycle."""
    try:
        logger.info(f"{BOT_NAME} - Starting scraping cycle")

        # Find JSON endpoint
        json_endpoint = browser_automation.find_json_endpoint()

        if json_endpoint:
            # Scrape listings
            new_cars = scraper.scrape_listings(json_endpoint)
            logger.info(f"Scraping cycle completed. New cars: {new_cars}")
        else:
            error_message = f"{BOT_NAME} - Could not find JSON endpoint, skipping this cycle"
            logger.warning(error_message)

        # Clean up old listings
        deleted = db_manager.delete_old_cars(days=7)
        if deleted > 0:
            logger.info(f"Deleted {deleted} old car listings")

        # Log database stats
        total_cars = db_manager.get_car_count()
        logger.info(f"Total cars in database: {total_cars}")

    except Exception as e:
        error_message = f"{BOT_NAME} - Error in scraping cycle: {e}"
        logger.error(error_message)
        notifier.send_error(error_message)


def main():
    """Main function - runs the scraper in an infinite loop."""
    logger.info(f"{BOT_NAME} - Starting up...")
    logger.info(f"Scrape interval: {SCRAPE_INTERVAL} seconds")

    # Send startup notification
    notifier.send_info(f"{BOT_NAME} has started successfully!")

    cycle_count = 0

    while True:
        try:
            cycle_count += 1
            logger.info(f"\n{'='*50}")
            logger.info(f"Cycle #{cycle_count}")
            logger.info(f"{'='*50}\n")

            run_scraper_cycle()

            logger.info(f"Waiting {SCRAPE_INTERVAL} seconds until next cycle...\n")
            time.sleep(SCRAPE_INTERVAL)

        except KeyboardInterrupt:
            logger.info(f"{BOT_NAME} - Shutting down gracefully...")
            notifier.send_info(f"{BOT_NAME} has been stopped.")
            break
        except Exception as e:
            error_message = f"{BOT_NAME} - Critical error in main loop: {e}"
            logger.error(error_message)
            notifier.send_error(error_message)
            logger.info("Waiting before retry...")
            time.sleep(SCRAPE_INTERVAL)


if __name__ == "__main__":
    main()

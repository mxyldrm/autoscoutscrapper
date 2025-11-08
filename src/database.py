"""
Database module for storing and managing car listings.
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, Optional
from src.config import DATABASE_URL, DB_TABLE_NAME, BOT_NAME
from src.utils import setup_logger
from src.notifier import notifier

logger = setup_logger(__name__)


class DatabaseManager:
    """Manages database operations for car listings."""

    def __init__(self, db_path: str = "autoscout.db"):
        """
        Initialize database manager.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._create_tables()

    def _create_tables(self):
        """Create necessary database tables if they don't exist."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {DB_TABLE_NAME} (
                        id TEXT PRIMARY KEY,
                        model_and_make TEXT,
                        price TEXT,
                        link TEXT,
                        image TEXT,
                        company TEXT,
                        transmission TEXT,
                        features TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
                logger.info("Database tables verified/created successfully")
        except sqlite3.Error as e:
            error_msg = f"Database table creation error: {e}"
            logger.error(error_msg)
            notifier.send_error(error_msg)

    def insert_car(self, car_info: Dict) -> bool:
        """
        Insert or update a car listing in the database.

        Args:
            car_info: Dictionary containing car information

        Returns:
            True if inserted (new car), False if updated (existing car)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Check if car already exists
                cursor.execute(
                    f"SELECT id FROM {DB_TABLE_NAME} WHERE id = ?",
                    (car_info['ID'],)
                )
                exists = cursor.fetchone()

                if exists:
                    # Update existing car
                    cursor.execute(f"""
                        UPDATE {DB_TABLE_NAME}
                        SET model_and_make = ?,
                            price = ?,
                            link = ?,
                            image = ?,
                            company = ?,
                            transmission = ?,
                            features = ?,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, (
                        car_info['Model and Make'],
                        car_info['Price'],
                        car_info['Link'],
                        car_info['Image'],
                        car_info['Company'],
                        car_info['Transmission'],
                        json.dumps(car_info['Features']),
                        car_info['ID']
                    ))
                    logger.debug(f"Updated existing car: {car_info['ID']}")
                    return False
                else:
                    # Insert new car
                    cursor.execute(f"""
                        INSERT INTO {DB_TABLE_NAME}
                        (id, model_and_make, price, link, image, company, transmission, features)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        car_info['ID'],
                        car_info['Model and Make'],
                        car_info['Price'],
                        car_info['Link'],
                        car_info['Image'],
                        car_info['Company'],
                        car_info['Transmission'],
                        json.dumps(car_info['Features'])
                    ))
                    logger.info(f"New car added: {car_info['Model and Make']} - {car_info['Price']}")
                    notifier.send_info(
                        f"New car listing found!\n\n"
                        f"<b>{car_info['Model and Make']}</b>\n"
                        f"Price: {car_info['Price']}\n"
                        f"Transmission: {car_info['Transmission']}\n"
                        f"<a href='{car_info['Link']}'>View Listing</a>"
                    )
                    return True

                conn.commit()
        except sqlite3.Error as e:
            error_msg = f"Database insertion error: {e}"
            logger.error(error_msg)
            notifier.send_error(error_msg)
            return False

    def delete_old_cars(self, days: int = 7) -> int:
        """
        Delete car listings older than specified days.

        Args:
            days: Number of days threshold

        Returns:
            Number of deleted records
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cutoff_date = datetime.now() - timedelta(days=days)

                cursor.execute(
                    f"DELETE FROM {DB_TABLE_NAME} WHERE updated_at < ?",
                    (cutoff_date,)
                )
                deleted_count = cursor.rowcount
                conn.commit()

                if deleted_count > 0:
                    logger.info(f"Deleted {deleted_count} old car listings")

                return deleted_count
        except sqlite3.Error as e:
            error_msg = f"Database deletion error: {e}"
            logger.error(error_msg)
            notifier.send_error(error_msg)
            return 0

    def get_car_count(self) -> int:
        """
        Get total number of cars in database.

        Returns:
            Number of car listings
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT COUNT(*) FROM {DB_TABLE_NAME}")
                count = cursor.fetchone()[0]
                return count
        except sqlite3.Error as e:
            logger.error(f"Database count error: {e}")
            return 0


# Global database instance
db_manager = DatabaseManager()

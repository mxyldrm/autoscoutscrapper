# AutoScout24 Scraper

A professional, modular web scraper for monitoring new car listings from [AutoScout24](https://www.autoscout24.de).

## Features

- **Modular Architecture**: Clean separation of concerns with dedicated modules for browser automation, scraping, database operations, and notifications
- **Automated Monitoring**: Continuously monitors for new car listings
- **Smart Data Extraction**: Extracts comprehensive car details including make, model, price, transmission, and more
- **Database Storage**: SQLite database with automatic cleanup of old listings
- **Telegram Notifications**: Optional real-time notifications for new listings and errors
- **User-Agent Rotation**: Random User-Agent headers to avoid detection
- **Error Handling**: Robust error handling with logging and notifications
- **Configurable**: Easy configuration via environment variables

## Project Structure

```
autoscoutscrapper/
├── src/
│   ├── __init__.py       # Package initialization
│   ├── config.py         # Configuration settings
│   ├── browser.py        # Playwright browser automation
│   ├── scraper.py        # Scraping logic
│   ├── database.py       # Database operations
│   ├── notifier.py       # Telegram notifications
│   └── utils.py          # Utility functions and logging
├── main.py               # Entry point
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mxyldrm/autoscoutscrapper.git
   cd autoscoutscrapper
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**:
   ```bash
   playwright install chromium
   ```

5. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Telegram credentials (optional):
   ```env
   TELEGRAM_API_KEY=your_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   ```

## Configuration

All configuration is handled in `src/config.py` and can be overridden with environment variables:

### Core Settings
- `SCRAPE_INTERVAL`: Time between scraping cycles (default: 60 seconds)
- `PAGES_TO_SCRAPE`: List of pages to scrape (default: [1, 2])
- `BROWSER_HEADLESS`: Run browser in headless mode (default: True)

### Telegram Notifications (Optional)
To enable Telegram notifications:
1. Create a bot via [@BotFather](https://t.me/botfather)
2. Get your chat ID from [@userinfobot](https://t.me/userinfobot)
3. Set `TELEGRAM_API_KEY` and `TELEGRAM_CHAT_ID` in `.env`

### Database
- Default: SQLite database (`autoscout.db`)
- Old listings are automatically deleted after 7 days
- Supports PostgreSQL (set `DATABASE_URL` in `.env`)

## Usage

Run the scraper:
```bash
python main.py
```

The scraper will:
1. Open AutoScout24 search page
2. Find the JSON API endpoint
3. Scrape car listings from multiple pages
4. Store new listings in the database
5. Send Telegram notifications for new cars (if configured)
6. Clean up old listings
7. Wait for the configured interval and repeat

### Stopping the Scraper
Press `Ctrl+C` to gracefully stop the scraper.

## Module Documentation

### `src/config.py`
Contains all configuration settings including URLs, timeouts, User-Agents, and environment variables.

### `src/browser.py`
Handles browser automation using Playwright to find the JSON API endpoint by monitoring network requests.

### `src/scraper.py`
Main scraping logic that fetches and parses car listings from the JSON API.

### `src/database.py`
Manages SQLite database operations including inserting, updating, and deleting car listings.

### `src/notifier.py`
Sends Telegram notifications for new listings and errors.

### `src/utils.py`
Utility functions for logging, price formatting, and feature extraction.

## Logging

Logs are written to both:
- Console (stdout)
- File: `autoscout_scraper.log`

Log levels can be configured via `LOG_LEVEL` environment variable.

## Development

### Running Tests
```bash
# Install dev dependencies
pip install pytest

# Run tests (if implemented)
pytest
```

### Code Formatting
```bash
# Install black
pip install black

# Format code
black src/ main.py
```

## Troubleshooting

### Browser Issues
If Playwright fails to launch:
```bash
playwright install chromium
```

### Database Issues
If database errors occur, delete the database file and restart:
```bash
rm autoscout.db
python main.py
```

### Network Issues
If scraping fails consistently:
- Check your internet connection
- Verify the AutoScout24 website is accessible
- Check if the website structure has changed

## Disclaimer

**IMPORTANT**: This project is strictly for **educational purposes only**.

- Web scraping may violate the terms of service of websites
- Users are solely responsible for how they use this code
- The authors assume no liability for misuse or damages
- Always respect robots.txt and website terms of service
- Use reasonable scraping intervals to avoid overloading servers

## Legal Notice

This tool is provided "as is" without warranty of any kind. Use at your own risk. Always comply with:
- Website terms of service
- Local laws and regulations regarding web scraping
- Data protection regulations (GDPR, etc.)

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Author

**mxyldrm**

## Acknowledgments

- Built with [Playwright](https://playwright.dev/) for browser automation
- Uses [Requests](https://requests.readthedocs.io/) for HTTP requests
- Database management with SQLite

---

**Remember**: This is an educational project. Always use web scraping responsibly and ethically.

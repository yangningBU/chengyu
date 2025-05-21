# Chinese Idioms Scraper

This project scrapes a table of 100 classic Chinese idioms from [LingoAce](https://www.lingoace.com/zh/blog/100-classic-idioms-you-must-know-when-learning-chinese-cn/) and saves them to a CSV file.

## Setup Instructions

### 1. Clone the repository (if applicable)
```
git clone <your-repo-url>
cd chengyu
```

### 2. Create and activate a Python virtual environment
```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Install Brave Browser
- Download and install Brave from [brave.com/download](https://brave.com/download/)

### 5. Run the Selenium scraper
```
python selenium_scraper.py
```

This will create a file called `chinese_idioms.csv` with the scraped idioms.

## Notes
- The script uses Brave (a Chromium-based browser) in headless mode via Selenium and undetected-chromedriver.
- Make sure Brave is installed at the default location (`/Applications/Brave Browser.app/Contents/MacOS/Brave Browser`) on macOS. If not, update the `binary_location` in `selenium_scraper.py` accordingly.
- The original `scraper.py` uses requests/BeautifulSoup and will not work for this site, as the data is rendered by JavaScript.

## Troubleshooting
- If you encounter browser/driver version errors, ensure Brave is up to date.
- If you use a different OS or browser, you may need to adjust the script accordingly. 
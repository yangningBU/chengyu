import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import csv
import time
import os

def setup_browser():
    """Set up and return a configured Chrome browser instance."""
    options = uc.ChromeOptions()
    options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return uc.Chrome(options=options)

def parse_idioms_from_tables(html):
    """Extract idioms from BeautifulSoup tables."""
    idioms = []
    tables = html.find_all('table')
    for table in tables:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Skip header row
            cols = row.find_all('td')
            if len(cols) >= 4:
                idiom = {
                    'chinese': cols[1].text.strip(),
                    'pinyin': cols[2].text.strip(),
                    'meaning': cols[3].text.strip()
                }
                idioms.append(idiom)
    return idioms

def save_idioms_to_csv(idioms, filename='chinese_idioms.csv'):
    """Save idioms to a CSV file."""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['chinese', 'pinyin', 'meaning']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for idiom in idioms:
            writer.writerow(idiom)
    print(f"Successfully saved {len(idioms)} idioms to {filename}")

def scrape_lingoace_idioms_selenium():
    """Main function to scrape idioms using Selenium."""
    url = "https://www.lingoace.com/zh/blog/100-classic-idioms-you-must-know-when-learning-chinese-cn/"
    
    driver = setup_browser()
    try:
        driver.get(url)
        time.sleep(5)  # Wait for JS to render tables
        html = BeautifulSoup(driver.page_source, 'html.parser')
        idioms = parse_idioms_from_tables(html)
        save_idioms_to_csv(idioms)
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_lingoace_idioms_selenium() 
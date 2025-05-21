import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import csv
import time
import os

def scrape_lingoace_idioms_selenium():
    url = "https://www.lingoace.com/zh/blog/100-classic-idioms-you-must-know-when-learning-chinese-cn/"
    
    # Set up undetected-chromedriver for Brave
    options = uc.ChromeOptions()
    options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = uc.Chrome(options=options)
    
    try:
        driver.get(url)
        time.sleep(5)  # Wait for JS to render tables
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tables = soup.find_all('table')
        idioms = []
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
        with open('chinese_idioms.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['chinese', 'pinyin', 'meaning']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for idiom in idioms:
                writer.writerow(idiom)
        print(f"Successfully scraped {len(idioms)} idioms and saved to chinese_idioms.csv")
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_lingoace_idioms_selenium() 
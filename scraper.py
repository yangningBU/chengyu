import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_lingoace_idioms():
    # URL of the webpage
    url = "https://www.lingoace.com/zh/blog/100-classic-idioms-you-must-know-when-learning-chinese-cn/"
    
    # Headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Send GET request to the URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        print("HTML response snippet:")
        print(response.text[:2000])  # Print first 2000 chars for inspection
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all tables in the page
        tables = soup.find_all('table')
        
        if tables:
            print("First table HTML snippet:")
            print(tables[0].prettify()[:2000])  # Print first 2000 chars for inspection
        else:
            print("No tables found.")
        
        # List to store all idioms
        idioms = []
        
        # Process each table
        for table in tables:
            rows = table.find_all('tr')
            for row in rows[1:]:  # Skip header row
                cols = row.find_all('td')
                if len(cols) >= 4:  # Ensure we have enough columns (including the counter)
                    idiom = {
                        'chinese': cols[1].text.strip(),  # Changed from 0 to 1
                        'pinyin': cols[2].text.strip(),   # Changed from 1 to 2
                        'meaning': cols[3].text.strip()   # Changed from 2 to 3
                    }
                    idioms.append(idiom)
        
        # Save to CSV
        with open('chinese_idioms.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['chinese', 'pinyin', 'meaning']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for idiom in idioms:
                writer.writerow(idiom)
        
        print(f"Successfully scraped {len(idioms)} idioms and saved to chinese_idioms.csv")
        
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    scrape_lingoace_idioms() 
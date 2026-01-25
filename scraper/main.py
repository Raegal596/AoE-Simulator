import requests
from bs4 import BeautifulSoup
import json
import os
import time
from unit_scraper import UnitScraper

BASE_URL = "https://ageofempires.fandom.com"
UNIT_LIST_URL = f"{BASE_URL}/wiki/Unit_(Age_of_Empires)"
OUTPUT_FILE = os.path.join("data", "units.json")

def get_unit_links():
    print(f"Fetching unit list from {UNIT_LIST_URL}...")
    try:
        response = requests.get(UNIT_LIST_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        links = set()
        
        content = soup.find('div', class_='mw-parser-output')
        if not content:
            print("Could not find content div.")
            return []

        # Iterate over all list items in the content to find unit links
        # This covers the main lists like Barracks, Stable, etc.
        for li in content.find_all('li'):
            for a_tag in li.find_all('a', href=True):
                href = a_tag['href']
                title = a_tag.get('title', '')
                
                # Filter logic:
                # 1. Must be a wiki link (starts with /wiki/)
                # 2. No colons (avoids File:, Category:, Talk:, etc.)
                # 3. Avoid "Edit" sections or other utility links
                # 4. Filter out main generic pages if they appear
                
                if href.startswith('/wiki/') and ':' not in href:
                    # Additional check: exclude common non-unit words if they appear in lists
                    # But most links in these lists are units or upgrades.
                    # We might get "Battle Axe" (upgrade) logic-wise, but that's okay for now, 
                    # the UnitScraper might fail or we filter later.
                    
                    full_url = BASE_URL + href
                    links.add(full_url)
        
        return list(links)
    except Exception as e:
        print(f"Error fetching unit list: {e}")
        return []

def main():
    if not os.path.exists("data"):
        os.makedirs("data")

    links = get_unit_links()
    print(f"Found {len(links)} potential unit links.")
    
    units_data = []
    
    # Limit for testing/development if needed, but we want all.
    # links = links[:5] 
    
    for i, link in enumerate(links):
        print(f"[{i+1}/{len(links)}] Scraping {link}...")
        scraper = UnitScraper(link)
        if scraper.fetch():
            data = scraper.parse()
            if data:
                # Basic validation: ensure it has a name
                if data.get('name'):
                    units_data.append(data)
                else:
                    print(f"Skipping {link}: No name found (likely not a unit page).")
        
        # Be nice to the server
        time.sleep(0.5)

    print(f"Saving {len(units_data)} units to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(units_data, f, indent=2, ensure_ascii=False)
    print("Done.")

if __name__ == "__main__":
    main()

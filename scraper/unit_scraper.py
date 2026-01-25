import requests
from bs4 import BeautifulSoup
import re

class UnitScraper:
    def __init__(self, unit_url):
        self.url = unit_url
        self.soup = None
        self.data = {
            "name": "",
            "description": "",
            "costs": {},
            "stats": {},
            "civilization_bonuses": []
        }

    def fetch(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.content, 'html.parser')
            return True
        except Exception as e:
            print(f"Error fetching {self.url}: {e}")
            return False

    def parse(self):
        if not self.soup:
            return None
        
        self._parse_name()
        self._parse_description()
        self._parse_infobox()
        self._parse_bonuses()
        
        return self.data

    def _parse_name(self):
        # Title usually contains the name. 
        # But we can also get it from the header.
        header = self.soup.find('h1', class_='page-header__title')
        if header:
            # Remove whitespace and newlines
            self.data['name'] = header.get_text().strip()
    
    def _parse_description(self):
        # First paragraph of the content usually
        content = self.soup.find('div', class_='mw-parser-output')
        if content:
            # Find the first paragraph that isn't a figure or aside
            for p in content.find_all('p', recursive=False):
                text = p.get_text().strip()
                if text:
                    self.data['description'] = text
                    break

    def _parse_infobox(self):
        # The portable infobox
        infobox = self.soup.find('aside', class_='portable-infobox')
        if not infobox:
            return

        # Costs
        # They appear as separate data-sources: Food, Wood, Gold, Stone
        resources = ['Food', 'Wood', 'Gold', 'Stone']
        for res in resources:
            row = infobox.find('div', {'data-source': res})
            if row:
                value_div = row.find('div', class_='pi-data-value')
                if value_div:
                    val_text = value_div.get_text(strip=True)
                    # Use regex to just get the numbers, or keep text? 
                    # Prefer numbers if possible.
                    # Sometimes it might be "50 (base)" etc.
                    # Just taking the first number.
                    match = re.search(r'\d+', val_text)
                    if match:
                        self.data['costs'][res] = int(match.group(0))

        # Stats mapping
        # data-source key -> output key
        # Note: data-source is case sensitive
        stats_map = {
            'HP': 'Hit points',
            'Attack': 'Melee attack', # Sometimes just "Attack"
            'Range': 'Range',
            'ROF': 'Reload time',
            'Armor': 'Melee armor',
            'PierceArmor': 'Pierce armor',
            'Speed': 'Speed',
            'LOS': 'Line of Sight',
            'Garrison': 'Garrison'
        }
        
        for source, output_key in stats_map.items():
            row = infobox.find('div', {'data-source': source})
            if row:
                value_div = row.find('div', class_='pi-data-value')
                if value_div:
                    val = value_div.get_text(strip=True)
                    self.data['stats'][output_key] = val

        # Handle 'PierceAttack' if it exists differently or generic 'Attack'
        # Some units might have different attack types.
        # Check for 'PierceAttack' specifically?
        row = infobox.find('div', {'data-source': 'PierceAttack'})
        if row:
            value_div = row.find('div', class_='pi-data-value')
            if value_div:
                self.data['stats']['Pierce attack'] = value_div.get_text(strip=True)

    def _parse_bonuses(self):
        # Look for "Civilization bonuses" section
        # Usually an h2 or h3 with id="Civilization_bonuses"
        
        # Find the span with id
        span = self.soup.find('span', id='Civilization_bonuses')
        if not span:
             span = self.soup.find('span', id='Civilization_Bonuses')
        
        if span:
            # The section content follows. usually a ul/li list.
            # We need to find the parent header, then look for the next sibling that is a list
            header = span.parent
            
            # Iterate siblings until we hit another header or find a list
            curr = header.find_next_sibling()
            while curr and curr.name not in ['h1', 'h2']:
                if curr.name == 'ul':
                    for li in curr.find_all('li'):
                        text = li.get_text().strip()
                        # Format usually: "CivName: Bonus text"
                        if ':' in text:
                            civ, bonus = text.split(':', 1)
                            self.data['civilization_bonuses'].append({
                                'civilization': civ.strip(),
                                'bonus': bonus.strip()
                            })
                curr = curr.find_next_sibling()

if __name__ == "__main__":
    # Test with Clubman
    scraper = UnitScraper("https://ageofempires.fandom.com/wiki/Clubman")
    if scraper.fetch():
        import json
        print(json.dumps(scraper.parse(), indent=2))

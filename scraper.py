import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_live_prices(state_name):
    # Formats the state name for the website URL
    state_url = state_name.lower().replace(" ", "-")
    url = f"https://www.propertypro.ng/property-for-sale/in/{state_url}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            listings = soup.find_all('div', class_='single-room-sale')
            
            data = []
            for item in listings[:5]: # Get the top 5 houses
                price_tag = item.find('h3', class_='listings-price')
                title_tag = item.find('h2')
                
                if price_tag and title_tag:
                    data.append({
                        "Property Description": title_tag.text.strip(), 
                        "Listed Price": price_tag.text.strip()
                    })
            
            return pd.DataFrame(data)
    except Exception as e:
        return None
    return None

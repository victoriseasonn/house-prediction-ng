import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_live_prices(state_name):
    # This turns "Akwa Ibom" into "akwa-ibom" for the website link
    state_url = state_name.lower().replace(" ", "-")
    url = f"https://www.propertypro.ng/property-for-sale/in/{state_url}"
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        # The 'requests' part you mentioned!
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # PropertyPro uses this class for their listings
            listings = soup.find_all('div', class_='single-room-sale')
            
            data = []
            for item in listings[:5]: # Just get the first 5 houses
                price_tag = item.find('h3', class_='listings-price')
                title_tag = item.find('h2')
                
                if price_tag and title_tag:
                    data.append({
                        "House Type": title_tag.text.strip(), 
                        "Price": price_tag.text.strip()
                    })
            
            return pd.DataFrame(data)
    except:
        return None
    return None

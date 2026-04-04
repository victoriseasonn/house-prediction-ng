import pandas as pd
import random

def get_live_prices(state):
    # realistic Nigerian price ranges
    base_prices = {
        "Lagos": 50000000,
        "Abuja": 45000000,
        "Rivers": 30000000,
        "Oyo": 20000000,
        "Kano": 18000000,
        "Enugu": 22000000
    }

    base = base_prices.get(state, 15000000)

    properties = []
    for i in range(5):
        price = base + random.randint(5_000_000, 50_000_000)
        properties.append({
            "Property": f"{random.choice(['2', '3', '4', '5'])} Bedroom House in {state}",
            "Price (₦)": f"{price:,.0f}"
        })

    return pd.DataFrame(properties)

from bs4 import BeautifulSoup
import pandas as pd
import re

# Read the HTML file
with open('data/car_0.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Parse with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all car card containers
car_cards = soup.find_all('div', class_='styles_normalCardWrapper__qDZjq')

# Lists to store extracted data
car_names = []
prices = []
fuel_types = []
km_driven_list = []

# Extract data from each car card
for card in car_cards:
    car_name = 'Unknown'
    badge_content = card.find('div', class_='styles_badgeContent__J3Wnd')
    if badge_content:
        img = badge_content.find('img')
        if img and img.get('alt'):
            alt_text = img.get('alt')
            # Extract car name from alt text like "thumbail-icon-2021 Toyota Camry HYBRID"
            # Remove "thumbail-icon-" and extract year + car name
            if 'thumbail-icon-' in alt_text:
                car_name_part = alt_text.replace('thumbail-icon-', '').split(',')[0]
                car_name = car_name_part.strip()
            else:
                car_name = alt_text.split(',')[0].strip()
    
    # Extract kilometers driven
    km_elem = card.find('p', string=re.compile(r'\d+\.?\d*[kKlL]?\s*km', re.IGNORECASE))
    km_driven = km_elem.get_text(strip=True) if km_elem else 'N/A'
    
    # Extract fuel type 
    fuel_elem = card.find('p', string=re.compile(r'Petrol|Diesel|Hybrid|CNG|Electric', re.IGNORECASE))
    fuel_type = fuel_elem.get_text(strip=True) if fuel_elem else 'N/A'
    
    # Extract price
    price_elem = card.find('p', class_=re.compile('frDqEi'))
    if not price_elem:
        
        price_elem = card.find('p', string=re.compile(r'Rs.*(?:lakh|L)'))
    price = price_elem.get_text(strip=True) if price_elem else 'N/A'
    
    # Append to lists
    car_names.append(car_name)
    prices.append(price)
    fuel_types.append(fuel_type)
    km_driven_list.append(km_driven)

# Create DataFrame
df = pd.DataFrame({
    'Car Name': car_names,
    'Price': prices,
    'Fuel Type': fuel_types,
    'KM Driven': km_driven_list
})

# Save to CSV
df.to_csv('car_data.csv', index=False, encoding='utf-8')

print(f"Successfully extracted {len(df)} cars!")
print("\nFirst 10 rows:")
print(df.head(10))
print(f"\n Data saved to 'car_data.csv'")

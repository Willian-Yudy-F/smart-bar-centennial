import requests
from bs4 import BeautifulSoup
import pandas as pd

def update_menu_from_site():
    url = "URL_DO_SITE_DO_HOTEL_AQUI" # Substitua pela URL real do menu
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Exemplo de lógica (isso varia conforme a estrutura do site)
    drinks = []
    # Supondo que os drinks estejam em tags <h3> e ingredientes em <p>
    for item in soup.find_all('div', class_='menu-item'): 
        name = item.find('h3').text
        desc = item.find('p').text
        price = item.find('span', class_='price').text
        
        drinks.append({
            "drink": name,
            "ingredients": desc,
            "price": float(price.replace('$', '')),
            "category": "Signature" if "Signature" in url else "Classic"
        })
    
    new_df = pd.DataFrame(drinks)
    new_df.to_csv("data/drinks_updated.csv", index=False)
    return "Menu Sync Complete!"
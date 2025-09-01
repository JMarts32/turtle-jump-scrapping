import json
import os
import requests
from bs4 import BeautifulSoup, Tag

URL = 'https://en.wikipedia.org/wiki/ASEAN'
FILE = 'population.json'

# Wikipedia rejects automaticaly requests without a user-agent header
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/117.0 Safari/537.36"
}

def extractUrbanAreasTable():
    
    response = requests.get(URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    
    tables = soup.find_all("table", {"class": "wikitable"})
    target_table = None
    for table in tables:
        if table.find("th").getText(strip=True) == "Metropolitan area":
            target_table = table
            break
    return target_table

def createCountryDictionary(table: Tag):
    country_dictionary = {}
    rows = table.find_all("tr")[1:]
    for row in rows:
        cols = row.find_all(["td", "th"])
        
        core_city = cols[1].get_text(strip=True)
        
        metropolitan_area = cols[0].get_text(strip=True)
        population = int(cols[2].get_text(strip=True).replace(",", ""))
        area = float(cols[3].get_text(strip=True).replace(",", ""))

        country = cols[4].get_text(strip=True)
        
        density = population/area
        
        if country not in country_dictionary:
            country_dictionary[country] = {
                "cities": []
            }
            
        country_dictionary[country]["cities"].append({
        "metropolitan_area": metropolitan_area,
        "core_city": core_city,
        "population": population,
        "area_km2": area,
        "density": density
        })

    return country_dictionary
    
    
def saveFile(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)
        
def loadExistingData():
    if os.path.exists(FILE):
        with open(FILE, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except:
                return {}
    return {}

def main():
    old_data = loadExistingData()
    
    tables = extractUrbanAreasTable()
    new_data = createCountryDictionary(tables)
    
    if new_data != old_data:
        print(new_data)
        saveFile(new_data)
    else:
        print('No new data. file not modified')
        
main()
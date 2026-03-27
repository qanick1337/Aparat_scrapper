import requests
import pandas as pd
import time
import os
import re


# 1. Make the request to the Core API
def fetch_all_rentals():
    url = "https://www.sreality.cz/api/cs/v2/estates"
    all_apartments = []
    page = 1

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    })

    print("Starting data extraction...")

    while True:
        params = {
            "category_main_cb": 1,  # Apartments
            "category_type_cb": 2,  # Rent
            "category_sub_cb": 2,  # 1+kk
            "locality_region_id": 10,  # Prague
            "per_page": 60,  # The maximum Sreality allows per request???
            "page": page  # The current page in the loop
        }

        response = session.get(url, params=params)

        if response.status_code != 200:
            print(f"Failed to fetch page {page}. Status code: {response.status_code}")
            break

        data = response.json()
        estates = data.get("_embedded", {}).get("estates", [])

        if len(estates) == 0:
            print(f"Reached the end of the results at page {page}.")
            break

        all_apartments.extend(estates)
        print(f"Successfully fetched {len(estates)} items from page {page}...")


        page += 1
        time.sleep(1)
    print(f"Successfully fetched {len(all_apartments)} items")
    return pd.DataFrame(all_apartments)

def extract_area(name_string):
    match = re.search(r'(\d+)\s*m²', str(name_string))
    if match:
        return int(match.group(1))
    return None

def extract_district(locality_string):
    match = re.search(r'Praha(\s\d+)', str(locality_string))
    if match:
        return match.group(1)
    return "Praha Unknown"

# "{'lat': 50.10833, 'lon': 14.524261}"
def extract_coords(gps_string, coord_type):
    match = re.search(rf'{coord_type}\':\s([\d\.]+)', str(gps_string))
    if match:
        return match.group(1)
    return f"Unknown {coord_type}"



if os. path.isfile('appartments.csv'):
    apartments_list = pd.read_csv('appartments.csv')
else:
    apartments_list = fetch_all_rentals()
    res = apartments_list.copy().to_csv('appartments.csv', index=False)

apartments_list['area_m2'] = apartments_list['name'].apply(extract_area)
apartments_list['district'] = apartments_list['locality'].apply(extract_district)
apartments_list['lat'] = apartments_list['gps'].apply(lambda x: extract_coords(x, 'lat'))
apartments_list['lon'] = apartments_list['gps'].apply(lambda x: extract_coords(x, 'lon'))
# apartments_list['is_new_building'] =

params = ['area_m2', 'district']



apartments_list_sample = apartments_list[0:6]


for apartment in apartments_list_sample.itertuples(index=False):
    print(f"{apartment.name} | {apartment.price} CZK | {apartment.district} | {apartment.hash_id} | {apartment.area_m2}")
    print(f"{apartment.lat} lattidute and  {apartment.lon} lontidute ")

# print(f"How much nulls {apartments_list[params].isnull().sum()}")
print(f"Digga was duplicates ? {apartments_list.duplicated().sum()}")

apartments_list[params] = apartments_list[params].fillna(apartments_list[params].mode())
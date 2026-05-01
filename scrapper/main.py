import requests
import pandas as pd
import time
import os
import re
import ast
import math
import joblib

import sys
import django


from price_prediction import run_ml_inference
from train_model import model_init
from  testing_model import  testing_model


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.backend.settings')
django.setup()

from api.models import Apartment



# Make the request to the Core API
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
            "per_page": 80,
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
    return 0

def extract_coords(gps_string, coord_type):
    match = re.search(rf'{coord_type}\':\s([\d\.]+)', str(gps_string))
    if match:
        return match.group(1)
    return f"Unknown {coord_type}"

def extract_all_labels(labels_list):
    all_labels_list = []

    for elem in labels_list:
        if isinstance(elem, str):
            data_list = ast.literal_eval(elem)
        else:
            data_list = elem
        all_labels_list.append(data_list)

    unique_labels = []
    seen = set()

    for row in all_labels_list:
        for sub_cat in row:
            for label in sub_cat:
                if label not in seen:
                    unique_labels.append(label)
                    seen.add(label)

    return  unique_labels

def calculate_haversine(lat_a:float, lon_a:float, lat_b:float, lon_b:float):
    R = 6371.0
    # Convert degrees to radians
    lat_a_rad, lon_a_rad = math.radians(lat_a), math.radians(lon_a)
    lat_b_rad, lon_b_rad = math.radians(lat_b), math.radians(lon_b)

    # Differences
    delta_lat = lat_b_rad - lat_a_rad
    delta_lon = lon_b_rad - lon_a_rad

    # Haversine formula
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat_a_rad) * math.cos(lat_b_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def get_distance_to_local_center(gps_lat, gps_lon):
    prague_hubs = {
        "Mustek": (50.0844, 14.4236),
        "Namesti_Miru": (50.0753, 14.4370),
        "Pankrac": (50.0511, 14.4394),
        "Andel": (50.0724, 14.4020),
        "Dejvicka": (50.1005, 14.3956),
        "Karlin": (50.0910, 14.4480),
        "Holesovice": (50.1030, 14.4320),
        "Chodov": (50.0320, 14.4910),
        "Stodulky": (50.0460, 14.3070),
        "Letnany": (50.1230, 14.4980)
    }

    distances_to_hubs = {
        "Mustek": 0,
        "Namesti_Miru": 0,
        "Pankrac": 0,
        "Andel": 0,
        "Dejvicka": 0,
        "Karlin": 0,
        "Holesovice": 0,
        "Chodov": 0,
        "Stodulky": 0,
        "Letnany": 0
    }

    for hub in prague_hubs:
        (hub_lat, hub_lon) = prague_hubs[hub]
        distances_to_hubs[hub] = calculate_haversine(hub_lat,hub_lon,gps_lat,gps_lon)

    return min(distances_to_hubs.values())

def get_seo_locality(seo):
    if isinstance(seo, str):
        try:
            seo = ast.literal_eval(seo)
        except (ValueError, SyntaxError):
            return None
    if isinstance(seo, dict):
        return seo.get('locality')
    return None


def sync_apartments_to_db(df):
    print("Starting the synchronization with the DB")
    current_active_ids = []

    for index, row in df.iterrows():
        sreality_id = str(row['hash_id'])
        current_active_ids.append(sreality_id)

        defaults = {
            'price': row['price'],
            'area_m2': row['area_m2'],
            'district': row['district'],
            'seo_locality': row['seo_locality'],
            'distance_to_local_hub': row['distance_to_local_hub'],
            'furnished': bool(row.get('furnished', 0)),
            'partly_furnished': bool(row.get('partly_furnished', 0)),
            'not_furnished': bool(row.get('not_furnished', 0)),
            'metro': bool(row.get('metro', 0)),
            'tram': bool(row.get('tram', 0)),
            'new_building': bool(row.get('new_building', 0)),
            'after_reconstruction': bool(row.get('after_reconstruction', 0)),
            'brick': bool(row.get('brick', 0)),
            'panel': bool(row.get('panel', 0)),
            'elevator': bool(row.get('elevator', 0)),
            'cellar': bool(row.get('cellar', 0)),
            'garage': bool(row.get('garage', 0)),
            'parking_lots': bool(row.get('parking_lots', 0)),
            'is_active': True
        }

        Apartment.objects.update_or_create(
            sreality_id=sreality_id,
            defaults=defaults
        )

    inactive_count = Apartment.objects.exclude(sreality_id__in=current_active_ids).update(is_active=False)

    print(f"Successfully synchronized!")
    print(f"Actual apartments found/updated: {len(current_active_ids)}")
    print(f"Deactivated: {inactive_count} apartments")


apartments_list = fetch_all_rentals()

# Saving the data into .csv for human analyzing
res = apartments_list.copy().to_csv('appartments.csv', index=False)

# Extracting the area from the listing name
apartments_list['area_m2'] = apartments_list['name'].apply(extract_area)

# Extracting the district (e.g. 1 - Prague 1)
apartments_list['district'] = apartments_list['locality'].apply(extract_district)

# Extracting the SEO locality slug (e.g. 'praha-hloubetin-podebradska')
apartments_list['seo_locality'] = apartments_list['seo'].apply(lambda x: get_seo_locality(x))

# Extracting the coords
apartments_list['lat'] = apartments_list['gps'].apply(lambda x: extract_coords(x, 'lat'))
apartments_list['lon'] = apartments_list['gps'].apply(lambda x: extract_coords(x, 'lon'))

# Initializing the array with the parameters used in ML-learning
params = ['area_m2']

all_labels_list = extract_all_labels(apartments_list["labelsAll"])

# The meaningful labels, used in ML-learning
critical_labels = ['furnished', 'partly_furnished', 'not_furnished', 'metro', 'tram', 'new_building', 'after_reconstruction', 'brick', 'panel', 'elevator', 'cellar', 'garage', 'parking_lots']

# One hot encoding of district
districts = range(1,11)
for distr in districts:
    column = "prague_" + str(distr)
    apartments_list[column] = apartments_list['locality'].apply(lambda x, lbl=str(distr): 1 if lbl in str(x) else 0)
    params.append(column)


for label in critical_labels:
    apartments_list[label] = apartments_list['labelsAll'].apply(lambda x, lbl=label: 1 if lbl in str(x) else 0)
    params.append(label)

# Computing the distance to the local hub of the apartment's area
apartments_list['distance_to_local_hub'] = apartments_list.apply(lambda x: get_distance_to_local_center(float(x['lat']), float(x['lon'])), axis=1)
params.append('distance_to_local_hub')

params.append('price')
params.append('hash_id')
params.append('district')
params.append('seo_locality')

# Getting rid of the apartments with zero price
apartments_list = apartments_list.loc[apartments_list['price'] > 1]
apartments_list = apartments_list.loc[apartments_list['district'] != 0]

sync_apartments_to_db(apartments_list[params])

# Model re-initialization block
# params.remove('hash_id')
# params.remove('district')
# model_init(apartments_list[params])

# Starting price computation
run_ml_inference()



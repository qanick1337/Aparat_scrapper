import os
import sys
import django
import pandas as pd
import joblib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Apartment

def run_ml_inference():
    if not os.path.exists('rf_sreality_model.pkl'):
        print("Error: File of Ml-model rf_sreality_model.pkl is not found!")
        return

    model = joblib.load('rf_sreality_model.pkl')

    # We take only the active one appartaments
    apartments_to_predict = Apartment.objects.filter(is_active=True, predicted_price__isnull=True)

    if not apartments_to_predict.exists():
        print("No more new apartments to predict.")
        return

    print(f"Found {apartments_to_predict.count()} new apartments to predict.")

    # Transforming data
    data = list(apartments_to_predict.values())
    df = pd.DataFrame(data)

    #Recreating the structure to use in ML-model
    for i in range(1, 11):
        df[f'prague_{i}'] = (df['district'] == i).astype(int)

    features = [
        'area_m2',
        'prague_1', 'prague_2', 'prague_3', 'prague_4', 'prague_5',
        'prague_6', 'prague_7', 'prague_8', 'prague_9', 'prague_10',
        'furnished', 'partly_furnished', 'not_furnished',
        'metro', 'tram', 'new_building', 'after_reconstruction',
        'brick', 'panel', 'elevator', 'cellar', 'garage', 'parking_lots',
        'distance_to_local_hub'
    ]

    X = df[features]

    # Prediction
    predictions = model.predict(X)

    # Updating the DB
    for i, apt_obj in enumerate(apartments_to_predict):
        apt_obj.predicted_price = int(predictions[i])
        apt_obj.save()

    print(f"Successfully predicted price for {len(predictions)} appartaments.")


if __name__ == "__main__":
    run_ml_inference()
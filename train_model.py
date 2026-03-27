import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

def model_init(df):
    # df = pd.read_csv('clear_data.csv')

    X = df.drop('price', axis=1)
    y = df['price']

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    predictions = model.predict(X)

    mae = mean_absolute_error(y, predictions)

    print(f"Model trained successfully!")
    print(f"Mean Absolute Error while traning: {mae:,.2f} CZK")

    joblib.dump(model, 'rf_sreality_model.pkl')
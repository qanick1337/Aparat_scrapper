import pandas as pd
import joblib

def testing_model(df):
    # df = pd.read_csv('pred_data.csv')

    y = df['price']
    df = df.drop(['price'], axis=1)

    print("Model successfully loaded!")
    model = joblib.load('rf_sreality_model.pkl')

    predictions = model.predict(df)

    df['predicted_price'] = predictions
    df['price'] = y
    real_result = df.copy().to_csv('predicted_result.csv')
    print("Model successfully predicted prices!")

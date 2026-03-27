# Sreality Prague Rent Predictor

## Overview
An end-to-end Data Engineering and Machine Learning pipeline that scrapes rental listings from Sreality.cz, processes the raw data, and uses a Random Forest Regressor to predict the fair market value of apartments in Prague. This allows users to identify mathematically undervalued real estate and flag "good deals."

## Core Features
* **Automated Scraper:** Extracts live JSON data directly from the Sreality REST API.
* **Feature Engineering:** Cleans raw text, applies multi-label binarization for amenities (elevators, brick, metro access), and uses the Haversine formula to calculate distances to major Prague micro-centers (Anděl, Můstek, Karlín, etc.).
* **Machine Learning:** Uses `scikit-learn` to train a Random Forest model on processed historical data to predict rent prices, avoiding the curse of dimensionality.

## How to Start the Project

**1. Install Dependencies**
Ensure you have Python installed, then install all required packages:
```bash
pip install -r requirements.txt
```

**2. Run the Main Pipeline**
Execute the main script to start the data extraction and ETL process:
```bash
python main.py
```
**Project Structure**
*main.py*: Handles data ingestion from the Sreality API and the data cleaning/transformation process.

*train_model.py*: The script to train, test, and evaluate the Random Forest Regressor.

*testing_model.py*: The script that uses the trained model to make predictions on the remaining ~300 records.

*rf_sreality_model.pkl*: The serialized machine learning model, ready for backend inference.

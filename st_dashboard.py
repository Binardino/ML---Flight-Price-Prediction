import joblib
import numpy as np
import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(page_title='Flight Price Predictor',
                   page_icon='samolot',
                   layout='wide')

@st.cache_resource
def load_model(model_path):
    if not model_path.exists():
        st.error('Model not found. Please export first a trained model')
        st.stop()

    return joblib.load(model_path)


model_path = Path('artifacts') / 'flight_price_model.joblib'
model = load_model(model_path)

#%%
# defining variables - list & default var
AIRLINES            = ["IndiGo", "Air India", "Vistara", "SpiceJet", "GO FIRST", "AirAsia"]
CITIES              = ["Delhi", "Mumbai", "Bangalore", "Kolkata", "Hyderabad", "Chennai"]
TIME_BANDS          = ["Early_Morning", "Morning", "Afternoon", "Evening", "Night", "Late_Night"]
STOPS_LABEL_TO_NUM  = {"zero": 0, "one": 1, "two_or_more": 2}
CLASS_LABEL_TO_NUM  = {"Economy": 0, "Business": 1}    

#
def create_df():
    return pd.DataFrame([
        'airline'          : airline,
        'source_city'      : source_city,
        'destination_city' : destination_city,
        'departure_time'   : departure_time,
        'arrival_time'     : arrival_time,
        'duration'         : float(duration),
        'days_left'        : int(days_left),
        'stops_num'        : int(STOPS_LABEL_TO_NUM[stops_label]),
        'class_num'        : int(CLASS_LABEL_TO_NUM([class_label])),
    ])

def format_indian_roupies(x):
    return f"₹ {float(x):,0f}".replace(",", " ")
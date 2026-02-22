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

#header
st.markdown(
    """
    <div class="header">
    <h1> Flight Price Finder</h1>
    <p>Online interface to find ticket price</p>
    """,
    unsafe_allow_html=True
)

#Central bloc code - search engine & form
st.markown('<div class="searchwrap">', unsafe_allow_hmtl=True)

with st.container():
    col1, col2, col3 = st.columns([1.1, 1.1, 1], 
                                  vertical_alignment="bottom")
    
    with col1:
        source_city      = st.selectbox('Origin city', CITIES, index=0)

    with col2:
        destination_city = st.selectbox('Destination city', CITIES, index=1)

    with col3:
        class_label      = st.segmented_control('Class', options=['Economy', 'Business'], default='Economy')

    col4, col5, col6, col7 = st.columns([1,1,1,1], vertical_alignment='bottom')

    with col4:
        airline = st.selectbox('Carrier', AIRLINES, index=0)

    with col5:
        stops_label = st.selectbox('Stop over', ['zero', 'one', 'two_or_more'], index=0)

    with col6:
        days_left = st.slider('Days before flight', 
                              min_value=1, max_value=60, value=15)

    with col7:
        duration = st.number_input('Duration (in hours)', 
                                   min_value=0.5, max_value=60.0, value=2.5,
                                   steps=0.5)
        
    col8, col9 = st.columns([1,1], vertical_alignment='bottom')

    with col8:
        departure_time = st.selectbox('Start time', TIME_BANDS, index=1)

    with col9:
        arrival_time   = st.selectbox('Arrival time', TIME_BANDS, index=3)

    st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
    run = st.button('Search for best price', width='stretch')


st.markdown("</div>", unsafe_allow_html=True)

#print results
st.markdown("<div style='height: 12px'></div>", unsafe_allow_html=True)

if run:
    if source_city == destination_city:
        st.warning("Origin & destination are identical : please choose two different cities")

    else:
        X_input = create_df(
            airline=airline,
            source_city=source_city,
            destination_city=destination_city,
            departure_time=departure_time,
            arrival_time=arrival_time,
            duration=duration,
            days_left=days_left,
            stops_label=stops_label,
            class_label=class_label,
        )
        
        pred = model.predict(X_input)[0]
        pred = max(0,0, float(pred))
import joblib
import numpy as np
import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(page_title='Flight Price Predictor',
                   page_icon='samolot',
                   layout='wide')

@st.cache_resource

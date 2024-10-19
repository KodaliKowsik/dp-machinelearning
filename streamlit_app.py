import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Custom CSS to add background image
def add_background(image_file):
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url({image_file});
             background-size: cover;
             background-repeat: no-repeat;
             background-attachment: fixed;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

# Add background image of wheat and paddy fields
add_background('https://example.com/wheat_paddy_background.jpg')  # Replace with your actual image URL or local file

# Title of the app
st.title('Crop Recommendation: Wheat or Paddy')

st.info('This app uses a machine learning model to recommend the best crop (Wheat or Paddy) based on your input!')

# Create a dataset for demonstration purposes (replace with real data in practice)
# Example dataset with soil nutrients and conditions
data = {
    'soil_type': ['Loamy', 'Sandy', 'Clay', 'Loamy', 'Sandy', 'Clay'],
    'temperature': [20, 30, 25, 18, 32, 28],
    'rainfall': [200, 150, 220, 180, 140, 160],
    'humidity

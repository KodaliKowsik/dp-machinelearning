import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier   


# Title of the app
st.title('Crop Recommendation: Wheat or Paddy')

st.info('This app uses a machine learning model to recommend the best crop (Wheat or Paddy) based on your input!', icon="")  # Added icon

# Set background image
st.set_page_config(page_title="Crop Recommendation App", page_icon="", layout="wide")  # Improved layout and title

with st.container():
    st.image("https://namkalam.in/wp-content/uploads/2021/07/rice-vs-wheat-which-is-healthier.jpg", use_column_width=True)  # Display background image

# Create a dataset for demonstration purposes (replace with real data in practice)
# Example dataset with soil nutrients and conditions
data = {
    'soil_type': ['Loamy', 'Sandy', 'Clay', 'Loamy', 'Sandy', 'Clay'],
    'temperature': [20, 30, 25, 18, 32, 28],
    'rainfall': [200, 150, 220, 180, 140, 160],
    'humidity': [50, 65, 70, 45, 60, 55],
    'nitrogen': [50, 40, 60, 55, 45, 65],
    'phosphorus': [30, 35, 40, 20, 45, 25],
    'sulphur': [20, 25, 30, 15, 35, 20],
    'potassium': [40, 50, 55, 60, 45, 50],
    'crop': ['Wheat', 'Paddy', 'Paddy', 'Wheat', 'Paddy', 'Wheat']
}

df = pd.DataFrame(data)

with st.expander('Data'):
    st.write('Raw data used for training')
    st.dataframe(df)

# Input features for the sidebar
with st.sidebar:
    st.header('Input Conditions for Your Farm')

    soil_type = st.selectbox('Soil Type', ('Loamy', 'Sandy', 'Clay'))
    temperature = st.slider('Temperature (°C)', 10, 45, 25)
    rainfall = st.slider('Rainfall (mm)', 50, 300, 150)
    humidity = st.slider('Humidity (%)', 30, 90, 60)

    nitrogen = st.slider('Nitrogen (N) level', 0, 100, 50)
    phosphorus = st.slider('Phosphorus (P) level', 0, 100, 30)
    sulphur = st.slider('Sulphur (S) level', 0, 100, 20)
    potassium = st.slider('Potassium (K) level', 0, 100, 40)

    # Create DataFrame for the input features
    input_data = {
        'soil_type': soil_type,
        'temperature': temperature,
        'rainfall': rainfall,
        'humidity': humidity,
        'nitrogen': nitrogen,
        'phosphorus': phosphorus,
        'sulphur': sulphur,
        'potassium': potassium
    }
    input_df = pd.DataFrame(input_data, index=[0])

# Display user input
with st.expander('Input features'):
    st.write('Here are the conditions you provided:')
    st.dataframe(input_df)

# Data preparation
X_raw = df.drop('crop', axis=1)
y_raw = df['crop']

# One-hot encode categorical features (soil_type)
X_encoded = pd.get_dummies(X_raw, columns=['soil_type'])
input_encoded = pd.get_dummies(input_df, columns=['soil_type'])

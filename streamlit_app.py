import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Title of the app
st.title('Crop Recommendation: Wheat or Paddy')

st.info('This app uses a machine learning model to recommend the best crop (Wheat or Paddy) based on your input!')

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

# Ensure input_encoded has the same columns as X_encoded
input_encoded = input_encoded.reindex(columns=X_encoded.columns, fill_value=0)

# Encode the target variable (crop: Wheat=0, Paddy=1)
target_mapper = {'Wheat': 0, 'Paddy': 1}
y = y_raw.map(target_mapper)

# Model training and prediction
clf = RandomForestClassifier()
clf.fit(X_encoded, y)

# Prediction for the input data
prediction = clf.predict(input_encoded)
prediction_proba = clf.predict_proba(input_encoded)

# Display the prediction probabilities
df_prediction_proba = pd.DataFrame(prediction_proba, columns=['Wheat', 'Paddy'])

st.subheader('Prediction Results')
st.write('Probability for each crop:')
st.dataframe(df_prediction_proba)

# Display the recommended crop
crops = np.array(['Wheat', 'Paddy'])
st.success(f'Recommended Crop: {crops[prediction][0]}')

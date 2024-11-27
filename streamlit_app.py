import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Define user credentials (for demonstration)
USER_CREDENTIALS = {
    "admin": "password123",
    "user1": "cropapp2024"
}

# Initialize session state for login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = None

# Login function
def login(username, password):
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        st.success(f"Welcome, {username}!")
    else:
        st.error("Invalid username or password.")

# Logout function
def logout():
    st.session_state["logged_in"] = False
    st.session_state["username"] = None
    st.success("Logged out successfully!")

# Main app logic
if not st.session_state["logged_in"]:
    # Login page
    st.title("Login Page")
    st.info("Please log in to access the Crop Recommendation App.")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        login(username, password)
else:
    # Logged-in user view
    st.sidebar.button("Logout", on_click=logout)
    st.sidebar.success(f"Logged in as: {st.session_state['username']}")

    # App title and information
    st.title('Crop Recommendation: Wheat / Paddy')
    st.info('This app uses a machine learning model to recommend the best crop (Wheat or Paddy) based on your input!')

    # Dataset for demonstration purposes (expanded with new soil types)
    data = {
        'soil_type': ['Loamy', 'Sandy', 'Clay', 'Loamy', 'Sandy', 'Clay', 'Black', 'Alluvial', 'Red'],
        'temperature': [20, 30, 25, 18, 32, 28, 25, 27, 22],
        'rainfall': [20, 15, 22, 18, 14, 16, 23, 21, 19],  # Rainfall in cm
        'humidity': [50, 65, 70, 45, 60, 55, 68, 52, 62],
        'nitrogen': [50, 40, 60, 55, 45, 65, 55, 60, 50],
        'phosphorus': [30, 35, 40, 20, 45, 25, 40, 35, 30],
        'sulphur': [20, 25, 30, 15, 35, 20, 28, 22, 25],
        'potassium': [40, 50, 55, 60, 45, 50, 60, 55, 52],
        'crop': ['Wheat', 'Paddy', 'Paddy', 'Wheat', 'Paddy', 'Wheat', 'Wheat', 'Paddy', 'Wheat']
    }

    df = pd.DataFrame(data)

    with st.expander('Data'):
        st.write('Raw data used for training:')
        st.dataframe(df)

    # Sidebar input for the user
    with st.sidebar:
        st.header('Input Conditions for Your Farm')
        
        soil_type = st.selectbox('Soil Type', ('Loamy', 'Sandy', 'Clay', 'Black', 'Alluvial', 'Red'))
        temperature = st.slider('Temperature (°C)', 10, 45, 25)
        rainfall = st.slider('Rainfall (cm)', 5, 30, 15)  # Adjusted to cm
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

    # Model training
    clf = RandomForestClassifier()
    clf.fit(X_encoded, y)

    # Prediction based on input data
    prediction = clf.predict(input_encoded)
    predicted_crop = 'Wheat' if prediction[0] == 0 else 'Paddy'

    # Display prediction
    st.subheader('Prediction Results')
    st.success(f'Recommended Crop: {predicted_crop}')

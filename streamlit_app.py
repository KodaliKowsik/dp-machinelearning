port streamlit as st
import numpy as np
import pandas as pd
import requests
import time
from sklearn.ensemble import RandomForestRegressor

# Define user credentials (for demonstration)
USER_CREDENTIALS = {
    "admin": "password123",
    "user1": "airquality2024"
}

# Add custom CSS for background image
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

# Add background image\add_background('https://i.postimg.cc/kgHLg4YL/premium-photo-1698086768776-2fe137e167df.avif')

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
    st.info("Please log in to access the Air Quality Monitoring System.")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        login(username, password)
else:
    # Logged-in user view
    st.sidebar.button("Logout", on_click=logout)
    st.sidebar.success(f"Logged in as: {st.session_state['username']}")

    # App title and information
    st.title('Air Quality Monitoring System')
    st.info('This app displays real-time air quality data using sensor readings from an Arduino IoT system.')

    # Fetch air quality data from API (replace with actual endpoint)
    def fetch_air_quality_data():
        try:
            response = requests.get('https://api.example.com/airquality')  # Replace with actual API URL
            data = response.json()
            return data
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            return None
    
    # Display real-time air quality data
    placeholder = st.empty()
    while True:
        air_quality_data = fetch_air_quality_data()
        if air_quality_data:
            aqi = air_quality_data.get('aqi', 'N/A')
            co2 = air_quality_data.get('co2', 'N/A')
            pm25 = air_quality_data.get('pm2.5', 'N/A')
            humidity = air_quality_data.get('humidity', 'N/A')

            placeholder.markdown(f"""
                ### Real-time Air Quality Data:
                - **AQI Level**: {aqi}
                - **CO2 Level**: {co2} ppm
                - **PM2.5 Concentration**: {pm25} µg/m³
                - **Humidity**: {humidity} %
            """)
        time.sleep(5)  # Refresh every 5 seconds

import streamlit as st
import base64

# Function to set background image
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function with the path to the uploaded image
add_bg_from_local('/mnt/data/image.png')

# Your existing app code here
st.title('Crop Recommendation: Wheat or Paddy')
st.info('This app uses a machine learning model to recommend the best crop (Wheat or Paddy) based on your input!', icon="ℹ️")

# Rest of the Streamlit app code

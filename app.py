import streamlit as st
import pandas as pd
from math import radians, sin, cos, sqrt, atan2

# Page configuration
st.set_page_config(page_title="Delhi Metro Distance Checker", layout="wide")

# Load dataset
@st.cache_data
def load_data():
    data = pd.read_csv("Metro_data.csv")
    data['Opening Date'] = pd.to_datetime(data['Opening Date'])
    data['Opening Year'] = data['Opening Date'].dt.year
    return data

metro_data = load_data()

# Function to calculate the distance between two stations using the Haversine formula
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius of Earth in kilometers
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c  # Output distance in kilometers
    return distance


# Sidebar for user options
st.sidebar.header("Metro Data Options")

# Check what the user wants to see
user_choice = st.sidebar.radio(
    "What would you like to do?",
    ("Check Distance Between Metro Stations", "See Additional Data and Analysis")
)

# Main page for checking distance between stations
if user_choice == "Check Distance Between Metro Stations":
    st.subheader("Check Distance Between Two Metro Stations")

    # Dropdowns to select two stations
    station_1 = st.selectbox('Select First Station:', metro_data['Station Name'].unique())
    station_2 = st.selectbox('Select Second Station:', metro_data['Station Name'].unique())

    if station_1 != station_2:
        # Get latitude and longitude for the selected stations
        station_1_data = metro_data[metro_data['Station Name'] == station_1].iloc[0]
        station_2_data = metro_data[metro_data['Station Name'] == station_2].iloc[0]

        lat1, lon1 = station_1_data['Latitude'], station_1_data['Longitude']
        lat2, lon2 = station_2_data['Latitude'], station_2_data['Longitude']

        # Calculate the distance between the two stations
        distance = haversine(lat1, lon1, lat2, lon2)

        # Display the result
        st.write(f"The distance between **{station_1}** and **{station_2}** is **{distance:.2f} km**.")
    else:
        st.write("Please select two different metro stations to calculate the distance.")

# Option for seeing additional data and analysis
elif user_choice == "See Additional Data and Analysis":
    st.subheader("Additional Data and Analysis")

    # Show raw data
    if st.sidebar.checkbox("Show raw Metro data"):
        st.write(metro_data)

    # Show missing values and data types
    if st.sidebar.checkbox("Show Missing Values and Data Types"):
        st.subheader("Missing Values & Data Types")
        missing_values = metro_data.isnull().sum()
        data_types = metro_data.dtypes
        st.write("Missing Values:")
        st.write(missing_values)
        st.write("Data Types:")
        st.write(data_types)

    # Show the map of Delhi Metro stations
    if st.sidebar.checkbox("Show Metro Map"):
        st.subheader("Delhi Metro Map")

        # Use st.map to display the stations on a map
        map_data = metro_data[['Latitude', 'Longitude']]  # Extract lat and long for st.map
        st.map(map_data)

# Footer message
st.sidebar.markdown("**Delhi Metro Data Analysis App**")

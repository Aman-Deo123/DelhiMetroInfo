import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium # type: ignore
from streamlit_folium import st_folium # type: ignore
from math import radians, sin, cos, sqrt, atan2

# Page configuration
st.set_page_config(page_title="Delhi Metro Data Analysis", layout="wide")

# Load dataset
@st.cache_data
def load_data():
    data = pd.read_csv("Metro_data.csv")
    data['Opening Date'] = pd.to_datetime(data['Opening Date'])
    data['Opening Year'] = data['Opening Date'].dt.year
    return data

metro_data = load_data()

# Helper function to validate coordinates
def is_valid_coordinates(lat, lon):
    """Check if latitude and longitude are valid."""
    return -90 <= lat <= 90 and -180 <= lon <= 180

# Function to calculate distance between two stations using the Haversine formula
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius of Earth in kilometers
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

# Sidebar controls
st.sidebar.header("Metro Data Analysis Options")
user_choice = st.sidebar.selectbox("What would you like to see?", 
                                    ("Raw Data", "Metro Map", "Data Types and Missing Values", 
                                     "Perform Analysis", "Fare Calculator", "Data Debug"))

# Raw data display
if user_choice == "Raw Data":
    if st.sidebar.checkbox("Show raw Metro data"):
        st.write(metro_data)

# Fare Calculator
if user_choice == "Fare Calculator":
    st.subheader("Station-wise Fare Calculator")

    fare_structure = {
        '0-500 km': 70,
        '500-1000 km': 130,
        '1000-3000 km': 220,
        '3000+ km': 280,
        '5000+ km': 320
    }

    station_1 = st.selectbox('Select Starting Station:', metro_data['Station Name'].unique())
    station_2 = st.selectbox('Select Destination Station:', metro_data['Station Name'].unique())

    if station_1 != station_2:
        station_1_data = metro_data[metro_data['Station Name'] == station_1].iloc[0]
        station_2_data = metro_data[metro_data['Station Name'] == station_2].iloc[0]

        lat1, lon1 = station_1_data['Latitude'], station_1_data['Longitude']
        lat2, lon2 = station_2_data['Latitude'], station_2_data['Longitude']

        if is_valid_coordinates(lat1, lon1) and is_valid_coordinates(lat2, lon2):
            distance = haversine(lat1, lon1, lat2, lon2)
            st.write(f"The distance between **{station_1}** and **{station_2}** is **{distance:.2f} km**.")

            if distance <= 500:
                fare = fare_structure['0-500 km']
            elif distance <= 1000:
                fare = fare_structure['500-1000 km']
            elif distance <= 3000:
                fare = fare_structure['1000-3000 km']
            elif distance <= 5000:
                fare = fare_structure['3000+ km']
            else:
                fare = fare_structure['5000+ km']

            st.write(f"The fare from **{station_1}** to **{station_2}** is **₹{fare}**.")
        else:
            st.write("Invalid coordinates found for the selected stations. Please check the data.")
    else:
        st.write("Please select two different metro stations to calculate the fare.")

# Distance Checker
st.subheader("Check Distance Between Two Metro Stations")

station_1 = st.selectbox('Select First Station:', metro_data['Station Name'].unique(), key='dist_station1')
station_2 = st.selectbox('Select Second Station:', metro_data['Station Name'].unique(), key='dist_station2')

if station_1 != station_2:
    station_1_data = metro_data[metro_data['Station Name'] == station_1].iloc[0]
    station_2_data = metro_data[metro_data['Station Name'] == station_2].iloc[0]

    lat1, lon1 = station_1_data['Latitude'], station_1_data['Longitude']
    lat2, lon2 = station_2_data['Latitude'], station_2_data['Longitude']

    if is_valid_coordinates(lat1, lon1) and is_valid_coordinates(lat2, lon2):
        distance = haversine(lat1, lon1, lat2, lon2)
        st.write(f"The distance between **{station_1}** and **{station_2}** is **{distance:.2f} km**.")
    else:
        st.write("Invalid coordinates found for the selected stations. Please check the data.")
else:
    st.write("Please select two different metro stations to calculate the distance.")

# Debugging Dataset
if user_choice == "Data Debug":
    st.subheader("Debugging Dataset for Issues")
    st.write("Checking for missing or invalid coordinates:")
    
    if metro_data[['Latitude', 'Longitude']].isnull().any().any():
        st.warning("The dataset contains missing latitude or longitude values.")
        st.write(metro_data[metro_data[['Latitude', 'Longitude']].isnull()])
    
    invalid_coords = metro_data[
        ~metro_data.apply(lambda row: is_valid_coordinates(row['Latitude'], row['Longitude']), axis=1)
    ]

    if not invalid_coords.empty:
        st.warning("The following stations have invalid coordinates:")
        st.write(invalid_coords[['Station Name', 'Latitude', 'Longitude']])
    else:
        st.success("All latitude and longitude values are valid.")

# Metro Map
# Folium Metro Map
if user_choice == "Metro Map":
    st.subheader("Delhi Metro Map")

    # Define valid colors for the metro lines
    line_colors = {
        'Red line': 'red',
        'Blue line': 'blue',
        'Yellow line': 'beige',
        'Green line': 'green',
        'Violet line': 'purple',
        'Pink line': 'pink',
        'Magenta line': 'darkred',
        'Orange line': 'orange',
        'Rapid Metro': 'cadetblue',
        'Aqua line': 'blue',
        'Green line branch': 'green',
        'Blue line branch': 'lightblue',
        'Gray line': 'gray'
    }

    # Create the folium map
    delhi_map = folium.Map(location=[28.7041, 77.1025], zoom_start=11)

    for index, row in metro_data.iterrows():
        line = row['Line']
        color = line_colors.get(line, 'blue')  # Default color is blue if line not found
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=row['Station Name'],
            tooltip=f"{row['Station Name']} - {line}",
            icon=folium.Icon(color=color)
        ).add_to(delhi_map)

    # Display the Folium map in Streamlit
    st_folium(delhi_map, width=700, height=500)


# Perform Analysis
if user_choice == "Perform Analysis":
    analysis_choice = st.sidebar.selectbox("Select Analysis Type", 
                                           ("Stations Opened Each Year", 
                                            "Metro Line Analysis", 
                                            "Station Layout Distribution"))
    if analysis_choice == "Stations Opened Each Year":
        stations_per_year = metro_data['Opening Year'].value_counts().sort_index()
        fig = px.bar(stations_per_year, labels={"x": "Year", "y": "Number of Stations"})
        st.plotly_chart(fig)
    elif analysis_choice == "Metro Line Analysis":
        st.write("Analysis for Metro Lines")
    elif analysis_choice == "Station Layout Distribution":
        st.write("Station Layout Analysis")

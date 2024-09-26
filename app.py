import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from streamlit_folium import folium_static
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

# Sidebar controls
st.sidebar.header("Metro Data Analysis Options")

# Feature to ask user what they want to see
user_choice = st.sidebar.selectbox("What would you like to see?", 
                                    ("Raw Data", "Metro Map", "Data Types and Missing Values", "Perform Analysis"))

# Show raw data
if user_choice == "Raw Data":
    if st.sidebar.checkbox("Show raw Metro data"):
        st.write(metro_data)

# Function to calculate the distance between two stations using Haversine formula
def haversine(lat1, lon1, lat2, lon2):
    # Radius of Earth in kilometers
    R = 6371.0
    
    # Converting latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Differences in coordinates
    dlat = lat2 - lat1
    dlon = lat2 - lon1
    
    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c  # Output distance in kilometers
    return distance

# Add check distance feature on the front page
st.subheader("Check Distance Between Two Metro Stations")

# Dropdowns to select two stations
station_1 = st.selectbox('Select First Station:', metro_data['Station Name'].unique())
station_2 = st.selectbox('Select Second Station:', metro_data['Station Name'].unique())

# Get latitude and longitude for the selected stations
if station_1 != station_2:
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

# Display Data Types and Missing Values if selected
if user_choice == "Data Types and Missing Values":
    st.subheader("Missing Values & Data Types")
    missing_values = metro_data.isnull().sum()
    data_types = metro_data.dtypes
    st.write("Missing Values:")
    st.write(missing_values)
    st.write("Data Types:")
    st.write(data_types)

# Folium Metro Map
if user_choice == "Metro Map":
    st.subheader("Delhi Metro Map")

    # Define colors for the metro lines
    line_colors = {
        'Red line': 'red',
        'Blue line': 'blue',
        'Yellow line': 'beige',
        'Green line': 'green',
        'Voilet line': 'purple',
        'Pink line': 'pink',
        'Magenta line': 'darkred',
        'Orange line': 'orange',
        'Rapid Metro': 'cadetblue',
        'Aqua line': 'black',
        'Green line branch': 'lightgreen',
        'Blue line branch': 'lightblue',
        'Gray line': 'lightgray'
    }

    # Create the folium map
    delhi_map = folium.Map(location=[28.7041, 77.1025], zoom_start=11)

    for index, row in metro_data.iterrows():
        line = row['Line']
        color = line_colors.get(line, 'black')  # Default color if line not found
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=row['Station Name'],
            tooltip=f"{row['Station Name']} - {line}",
            icon=folium.Icon(color=color)
        ).add_to(delhi_map)

    # Display the Folium map in Streamlit
    folium_static(delhi_map)

# Analysis Section
if user_choice == "Perform Analysis":
    analysis_choice = st.sidebar.selectbox("Select Analysis Type", 
                                            ("Number of Stations Opened Each Year", 
                                             "Metro Line Analysis", 
                                             "Distribution of Station Layouts"))

    if analysis_choice == "Number of Stations Opened Each Year":
        st.subheader("Number of Stations Opened Each Year")
        stations_per_year = metro_data['Opening Year'].value_counts().sort_index()
        stations_per_year_df = stations_per_year.reset_index()
        stations_per_year_df.columns = ['Year', 'Number of Stations']

        fig1 = px.bar(stations_per_year_df, x='Year', y='Number of Stations',
                      title="Number of Metro Stations Opened Each Year in Delhi",
                      labels={'Year': 'Year', 'Number of Stations': 'Number of Stations Opened'})
        fig1.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig1)

    elif analysis_choice == "Metro Line Analysis":
        st.subheader("Metro Line Analysis")

        stations_per_line = metro_data['Line'].value_counts()
        total_distance_per_line = metro_data.groupby('Line')['Distance from Start (km)'].max()
        avg_distance_per_line = total_distance_per_line / (stations_per_line - 1)

        line_analysis = pd.DataFrame({
            'Line': stations_per_line.index,
            'Number of Stations': stations_per_line.values,
            'Average Distance Between Stations (km)': avg_distance_per_line
        }).sort_values(by='Number of Stations', ascending=False)

        fig2 = make_subplots(rows=1, cols=2, subplot_titles=(
            'Number of Stations Per Metro Line', 'Average Distance Between Stations Per Metro Line'))

        # Plot for Number of Stations per Line
        fig2.add_trace(go.Bar(y=line_analysis['Line'], x=line_analysis['Number of Stations'],
                              orientation='h', name='Number of Stations', marker_color='crimson'), row=1, col=1)

        # Plot for Average Distance Between Stations
        fig2.add_trace(go.Bar(y=line_analysis['Line'], x=line_analysis['Average Distance Between Stations (km)'],
                              orientation='h', name='Average Distance (km)', marker_color='navy'), row=1, col=2)

        # Update axes and layout
        fig2.update_xaxes(title_text="Number of Stations", row=1, col=1)
        fig2.update_xaxes(title_text="Average Distance Between Stations (km)", row=1, col=2)
        fig2.update_yaxes(title_text="Metro Line", row=1, col=1)
        fig2.update_layout(height=600, width=1200, title_text="Metro Line Analysis", template="plotly_white")

        st.plotly_chart(fig2)

    elif analysis_choice == "Distribution of Station Layouts":
        st.subheader("Distribution of Station Layouts")
        layout_counts = metro_data['Station Layout'].value_counts()

        fig3 = px.bar(x=layout_counts.index, y=layout_counts.values,
                      labels={'x': 'Station Layout', 'y': 'Number of Stations'},
                      title='Distribution of Delhi Metro Station Layouts',
                      color=layout_counts.index,
                      color_continuous_scale='pastel')

        fig3.update_layout(xaxis_title="Station Layout", yaxis_title="Number of Stations", coloraxis_showscale=False)
        st.plotly_chart(fig3)

# Coming Soon Section
st.subheader("Coming Soon")
st.write("We are working on adding more features to enhance your experience. Stay tuned for:")
st.write("- Real-time metro status updates")
st.write("- Station-wise fare calculator")
st.write("- User feedback and ratings on stations")
st.write("- More detailed analysis on line efficiency and delays")


# Delhi Metro Distance Checker

This is a simple Streamlit app that allows users to check the distance between two Delhi Metro stations using their latitude and longitude coordinates. The app also displays additional data and a map of metro stations.

## Features

1. **Check Distance Between Metro Stations**:
    - Users can select two metro stations from a dropdown and calculate the distance between them using the Haversine formula.
    - The result is displayed as the distance in kilometers.
2. **Check Fare Between Metro Stations**:
    - Users can select two metro stations from a dropdown and calculate the fare between them using certain pre-defined fares.
    - The result is displayed as the fare in INR.

2. **View Metro Data**:
    - Users can see the raw metro data, including information such as the station name, line, latitude, longitude, and opening date.
    - The app displays missing values and data types for the metro data.
    
3. **Visualize Metro Stations on a Map**:
    - The app provides an option to visualize all metro stations on an interactive map using Streamlit’s `st.map` feature.

## Installation and Usage

### Prerequisites
- Python 3.7 or above
- The following Python libraries:
  - `streamlit`
  - `pandas`
  - `math`
  - `folium`
  - `strealit_folium`

### Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/delhi-metro-distance-checker.git
    cd delhi-metro-distance-checker
    ```

2. **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Place the dataset**:
    - Ensure the `Metro_data.csv` file is located in the root of the project directory. The dataset should include columns such as `Station Name`, `Latitude`, `Longitude`, `Opening Date`, etc.

5. **Run the app**:
    ```bash
    streamlit run app.py
    ```

6. **Access the app**:
    - After running the above command, you can access the app at `http://localhost:8508/` in your browser.

### Usage

- Select the **first metro station** and **second metro station** from the dropdown lists on the app's main page.
- If both stations are different, the app will calculate and display the distance between them.
- Explore other options like viewing raw data, analyzing missing values, and visualizing metro stations on a map.

## Dataset

The `Metro_data.csv` file should contain the following columns:
- `Station Name`: Name of the metro station.
- `Latitude`: Latitude of the station.
- `Longitude`: Longitude of the station.
- `Opening Date`: Date the station was opened.
- `Line`: The metro line the station belongs to.




## Contributing

Contributions are welcome! If you'd like to improve the app or add new features, feel free to fork the repository and submit a pull request.



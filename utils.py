import matplotlib.pyplot as plt
import requests
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import shape, Point
import time

def get_ISRIC_results(polygon, grid_res=0.0025):
    # Calculate bounds of polygon
    min_x, min_y, max_x, max_y = polygon.bounds

    # Calculate number of grid points within polygon
    grid_points = []
    for x in np.arange(min_x, max_x, grid_res):
        for y in np.arange(min_y, max_y, grid_res):
            point = Point(x, y)
            if polygon.contains(point):
                grid_points.append((x, y))

    # Call ISRIC API for each grid point
    url = f'https://isqaper.isric.org/isqaper-rest/api/1.0/query'
    results = []
    for point in grid_points:
        lon, lat = point
        params = {
            "lon": lon,
            "lat": lat
        }
        response = requests.get(url, params=params)
        results.append(response.json())
    
    return results

def extract_data(results):
    # List to hold the extracted properties from each dictionary
    data = {'longitude': [], 'latitude': [], 'water_capacity': [], 'ph': [],'oc_content': [],
                                       'silt_content': [], 'sand_content': [], 'clay_content': []}

    # Loop over each dictionary in the results and extract the relevant properties
    for result in results:
        # get the coordinates
        coor = result['features'][0]['geometry']['coordinates']
        data['longitude'].append(coor[0])
        data['latitude'].append(coor[1])

        prop = result['features'][0]['properties']['properties']
        # Extract the values for each property
        data['water_capacity'].append(prop['AWCh1_M_sl1_250m_ll_pF2.3_0-30cm.tif']['value'])
        data['ph'].append(prop['PHIHOX_M_sl1_250m_ll_by10_0-30cm.tif']['value'])
        data['oc_content'].append(prop['ORCDRC_M_sl1_250m_ll_0-30cm.tif']['value'])
        data['silt_content'].append(prop['SLTPPT_M_sl1_250m_ll_0-30cm.tif']['value'])
        data['sand_content'].append(prop['SNDPPT_M_sl1_250m_ll_0-30cm.tif']['value'])
        data['clay_content'].append(prop['CLYPPT_M_sl1_250m_ll_0-30cm.tif']['value'])

    # Create the DataFrame from the data list
    df = pd.DataFrame(data)
    
    return df


def plot_geodataframe(gdf, gdf_data,column, cmap='OrRd'):
    fig, ax = plt.subplots(figsize=(13, 7))
    gdf.plot(ax=ax, alpha=0.5)
    gdf_data.plot(ax=ax, column=column, cmap=cmap, legend=True)

    # Set the title and labels for the plot
    ax.set_title(f"{column} Distribution", fontsize=20)
    ax.set_xlabel("Longitude", fontsize=14)
    ax.set_ylabel("Latitude", fontsize=14)

    # Set the background color of the plot
    ax.set_facecolor('#F2F2F2')

    plt.show()
    
 # Define the dictionary with the soil categories and their corresponding sand, clay, and silt content ranges
soil_categories = {
    'Sand': (85, 0, 0),
    'Loamy sand': (70, 10, 0),
    'Sandy loam': (50, 15, 85),
    'Sandy clay loam': (45, 20, 65),
    'Sandy clay': (45, 35, 0),
    'Clay': (0, 40, 0),
    'Clay loam': (20, 27, 60),
    'Loam': (23, 8, 28),
    'Silt clay loam': (0, 27, 60),
    'Silt loam': (15, 0, 50),
    'Silty clay': (0, 40, 40),
    'Silt' : (0, 0, 87)
}

# Convert soil_categories dictionary to a numpy array
soil_categories_arr = np.array(list(soil_categories.values()))

# Define a function to assign soil categories based on the sand, clay, and silt content
def assign_soil_category_numpy(row):
    # Create a numpy array of sand, clay, silt content for the given row    
    row_arr = np.array([row['sand_content'], row['clay_content'], row['silt_content']])
    
    # Use numpy broadcasting to perform element-wise comparison of the row array and soil_categories_arr
    comparison_arr = np.all(np.greater_equal(row_arr, soil_categories_arr), axis=1)
    # Find the index of the first True value in the comparison array
    idx = np.argmax(comparison_arr)
    
    # Return the soil category corresponding to the first True value in comparison_arr
    if True in comparison_arr:
        return list(soil_categories.keys())[idx]
    else:
        return None
    
# Define a function to assign soil categories based on the sand, clay, and silt content
def assign_soil_category_pandas(row):
    for category, (sand_min, clay_min, silt_min) in soil_categories.items():
        if row['sand_content'] >= sand_min and row['clay_content'] >= clay_min and row['silt_content'] >= silt_min:
            return category
    return None
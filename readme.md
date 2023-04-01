In this test, we explored the soil data provided by ISRIC, an organization that specializes in providing soil information worldwide. There are two versions of their API to retrieve soil data for a specified polygon. The first version didn't contain empty values, so it was the main solution used for our analysis.

I also noticed that the soil organic carbon stocks column wasn't available in the provided dataset, so I only considered the soil organic carbon content. 

### Questions 1& 2 & 3

#### Task : 
The task is to extract soil information for a specific area defined by a polygon from the ISRIC API. The area is divided into a grid of points, and the API is called for each point to extract certain properties. The results are then stored in a Pandas DataFrame.

#### Approach :

The code first loads a GeoJSON file, extracts the target polygon, and calculates its bounds. The next step is to create a grid of points within the polygon. This is done by iterating over a range of x and y values within the bounds of the polygon, and checking if each point is contained within the polygon using the contains method of the shapely.geometry.Polygon class. The grid points that are contained within the polygon are stored in a list.

The ISRIC API is then called for each grid point using the requests library, and the results are stored in a list. The code then extracts the values of each property for each grid point and stores them in a dictionary. Finally, the dictionary is used to create a Pandas DataFrame.
 

#### Assumptions

- The target polygon is a closed polygon with valid boundaries.
- The grid resolution is fixed at 0.0025 degrees (250m). This means that the density of grid points within the polygon may vary depending on the size and shape of the polygon.
- The ISRIC API provides the necessary properties for each grid point within the polygon.
- There is a one-to-one mapping between each grid point and its corresponding properties.

#### Possible Improvements
- The code could be improved by using a more sophisticated method for creating the grid of points within the polygon. For example, the points could be generated using a hexagonal grid or a Voronoi diagram to ensure a more uniform distribution of grid points within the polygon.
- The API calls could be parallelized using a library such as multiprocessing or concurrent.futures. This would allow multiple API calls to be made simultaneously, reducing the total runtime of the script.
- The code could be modified to handle errors and exceptions that may arise during the API calls, such as connection timeouts or HTTP errors.
- Additionally, it would be a good idea to handle cases where the 'results' list is empty or if the expected keys or values are missing. This would make the code more robust and prevent it from crashing or producing incorrect results in case of errors.
- It would be helpful to add a progress indicator to show the user the progress of the loop as it can take a while to complete for large datasets. A library such as tqdm could be used to add a progress bar to the loop.


### Questions 4

#### Task : 
Create a map and overlay one of the above parameters on the map (eg ph map or carbon stock map)

#### Approach
- The code first creates a GeoDataFrame from a pandas DataFrame by specifying the longitude and latitude columns as the x and y coordinates of the points.
- The GeoDataFrame is then plotted on a map using the plot method of the GeoDataFrame object.
- A column is selected to represent the soil parameter of interest and is passed to the column argument of the plot method. The colormap and legend are specified using the cmap and legend arguments, respectively.

#### Assumptions:
- The input data includes valid longitude and latitude values.
- The input data includes valid soil parameter values.
- The input data has already been preprocessed and cleaned.

#### Results :

Our analysis revealed that there is a negative correlation between pH and organic carbon content, and that the west region of the polygon generally has lower pH levels compared to the other regions. 

#### Possible Improvements:
- The code can be improved by adding additional parameters to the plot method to adjust the size and color of the points based on other variables or to add additional layers to the map.
- It would be good to provide interactivity to the map by using a library like Folium to allow users to zoom in and out, hover over points to see additional information, and toggle between different soil parameters or map layers.
- Additionally, the code could be modified to handle errors or exceptions that may arise during the visualization process, such as invalid input data or missing values.


### Questions 5

#### Task : 
Add a column to the dataframe with the category of the soil. This can be derived using the texture triangle with the sand, clay and soil content as inputs
#### Approach

- In the provided code, I defined a dictionary soil_categories which contains the soil categories and their corresponding sand, clay, and silt content ranges.

- The assign_soil_category_numpy() function uses NumPy broadcasting to compare the sand, clay, and silt content of a row with the content ranges in soil_categories_arr. It returns the soil category corresponding to the first True value in comparison_arr.

- The assign_soil_category_pandas() function uses a loop to compare the sand, clay, and silt content of a row with the content ranges in soil_categories. It returns the soil category if the row's sand, clay, and silt content are greater than or equal to the minimum values for a soil category.

- I then applied both assign_soil_category_numpy() and assign_soil_category_pandas() to create two new columns in the dataframe, soil_category_numpy and soil_category_pandas, respectively.

- To evaluate the performance of both functions, I recorded the execution time using the time module and printed it for both functions to compare their efficiency.

#### Possible Improvements
- The assign_soil_category_numpy function could be further optimized by using Numba or Cython to speed up the computation.
- The soil texture triangle method assumes that the sand, clay, and silt content are the only factors that determine soil texture. Other factors such as  soil structure, mineralogy, and organic matter content can also affect soil texture and should be taken into account.
- The accuracy of the soil texture triangle method can be affected by the accuracy of the measurements of sand, clay, and silt content. Careful sample collection and laboratory analysis are important to ensure accurate measurements.


### Questions 6

#### Task : 
The code generates a heatmap of soil pH values interpolated onto a regular grid of points.

#### Approach

The code defines the resolution of the regular grid and the boundaries of the area to be gridded. It then creates a regular grid of points using NumPy's meshgrid function, and interpolates the soil pH values onto the grid using SciPy's griddata function with linear interpolation. Finally, it plots the interpolated data as a heatmap using Matplotlib's imshow function.

#### Assumptions:
- The input soil pH data is representative of the entire area of interest.
- Linear interpolation is an appropriate method for interpolating the soil pH values.
- The chosen grid resolution is appropriate for the size of the area of interest and the density of the input data.

#### Possible Improvements:

- Using other interpolation methods, such as nearest neighbor or cubic, to see if they produce better results.
- Experimenting with different grid resolutions to find the optimal balance between resolution and computation time.
- Considering a measure of uncertainty or error in the interpolated data.

## Conclusion :

In this project, we explored the soil data for a specific polygon using the ISRIC API. We extracted various properties such as soil pH, soil organic carbon content, sand content, silt content, and clay content using the API. We then performed exploratory data analysis (EDA) on the extracted data to understand the distribution of the properties across the polygon.

Our analysis revealed that the soil pH across the polygon was mostly in the range of 7.2 to 7.8, indicating that the soil was moderately acidic to slightly alkaline. However, we also observed low pH values in the western region of the polygon. The organic carbon content was negatively correlated with pH, suggesting that the soil with high pH has low organic carbon content. 

To visualize the distribution of the soil properties, we plotted a heatmap using the longitude and latitude coordinates of the polygon. The heatmap showed the distribution of soil pH across the polygon, with the low pH values being more pronounced in the western region.

Overall, this project gave us insights into the soil properties of the polygon and how they are distributed. One of the limitations of this project is that we used only a single polygon, and the findings may not be generalizable to other regions. However, this project can be extended by analyzing soil data for multiple polygons and comparing their properties. Additionally, more advanced machine learning techniques can be applied to the soil data to predict properties such as soil fertility, crop yield, and nutrient content.


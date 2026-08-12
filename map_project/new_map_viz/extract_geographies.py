# this is meant to extract the geographies from the shapefile and save them as a geojson file
# this is only fron a .zi pfile though 

# most likely if running this on windows, can connect to arcGIS probs

# click cmd + shift + p and select "Python: Select Interpreter" and select the one with the venv in it
# i.e. CC in this case 

import shutil
import zipfile 
import json 
import geopandas as gpd
import shutil
import os


def extract_files(zip_data_path, extracted_path):
    print('Current working directory:', os.getcwd())
    
    with zipfile.ZipFile(zip_data_path, 'r') as zip_ref:
        zip_ref.extractall(extracted_path)
    print("Files extracted successfully.")
        
def extract_geographies(zip_data_path, extracted_path, folder_name):
    # function to extract the geographies from the shapefile and save them as a geojson file
    # this is only from a .zip file though 
    
    
    # extracting the files from the zip file
    extract_files(zip_data_path, extracted_path)
    
    # loading the shapefile
    shapefile_name = extracted_path + folder_name + '/' + folder_name + '.shp'
    myshpfile = gpd.read_file(shapefile_name)
    
    print("Geojson file created successfully.")
    return myshpfile


def clean_gdf(gdf):
    gdf.rename(columns={'STCD': 'DC', 'STAB': 'State'}, inplace=True)
    gdf_new = gdf[['CCN20', 'DC', 'State', 'geometry']]
    return gdf_new

def create_dict(gdf_new):
    # function to create a dictionary with the congressional community number as 
    # the key and the congressional district and state as the values
    
    ccn20_str_dict = gdf_new[['CCN20', 'DC', 'State']].groupby('CCN20').apply(
    lambda g:g.to_dict(orient='records')
        ).to_dict()
    return ccn20_str_dict

def save_geo_dict(file_path, gdf_new, ccn20_str_dict):
    gdf_indexed = gdf_new.set_index('CCN20')

    gdf_data = {}

    for ccn20_number in set(gdf_new.CCN20):
        ccn20_record = ccn20_str_dict[ccn20_number][0]
        gdf_row = gdf_indexed.loc[ccn20_number]

        gdf_data[str(ccn20_number)] = {
            "DC": ccn20_record['DC'],
            "State": ccn20_record['State'],
            "geometry": gdf_row['geometry'].__geo_interface__  # Convert geometry to GeoJSON format
        }
        
    with open(file_path, 'w') as f:
        json.dump(gdf_data, f)
        
    print("Geojson dictionary saved successfully to {}".format(file_path))
        
def delete_extra_files(extracted_path):
    shutil.rmtree(extracted_path)
    print("Extra files deleted successfully from {}".format(extracted_path))
    
if __name__ == '__main__':
    # setting the working directory to the root of the project
    cwd = os.getcwd()
    print(cwd)
    os.chdir('/Users/camillebergeron/Documents/GitHub/congressional_communities')
    print("Changed working directory to:", os.getcwd())
    
    # setting file paths
    zip_data_path = "./data/cc20_us_03102025_500k-20260811T170554Z-1-001.zip"
    extracted_path = './data/extracted_files/'
    folder_name = 'cc20_us_03102025_500k'
    save_file_path = './map_project/new_map_viz/data/ccn20_geo_dict.json'
    
    # calling functions 
    gdf = extract_geographies(zip_data_path, extracted_path, folder_name)
    gdf_new = clean_gdf(gdf)
    ccn20_str_dict = create_dict(gdf_new)
    save_geo_dict(save_file_path, gdf_new, ccn20_str_dict)
    delete_extra_files(extracted_path)

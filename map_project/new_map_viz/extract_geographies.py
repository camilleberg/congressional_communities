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
    # function to save the geojson dictionary to a file
    
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
    
def detect_size(file_path):
    # function to detect the size of a file in MB
    
    size = os.path.getsize(file_path) / (1024 * 1024)
    return size

def split_json_file(file_path, max_size_mb=100):
    # function to split a json file into smaller files if it exceeds a certain size
    # max_size_mb is the maximum size of each file in MB
    
    size = detect_size(file_path)
    
    if size <= max_size_mb:
        print("File size is within the limit. No need to split.")
        return [file_path]
    
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    subfiles = []
    current_subfile = {}
    current_size = 0
    subfile_index = 1
    
    for key, value in data.items():
        current_subfile[key] = value
        current_size += len(json.dumps({key: value}).encode('utf-8')) / (1024 * 1024)  # Size in MB
        
        if current_size >= max_size_mb:
            subfiles.append(current_subfile)
            current_subfile = {}
            current_size = 0
            subfile_index += 1
    
    if current_subfile:
        subfiles.append(current_subfile)
    
    print(f"File split into {len(subfiles)} parts.")
    return subfiles

def save_split_json_files(subfiles):
    subfile_names = []
    for i, sub_dict in enumerate(subfiles):
        subfile_name = f'./map_project/new_map_viz/data/ccn20_geo_dict_subfiles/ccn20_geo_dict_part_{i+1}.json'
        with open(subfile_name, 'w') as f:
            json.dump(sub_dict, f)
        subfile_names.append(subfile_name)
    
    print(f"Split files saved: {subfile_names}")
    return subfile_names
        
def delete_extra_files(extracted_path):
    shutil.rmtree(extracted_path)
    print("Extra files deleted successfully from {}".format(extracted_path))
    
def delete_file(file_path):
    os.remove(file_path)
    print("File deleted successfully: {}".format(file_path))
    
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
    
    # split the json file if it exceeds the size limit
    subfiles = split_json_file(save_file_path, max_size_mb=80)
    save_split_json_files(subfiles)
    delete_file(save_file_path)  # Delete the original large file after splitting

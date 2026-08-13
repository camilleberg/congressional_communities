# this is meant to extract the geographies from the shapefile and save them as a geojson file
# this is only fron a .zi pfile though 

# most likely if running this on windows, can connect to arcGIS probs

# click cmd + shift + p and select "Python: Select Interpreter" and select the one with the venv in it
# i.e. CC in this case 

import shutil
import zipfile
import json
import os
import sys
import geopandas as gpd
from shapely.geometry import mapping
from topojson import Topology


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
    gdf_clean = gdf[['CCN20', 'DC', 'State', 'geometry']]
    return gdf_clean


def convert_to_top(gdf_clean):
    gdf_topo = Topology(gdf_clean).to_json()
    print("geojson converted")
    return gdf_topo


def save_topo_json(gdf_topo, save_path):
    with open(save_path, "w") as f:
        f.write(gdf_topo)
    print("Topojson saved")


def detect_file_size_mb(file_path):
    # function to detect the size of a file on disk, in MB
    size_bytes = os.path.getsize(file_path)
    return size_bytes / (1024 * 1024)


def split_json_file(file_path, max_size_mb=100):
    # function to split a json file into smaller files if it exceeds a certain size
    # max_size_mb is the maximum size of each file in MB

    size = detect_file_size_mb(file_path)

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
    save_file_path = './map_project/new_map_viz/data/ccn20_geo_topo.json'

    # calling functions
    gdf = extract_geographies(zip_data_path, extracted_path, folder_name)
    gdf_clean = clean_gdf(gdf)
    gdf_topo = convert_to_top(gdf_clean)
    save_topo_json(gdf_topo, save_file_path)
    
    delete_extra_files(extracted_path)

    # split the json file if it exceeds the size limit
    # subfiles = split_json_file(save_file_path, max_size_mb=80)
    # save_split_json_files(subfiles)
    # delete_file(save_file_path)  # Delete the original large file after splitting
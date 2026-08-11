import pandas as pd
import re
import math 
import json 



def load_data():
    # function to load data
    df = pd.read_excel('../../data/cc20_us_02052025_website.xlsx')
    return df


def clean_data_age(df):
    # function that groups age data into three groups: under 18, 18-65, and over 65
    # returns a new dataframe with the three age groups and a list of the new columns
    
    df = df.copy()  # copying for safety 
    
    # assigning groups 
    df_new = df.assign(
        ageGroup_under18=lambda x: x['Total Population'] - x['18 years and over - Tot Pop'],
        ageGroup_18_65=lambda x: (
                x['18 years and over - Tot Pop'] - x['65 years and over  - Tot Pop']
            ),
        ageGroup_over65=lambda x: x['65 years and over  - Tot Pop'],
    )
    
    # getting the new columns
    age_bracket_cols= [col for col in df_new.columns if re.search(r'^ageGroup', col)]
    
    # creating a new dataframe with the relevant columns and only the rleevant columns
    df_age = df_new[['CCN20', 'DC', 'State', 'Total Population']].join(df_new[age_bracket_cols])

    return df_age, age_bracket_cols

def create_dict(df):
    # function to create a dictionary with the congressional community number as 
    # the key and the congressional district and state as the values
    
    ccn20_dict = df[['CCN20', 'DC', 'State']].groupby('CCN20').apply(
        lambda g:g.to_dict(orient='records')
    ).to_dict()
    return ccn20_dict


def group_function(df, group, age_bracket_cols):
    # function to group the dataframe by congressional community, congressional district, 
    # or state and return a nested dictionary with the age groups and total population
    
    # aggregating bases on cc, congressional, dist 
    age_groups = age_bracket_cols + ['Total Population']
    nested_dict = df.groupby(group)[age_groups].sum().to_dict(orient='index')
    return nested_dict

def group_data(df_age, age_bracket_cols):
    # function to group the dataframe by congressional community, congressional district,
    # or state and return a nested dictionary with the age groups and total population
    # returns a dcitionary with the congressional 
    # community number as the key and the congressional district and state as the values
    
    df_state_graph = group_function(df_age, 'State', age_bracket_cols)
    df_cd_graph = group_function(df_age, 'DC', age_bracket_cols)

    return df_state_graph, df_cd_graph

def prep_dict(df_age, cc_number): 
    # function to prepare a dictionary with the age data for a specific congressional community number
    
    new_df = df_age.loc[df_age['CCN20'] == cc_number].drop(columns=['CCN20','DC', 'State']).to_dict(orient = 'records')
    return new_df[0]

def exclude_key(d, key):
    d = d.copy()
    d.pop(key, None)
    return d
    

# function to save age data for each congressional community, congressional district, and state
def save_age_data(df_age, age_bracket_cols, ccn20_dict, df_cd_graph, df_state_graph): 
    df_age_indexed = df_age.set_index('CCN20')

    age_cc_data = {}

    for ccn20_number in set(df_age.CCN20):
        ccn20_record = ccn20_dict[ccn20_number][0]
        cc_row = df_age_indexed.loc[ccn20_number]

        age_cc_data[str(ccn20_number)] = {
            "age_brackets": age_bracket_cols,
            "cc": {col: int(cc_row[col]) for col in age_bracket_cols},
            "cc_total": int(cc_row['Total Population']),
            "cd": {col: int(df_cd_graph[ccn20_record['DC']][col]) for col in age_bracket_cols},
            "cd_total": int(df_cd_graph[ccn20_record['DC']]['Total Population']),
            "state": {col: int(df_state_graph[ccn20_record['State']][col]) for col in age_bracket_cols},
            "state_total": int(df_state_graph[ccn20_record['State']]['Total Population']),
        }

    with open('./data/age_cc_data.json', 'w') as f:
        json.dump(age_cc_data, f)
        
if __name__ == '__main__':
    df = load_data()
    print("Data loaded successfully.")
    df_age, age_bracket_cols = clean_data_age(df)
    print("Data cleaned successfully.")
    ccn20_dict = create_dict(df)
    print("Dictionary created successfully.")
    df_state_graph, df_cd_graph = group_data(df_age, age_bracket_cols)
    print("Data grouped successfully.")
    save_age_data(df_age, age_bracket_cols, ccn20_dict, df_cd_graph, df_state_graph)
    print("Age data saved successfully.")
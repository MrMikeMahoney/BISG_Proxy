# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 20:58:27 2018

@author: Mike
This attempts to recreate the BISG proxy >> probability of an ethnicity based on census tract and last name occurance

## This runs data created in bsig_synthetic_ln_creator.py >> and uses two functions:
##      bisg_match >> to match the statistics based on the chosen last name and census tract
##      bisg_probability >> runs a probability calculation yielding a statistic for each ethnicity
## It then appends the results to a list to put into the orginal dataframe
## Then it checks if the predicted columns are equal to the actual value and gives a right/wrong score
"""

import pandas as pd
from time import time
import numpy as np

## Reads the csv to create census_tracts and last_names
#census_tract_df = pd.read_csv("C:/Users/Mike/Documents/Conda Scripts/Created Datasets/census_synthetic_data.csv")
census_tract_df = pd.read_csv("C:/Users/Mike/Documents/Data_Science_Data_Sets/ACS_17_5YR_DP05_with_ann.csv")
last_name_df = pd.read_csv("C:/Users/Mike/Downloads/names/Names_2010Census.csv")

## Reads the csv of the synthetic last names, ethnicity and census tracts
synth_ln = pd.read_csv("C:/Users/Mike/Documents/Conda Scripts/Created Datasets/last_name_eth_synthetic_data.csv", index_col=False)

## The list that contains the 6 races to predict >> race_6
race_6 = ["white", "black", "api", "native_american", "two or more", "hispanic"]

## Creating the bisg proxy matchvfunction
def bisg_match(last_name, census_tract):
    ## Gets the row from last_name_df >> from last_name
    last_name = last_name.upper()  ## Converts last_name to UPPERCASE
    #surname = last_name_df.loc[last_name_df['name'] == last_name] # Finds the input last_name in the last_name_df
    ## Finds the finds the last name imput in the function and returns a one row data frame from last_name_df of corresponding match
    surname = last_name_df.loc[last_name_df.name == last_name]
    ## Slices the surname to get only the 6 rows we care about
    surname = surname.iloc[:,5:11]
    ## Returns the data frame values to a list
    surname_list = surname.values.tolist()[0]
    ## Converts the data to numeric >> Census had GENERAL format >> A short loop
    surname_final = []
    for race_prob in surname_list:
        if race_prob != '(S)': # If race_prob is not a string >> Then converting to a percent
            probability = round(float(race_prob),4)/100 # Sets that porbability to scale of 1
        else: # If it is a sting >> prob becomes 0
            probability = 0.0000
        surname_final.append(float(probability))
    #return surname
    ## Gets the row from census_tract_df
    ct = census_tract_df.loc[census_tract_df.CT_Full_Name == census_tract]
    ct = ct.iloc[:,2:8]
    ct_list = ct.values.tolist()[0]
    ct_list_final = []
    ## A short loop to change the itmes in a list to a float
    for race_prob in ct_list:
        if race_prob != '-': # If race_prob is not a string >> Then converting to a percent
            probability = round(float(race_prob),4)/100 # Sets that porbability to scale of 1
        else: # If it is a sting >> prob becomes 0
            probability = 0.0000
        ct_list_final.append(float(probability))
    #most_likely = max(surname)
    return surname_final, ct_list_final
    #return ct
    #return most_likely

## Creating bisg probability >> takes probabillity row >> which is two tuples packed together. They each line up to the same race
def bisg_probability(prob_row):
    race_prob_list = [] # Empty ist
    for race in range(len(race_6)): # Iterating through the race_6 or six races
        # Using the race index to loop through each race and figure out the prob for each race
        try: # Avoiding ZeroDivisionError
            output  = (float(prob_row[0][race] * prob_row[1][race]) / (float(prob_row[0][0] * prob_row[1][0]) + (prob_row[0][1] * prob_row[1][1]) +
                (prob_row[0][2] * prob_row[1][2]) + (prob_row[0][3] * prob_row[1][3]) + (prob_row[0][4] * prob_row[1][4]) +
                (prob_row[0][5] * prob_row[1][5])))*100
        except ZeroDivisionError: # A few of our probabilities are zero >> avoids this
                output = 0.0
        race_prob_list.append(output)   
    return race_prob_list


t0 = time() # Start the timer for the loop
## Creating a loop to iterate over all data in synth_ln and apply >> functions: bisg_match & bisg_probability
proxy_results_list = []
for last_name in range(len(synth_ln)):
    last_name_ct = synth_ln.iloc[last_name,1] # Gets the selected census tract for the last name
    last_name_selected = synth_ln.iloc[last_name,0] # Gets the selected last name based on index position in the loop
    find_stats = bisg_match(last_name_selected, last_name_ct) # Saves the results from the bisg_match function
    proxy_guess = bisg_probability(find_stats) # Saves the probabilities from bisg_probability
    proxy_pick = proxy_guess.index(max(proxy_guess)) # Gets the index of the highest probability
    proxy_results = race_6[proxy_pick] # Selects the race based on the index of proxy_pick
    proxy_results_list.append(proxy_results)
    
t1 = time() # Endind timer for loop
print("It took: ", round(t1-t0,2), "seconds to run the BSIG Proxy")

#### Adding pred_race column to synth_ln df >> from proxy_results_list >> check our work
synth_ln["pred_race"] = proxy_results_list
## Checking if the ethnicity and pred_race are equal
synth_ln["check_proxy"] = np.where(synth_ln["pred_race"] == synth_ln["ethnicity"],"Correct", "Wrong")
## Check our accuracy of correct vs wrong for BSIG Proxy
synth_ln["check_proxy"].value_counts()/1000
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 15:53:05 2019

@author: Mike
This attempts to recreate the BISG proxy >> probability of an ethnicity based on census tract and last name occurance

## This creates the synthetic data for last names from the US Census
## It takes the last name and the probabilities of each of the 6 races and assigns a race
## This is then used for the bsig_proxy to predict what the ethnicity is for a particular last name
## A census tract (from Texas) is randomly assigned to the last name and creates the dataset >>
## last_name_eth_synthetic_data.csv

#### Note: Only Texas is used for this synthetic data
"""

#import random
from time import time
from numpy.random import choice
import pandas as pd

###### Creating a synthetic list of ehtnicities based on last name >> to train and test the model >> GOOD STUFF!
## Opening the last names df >> with the probabilities of ethnicity for US census surnames
last_name_df = pd.read_csv("C:/Users/Mike/Downloads/names/Names_2010Census.csv")
census_tract_df = pd.read_csv("C:/Users/Mike/Documents/Data_Science_Data_Sets/ACS_17_5YR_DP05_with_ann.csv")

## The list that contains the 6 races to predict >> race_6
race_6 = ["white", "black", "api", "native_american", "two or more", "hispanic"]


## Getting ln_list >> list of last names to use
total_ln = last_name_df.iloc[:,0].tolist()
ln_list = choice(total_ln, 1000).tolist()

## Getting ct_list >> list of census tracts to use
ct_list = census_tract_df.iloc[:,8].tolist()
location_ct = choice(ct_list, 1000)

t0 = time() # Start the timer for the loop

## Writing the file to csv
file_name = "C:/Users/Mike/Documents/Conda Scripts/Created Datasets/last_name_eth_synthetic_data.csv"
f=open(file_name, "w")
headers="last_name,census_tract,ethnicity\n"
f.write(headers)

## Sythentic list of last names >> with census tracts in Texas
sum_s = 0.0 # Resets the sum to zero >> just in case
for last_name in range(len(ln_list)): # Loops through the names in the ln_list
    chosen_last_name = ln_list[last_name] # A palceholder for the chosen last name
    ln_var = last_name_df.loc[last_name_df.name == chosen_last_name] # Finds the 6 race statistics for the last name in the loop
    name_slice = ln_var.iloc[0,5:11].tolist() # Takes name stats and converts to list
    #print(name_slice)
    sum_s = 0.0
    name_probability = [] # Empty names_probability list
    for prob in name_slice:
        ## Statement to catch if prob is a str() 
        if prob != '(S)': # If prob is not a string >> Then converting to a percent
            probability= round(float(prob),4)/100 # Sets that porbability to scale of 1
        else: # If it is a sting >> prob becomes 0
            probability = 0.0000
        sum_s = sum_s + float(probability) # Running sum of th probabilities for that name
        #name_slice[prob]
        name_probability.append(probability) # Appends to the names_probability list
        normalized_probabilities = [] #Creating a list to hold the normalized probabilites
    ## Normalizing each probability >> to get an anwser equal to 1
    for p in range(len(name_probability)):
        norm_prob = name_probability[p]/sum_s # Dividing the probability by the sum of all the probabilities
        normalized_probabilities.append(norm_prob)
    census_tract_for_name = str(location_ct[last_name]) # Getting a census tract based on position in master loop
    ethnicity_name_generator = choice(race_6, 1, p = (normalized_probabilities)) # Makes a descion on race based on last name stats
    ethnicity_name_generator_var = str(ethnicity_name_generator) # Converts the decsion to a string
    ethnicity_name_generator_var = ethnicity_name_generator_var.strip("[]''") # Removing excess characters
    f.write(chosen_last_name+","+census_tract_for_name+","+ethnicity_name_generator_var+","+"\n") # Writing to file
f.close()
#print(name_slice)
#print(name_probability)


t1 = time() # Endind timer for loop
print("It took: ", round(t1-t0,2), "seconds to create 1000 fake people")

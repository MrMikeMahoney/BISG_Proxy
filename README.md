# BISG_Proxy
Recreates the BISG Proxy (Bayesian Improved Surname Geocoding) in Python. 
Using data from the US Census (American Community Survey) on Surnames and Census Tracts, it runs a probability that a given surname is one of 
6 possible races/ethnicities >> race_6 = ["white", "black", "api", "native_american", "two or more", "hispanic"]

I only used data from 5265 Texas Census Tracts, and used the 162254 Last Names provided by the 2010 US Census.  Due to the inability to find a real datasets of people (or loan applications) of last names and their races; I had to create synthetic data (using bisg_synthetic_ln_creator.py) to assign 

There are 5 files used in this proxy:
  1) Names_2010Census.csv
  2) ACS_17_5YR_DP05_with_ann.csv
  3) bisg_synthetic_ln_creator.py
  4) last_name_eth_synthetic_data
  5) bisg_proxy_first.py

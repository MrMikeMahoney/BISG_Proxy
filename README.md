# BISG_Proxy
Recreates the BISG Proxy (Bayesian Improved Surname Geocoding) in Python. The BISG Proxy is commonly used in banking to comply with Fair Lending, because it is illegal to ask commerical loan applicants demographic data, but the bank is still required to comply with the Fair Lending Laws despite not knowing the race of the applicant.
Using data from the US Census (American Community Survey) on Surnames and Census Tracts, the main script (bisg_proxy_final.py) runs a probability that a given surname is one of 
6 possible races/ethnicities >> race_6 = ["white", "black", "api", "native_american", "two or more", "hispanic"]

I only used data from 5265 Texas Census Tracts, and used the 162254 Last Names provided by the 2010 US Census.  Due to the inability to find a real datasets of people (or loan applications) of last names and their races; I had to create synthetic data (using bisg_synthetic_ln_creator.py) to assign 

There are 5 files used in this proxy:
  1) Names_2010Census.csv
  2) ACS_17_5YR_DP05_with_ann.csv
  3) bisg_synthetic_ln_creator.py
  4) last_name_eth_synthetic_data.csv
  5) bisg_proxy_final.py
  
  Note: bisg_synthetic_ln_creator.py >> is only used to generate synthetic data.  It assigns a race to a last name, based on the probabilities of each race occurring in that last name.  Due to this script generating a last name, it is not based on actual data.  This script also randomly assigns a Texas Census tract to each last name. 'last_name_eth_synthetic_data.csv' is the output of this script
  
  To accurately generate the BISG proxy, one should run the 'bisg_synthetic_ln_creator.py' and recieve the output 'last_name_eth_synthetic_data.csv' >> then run 'bisg_proxy_final.py' using 'last_name_eth_synthetic_data.csv'.
  
  Thank you for reading, I hope you enjoy.

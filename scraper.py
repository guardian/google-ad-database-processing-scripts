import requests
import pandas as pd
import zipfile
import os
import shutil
import scraperwiki
from datetime import date, datetime

# https://storage.googleapis.com/transparencyreport/google-political-ads-transparency-bundle.zip
#%%
# Remove ad folder if it already exists
path = "google-political-ads-transparency-bundle"

if os.path.exists(path):
	shutil.rmtree(path)
	
#%%

# Get the actual ad zip

print("Downloading the ad file")

# r = requests.get("https://storage.googleapis.com/transparencyreport/google-political-ads-transparency-bundle.zip")

# with open(f"{path}.zip", "wb") as file:
# 	file.write(r.content)

#%%

# unzip the folder

with zipfile.ZipFile(f"{path}.zip", 'r') as zip_ref:
    zip_ref.extractall(".")	

#%%

# Get only Australian ads

print("Getting the Australian ads")

df = pd.read_csv("google-political-ads-transparency-bundle/google-political-ads-creative-stats.csv")

aus = df[df['Regions'] == "AU"]

#%%

# Get rid of columns we don't want

cols = list(aus.columns)

remove_cols = ['Spend_Range_Min_EUR','Spend_Range_Max_EUR','Spend_Range_Min_INR','Spend_Range_Max_INR','Spend_Range_Min_BGN','Spend_Range_Max_BGN','Spend_Range_Min_HRK','Spend_Range_Max_HRK','Spend_Range_Min_CZK','Spend_Range_Max_CZK','Spend_Range_Min_DKK','Spend_Range_Max_DKK','Spend_Range_Min_HUF','Spend_Range_Max_HUF','Spend_Range_Min_PLN','Spend_Range_Max_PLN','Spend_Range_Min_RON','Spend_Range_Max_RON','Spend_Range_Min_SEK','Spend_Range_Max_SEK','Spend_Range_Min_GBP','Spend_Range_Max_GBP','Spend_Range_Min_ILS','Spend_Range_Max_ILS','Spend_Range_Min_NZD','Spend_Range_Max_NZD','Spend_Range_Min_TWD','Spend_Range_Max_TWD']

new_cols = [x for x in cols if x not in remove_cols]

aus = aus[new_cols]

#%%

# Save the ads into sqlite db

print("Saving the ads")

aus_dict = aus.to_dict(orient='records')

scraperwiki.sqlite.save(unique_keys=["Ad_ID"], data=aus_dict, table_name="aus_ads")

# Backup today's ads with a timestamp
#%%

# Archive each day's scrape somewhere

# todaysDate = date.strftime(datetime.now(), "%Y-%m-%d")

# if os.path.exists("adfiles"):
# 	aus.to_csv(f"adfiles/{todaysDate}.csv")

# else:
# 	os.mkdir("adfiles")
# 	aus.to_csv(f"adfiles/{todaysDate}.csv")




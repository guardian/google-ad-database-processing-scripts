# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 13:09:12 2022

@author: everall
"""
import scraperwiki
import sqlite3
import cv2
import pandas as pd
import os
import pytesseract
import time
import simplejson as json
from PIL import Image
#import urllib2
import requests
from  bs4 import BeautifulSoup


os.chdir("C:\Users\everall\Documents\Python\Projects\google-ad-database-processing-scripts")

con = sqlite3.connect("scraperwiki.sqlite")

cur = con.cursor()
df = pd.read_sql_query("SELECT * FROM aus_ads", con)

ip.downloadImage("https://tpc.googlesyndication.com/sadbundle/$csp%3Der3$/3760334257784916408/index.html")

r = requests.get("https://tpc.googlesyndication.com/sadbundle/$csp%3Der3$/3760334257784916408/index.html")
page = BeautifulSoup(r.content)
page.findAll("localUrl")






https://transparencyreport.google.com/political-ads/advertiser/AR146135025295818752/creative/CR118339371345641472









ip.getImage("https://transparencyreport.google.com/political-ads/advertiser/AR146135025295818752/creative/CR118339371345641472")
ip.getImage("https://transparencyreport.google.com/political-ads/library/advertiser/AR133579976896151552/creative/CR208733795677896704")

ad_url = "https://transparencyreport.google.com/political-ads/advertiser/AR146135025295818752/creative/CR118339371345641472"

# url_split = ad_url.split("/")
#     #can just introduce regex to find index
# 	ar_id = url_split[6]
# 	cr_id = url_split[8]
# 	# print(ar_id, cr_id)
# 	ad_api_url = f"https://transparencyreport.google.com/transparencyreport/api/v3/politicalads/creatives/details?entity_id={ar_id}&creative_id={cr_id}&hl=en"
# 	print(ad_api_url)
# 	ad_results = requests.get(ad_api_url)
# 	results_text = ad_results.text.replace(")]}'","").strip()
# 	ad_results_json = json.loads(results_text)

def get_HTML(ad_url):
   url_split = ad_url.split("/")
   ar_id = url_split[5]
   cr_id = url_split[7]
	# print(ar_id, cr_id)
   ad_api_url = f"https://transparencyreport.google.com/transparencyreport/api/v3/politicalads/creatives/details?entity_id={ar_id}&creative_id={cr_id}&hl=en"
   ad_results = requests.get(ad_api_url)
   results_text = ad_results.text.replace(")]}'","").strip()
   ad_results_json = json.loads(results_text)
   
   return ad_results_json

ad_results_json = get_HTML(ad_url)
results[0][3][4][3][3]
ad_url = ad_results_json[0][3][4][3][3]
print(ad_url)
ad_js = requests.get(ad_url).content
page = BeautifulSoup(ad_js)
page.findAll("img")














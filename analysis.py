#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import youtube_transcript_api
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import requests
import simplejson as json
from collections import Counter

# Google data contains the postcode 4803 for Hamilton Island which is not in the most recent version 
# of the ASGS POA file, so possibly they're using an older one

#%%
formatter = TextFormatter()

df = pd.read_csv("google-political-ads-transparency-bundle/google-political-ads-creative-stats.csv")

#%%

aus = df[df['Regions'] == "AU"]
aus = aus[aus['Last_Served_Timestamp'] >= "2021-07-01"]
advertisers = list(aus['Advertiser_Name'].unique())

#%%
aus_cols = list(aus.columns)

#%%

excludes = ["Western Australia", "South Australia", "New South Wales", "Northern Territory", "Tasmania", "Victoria", "Queensland", "Australian Capital Territory", "Australia"]

with open('poa-to-ced.json') as json_file:
    postcodes = json.load(json_file)

def convertElec(row):
	if row['Geo_Targeting_Included'] == "Northern Territory":
		return ['Lingiari', 'Solomon']
	else:
		row_str = row['Geo_Targeting_Included']
		results = []
		for word in excludes:
			row_str = row_str.replace(word, "")
		
		row_str = row_str.replace(" ", "")
		
		row_list = row_str.split(",")
		row_list = [i for i in row_list if i]
		for row_pc in row_list:
			if row_pc in postcodes:
				elec_list = postcodes[row_pc]
				elec_list = [i for i in elec_list if i['overlap'] >= 50]
				
	# 			print(row_pc)
	# 			print(elec_list)
				for elec in elec_list:	
					results.append(elec['electorate'])
			else:
				pass
		count = Counter(results)
		print(count)
		if len(count) > 1:
			new_count = Counter({k: c for k, c in count.items() if c >= 3})
			new_list = list(new_count.keys())
		else:
			new_list = list(count.keys())
		
		print(new_list)		
		return list(set(new_list))	
# 	print(results)

# https://stackoverflow.com/questions/39011511/pandas-expand-rows-from-list-data-available-in-column	

#%%

def convertPostcodes(row):
	row_str = row['Geo_Targeting_Included']
	results = []
	for word in excludes:
		row_str = row_str.replace(word, "")
	row_str = row_str.replace(" ", "")
	
	row_list = row_str.split(",")
	row_list = [i for i in row_list if i]

	return list(set(row_list))

	
#%%

# "47kBDwXtdFc"

def getTranscript(id):
	try:
		transcript = YouTubeTranscriptApi.get_transcript(id)
		text = formatter.format_transcript(transcript)
		return text
	except youtube_transcript_api.TranscriptsDisabled:
		print("Transcripts disabled")
		return None

#%%

r = requests.get("https://transparencyreport.google.com/political-ads/advertiser/AR133579976896151552/creative/CR199397842446450688")

print(r.text)

# https://transparencyreport.google.com/transparencyreport/api/v3/politicalads/creatives/details?entity_id=AR133579976896151552&creative_id=CR199397842446450688&hl=en


#%%

# https://transparencyreport.google.com/political-ads/library/advertiser/AR195639161946898432/creative/CR100078407353630720

def getVideoId(row):
	url_split = row['Ad_URL'].split("/")
	ar_id = url_split[6]
	cr_id = url_split[8]
	print(ar_id, cr_id)
	ad_results = requests.get(f"https://transparencyreport.google.com/transparencyreport/api/v3/politicalads/creatives/details?entity_id={ar_id}&creative_id={cr_id}&hl=en")
	results_text = ad_results.text.replace(")]}'","").strip()
	ad_results_json = json.loads(results_text)
	video_id = ad_results_json[0][3][0][0]
	return video_id
	

#%%

# Labor analysis

alp = aus[aus['Advertiser_Name'] == "Australian Labor Party National Secretariat"]
alp_vids = alp[alp['Ad_Type'] == "Video"]
alp_vids['video_id'] = alp_vids.apply(getVideoId, axis=1)

#%%
alp_vids.to_csv("alp-vids.csv")

#%%

unique_vids_list = list(alp_vids['video_id'].unique())
vids_transcript = {}
vids_titles = {}
for vid_id in unique_vids_list:
	transcript = getTranscript(vid_id)
	vids_transcript[vid_id] = transcript
	vid_info = requests.get(f"https://www.youtube.com/oembed?format=json&url=https://www.youtube.com/watch?v={vid_id}")
	vids_titles[vid_id] = vid_info.json()['title']				 
	
						 
#%%

medicare_ids = ['47kBDwXtdFc']


#%%

alp_vids['text'] = alp_vids['video_id'].map(vids_transcript)

#%%

alp_vids['titles'] = alp_vids['video_id'].map(vids_titles)

#%%

alp_vids['electorates'] = alp_vids.apply(convertElec, axis=1)

#%%

alp_vids['postcodes'] = alp_vids.apply(convertPostcodes, axis=1)

#%%

alp_postcodes = alp_vids[['postcodes','Ad_URL', 'titles', 'electorates','Date_Range_End','Spend_Range_Min_AUD', 'Spend_Range_Max_AUD']]

alp_postcodes = alp_postcodes.explode('postcodes')

alp_postcodes = alp_postcodes[pd.notnull(alp_postcodes['postcodes'])]
alp_postcodes['count'] = 1

alp_postcodes_count = alp_postcodes[['postcodes', 'count']].groupby(['postcodes']).count()

#%%

alp_mediscare = alp_vids[alp_vids['titles'] == "Exposing Scott Morrison’s plan to cut Medicare"][:2]

alp_mediscare = alp_mediscare[['Ad_URL', 'titles', 'electorates', 'Date_Range_End','Spend_Range_Min_AUD', 'Spend_Range_Max_AUD']]

alp_mediscare = alp_mediscare.explode('electorates')

#%%
alp_electorates = alp_vids[['electorates','Ad_URL', 'titles','Date_Range_End','Spend_Range_Min_AUD', 'Spend_Range_Max_AUD']]

alp_electorates = alp_electorates.explode('electorates')

alp_electorates['count'] = 1

alp_electorates_count = alp_electorates[['electorates','count']].groupby(['electorates']).count()


#%%

margins = pd.read_csv('margins.csv')

alp_mediscare = alp_mediscare.merge(margins, left_on='electorates', right_on='name', how='left')

alp_electorates_count_merge = alp_electorates_count.merge(margins, left_on='electorates', right_on='name', how='left')
#%%

alp_electorates_count_merge.to_csv('alp-electorates-details.csv')

#%%
median = alp_mediscare['margin'].median()
	
#%%	

# uap = aus[aus['Advertiser_Name'] == "United Australia Party"]
alp_postcodes_count.to_csv('postcodes-count.csv')
#%%



uwu_ads = ['CR500714056236138496','CR484516463252602880','CR236058721212432384']

uwu = aus[aus['Ad_ID'].isin(uwu_ads)]
uwu['electorates'] = uwu.apply(convertElec, axis=1)

#%%

uwu['postcodes'] = uwu.apply(convertPostcodes, axis=1)

#%%
uwu['count'] = 1
uwu_postcodes = uwu.explode('postcodes')
uwu_postcodes_count = uwu_postcodes[['postcodes', 'count']].groupby(['postcodes']).count()

uwu_electorates = uwu.explode('electorates')
uwu_electorates_count = uwu_electorates[['electorates', 'count']].groupby(['electorates']).count()


#%%

leigh = aus[aus['Advertiser_Name'] == "Andrew K Leigh"]
leigh['count'] = 1
leigh['postcodes'] = leigh.apply(convertPostcodes, axis=1)
leigh['electorates'] = leigh.apply(convertElec, axis=1)

leigh_postcodes = leigh.explode('postcodes')
leigh_postcodes_count = leigh_postcodes[['postcodes', 'count']].groupby(['postcodes']).count()

leigh_electorates = leigh.explode('electorates')
leigh_electorates_count = leigh_electorates[['electorates', 'count']].groupby(['electorates']).count()


#%%

alp_postcodes_count = alp_postcodes_count.rename(columns={"count":"alp-count"})
uwu_postcodes_count = uwu_postcodes_count.rename(columns={"count":"uwu-count"})
leigh_postcodes_count = leigh_postcodes_count.rename(columns={"count":"leigh-count"})

total_postcodes = alp_postcodes_count.merge(uwu_postcodes_count, how='outer', left_index=True, right_index=True)

total_postcodes = total_postcodes.merge(leigh_postcodes_count, how='outer', left_index=True, right_index=True)

#%%

# def yesNo(row):
# 	if row['count']

alp_electorates_count = alp_electorates_count.rename(columns={"count":"alp-count"})

alp_electorates_count['adsShown'] = "yes"

alp_electorates_count = alp_electorates_count.reset_index()

elecs = margins[['name', 'incumbent', 'margin']]

new_alp_count = elecs.merge(alp_electorates_count, how="left", left_on="name", right_on="electorates")

new_alp_count['adsShown'] = new_alp_count['adsShown'].fillna("no")

# uwu_electorates_count = uwu_electorates_count.rename(columns={"count":"uwu-count"})
# leigh_electorates_count = leigh_electorates_count.rename(columns={"count":"leigh-count"})

# total_electorates = alp_electorates_count.merge(uwu_electorates_count, how='outer', left_index=True, right_index=True)

# total_electorates = total_electorates.merge(leigh_electorates_count, how='outer', left_index=True, right_index=True)


#%%
from syncMap import syncMap

def makeMap(df):
	df = df.fillna("")
	settings = [
				{
					"title": "Areas targeted with ads by the ALP and UWU",
					"subtitle": "",
					"footnote": "",
					"source": "",
					"boundary":"https://interactive.guim.co.uk/gis/POA_2021.json",
					"overlay":"https://interactive.guim.co.uk/gis/CED_2021.json",
					"place":"au"
				}
			]
	
	mapping = [{"data":"alp-count","display":"ALP ad count","values":"","colours":"#fed976, #800026","tooltip":"<strong>{{postcodes}}</strong><br>Count: <b>{{alp-count}}","overlayTooltip":"<br><strong>{{CED_NAME21}}</strong>","scale":"linear","keyText":"Number of ads"},
			{"data":"uwu-count","display":"UWU ad count","values":"","colours":"#fed976, #800026","tooltip":"<strong>{{postcodes}}</strong><br>Count: <b>{{uwu-count}}","overlayTooltip":"<br><strong>{{CED_NAME21}}</strong>","scale":"linear","keyText":"Number of ads"},
			{"data":"leigh-count","display":"Andrew Leigh ad count","values":"","colours":"#fed976, #800026","tooltip":"<strong>{{postcodes}}</strong><br>Count: <b>{{leigh-count}}","overlayTooltip":"<br><strong>{{CED_NAME21}}</strong>","scale":"linear","keyText":"Number of ads"}]
	
	mapData = df.to_dict('records')
	syncMap(settings=settings, data=mapData, mapping=mapping, chartName="1D8yJH_CrpQEGWVTnfCVsTHHbQlN8jPPOVF-rNLGXyV8")


makeMap(total_postcodes.reset_index())

#%%

def makeMap2(df):
	df = df.fillna("")
	settings = [
				{
					"title": "Areas targeted with YouTube ads by the Labor party",
					"subtitle": "Showing the number of unqiue ads displayed since ",
					"footnote": "",
					"source": "",
					"boundary":"https://interactive.guim.co.uk/gis/CED_2021.json",
					"overlay":"",
					"place":"au"
				}
			]
	
	mapping = [{"data":"alp-count","display":"ALP ad count","values":"","colours":"#fed976, #800026","tooltip":"<strong>{{electorates}}</strong><br>Count: <b>{{alp-count}}","overlayTooltip":"<br><strong>{{CED_NAME21}}</strong>","scale":"linear","keyText":"Number of ads"}]
	
	mapData = df.to_dict('records')
	syncMap(settings=settings, data=mapData, mapping=mapping, chartName="1D8yJH_CrpQEGWVTnfCVsTHHbQlN8jPPOVF-rNLGXyV8-2")


makeMap2(total_electorates.reset_index())

#%%

def makeMap3(df):
	df = df.fillna("")
	settings = [
				{
					"title": "Areas targeted with political YouTube ads by the Labor party",
					"subtitle": "Showing areas targeted with political ads since 1 July 2021. The electorates shown have been derived from the postcode data provided in Google's ad transparency library, and so may differ in small ways to the actual targeted areas",
					"footnote": "",
					"source": "Guardian Australia analysis of <a href='https://transparencyreport.google.com/political-ads/region/AU' target='_blank'>Google ad transparency database</a>. Electorate margins courtesy Antony Green's <a href='https://antonygreen.com.au/2022-federal-electoral-pendulum/' target='_blank'>2021 redistribution pendulum</a>",
					"boundary":"https://interactive.guim.co.uk/gis/CED_2021.json",
					"overlay":"",
					"place":"au"
				}
			]
	
	mapping = [{"data":"adsShown","display":"ALP ad count","values":"no,yes","colours":"#e0f3f8, #d73027","tooltip":"<strong>{{name}}</strong><br><b>Margin</b>: {{margin}} ","scale":"ordinal","keyText":""}]
	
	mapData = df.to_dict('records')
	syncMap(settings=settings, data=mapData, mapping=mapping, chartName="1D8yJH_CrpQEGWVTnfCVsTHHbQlN8jPPOVF-rNLGXyV8-3")


makeMap3(new_alp_count)
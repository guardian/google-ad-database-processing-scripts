#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import youtube_transcript_api
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import requests
import simplejson as json
from collections import Counter
import re
import time
import scraperwiki

# https://transparencyreport.google.com/transparencyreport/api/v3/politicalads/creatives/details?entity_id=AR18849237072609280&creative_id=CR103253659495694336&hl=en
# Non YT video results https://transparencyreport.google.com/transparencyreport/api/v3/politicalads/creatives/details?entity_id=AR18849237072609280&creative_id=CR103253659495694336&hl=en
# YT id video https://transparencyreport.google.com/transparencyreport/api/v3/politicalads/creatives/details?entity_id=AR195639161946898432&creative_id=CR62918075430731776&hl=en

# TO DO
# backup YT vids in case of removal https://towardsdatascience.com/the-easiest-way-to-download-youtube-videos-using-python-2640958318ab
# make a audio transcriber for non-YT vids


# Gets video type, url and ID

def getVideoId(ad_url):
	url_split = ad_url.split("/")
	ar_id = url_split[6]
	cr_id = url_split[8]
	# print(ar_id, cr_id)
	ad_api_url = f"https://transparencyreport.google.com/transparencyreport/api/v3/politicalads/creatives/details?entity_id={ar_id}&creative_id={cr_id}&hl=en"
	print(ad_api_url)
	ad_results = requests.get(ad_api_url)
	results_text = ad_results.text.replace(")]}'","").strip()
	ad_results_json = json.loads(results_text)
	print(ad_results_json[0][3])

	# If ad removed

	if len(ad_results_json[0][3]) == 0:
		video_id = None
		video_type = "removed"
		video_url = None
		print("Removed?")
		print(ad_url)

	if len(ad_results_json[0][3]) > 0:	

		# Native doubleclick video

		if ad_results_json[0][3][0] == None:
			video_id = None
			video_type = "doubleclick"
			video_url = ad_results_json[0][3][1][0]
			print("doubleclick video")
				
		else:
			video_id = ad_results_json[0][3][0][0]
			video_type = "youtube"
			video_url = f"https://www.youtube.com/watch?v={video_id}"
			print("youtube video")
	print({"video_id":video_id, "video_type":video_type, "video_url":video_url})			
	return {"video_id":video_id, "video_type":video_type, "video_url":video_url}

def getTranscript(id):
	formatter = TextFormatter()
	try:
		transcript = YouTubeTranscriptApi.get_transcript(id)
		text = formatter.format_transcript(transcript)
		return text
	except youtube_transcript_api.TranscriptsDisabled:
		print("Transcripts disabled")
		return None

def parseVideos():
	# queryString = "* from aus_ads where Ad_Type='Video' AND video_id IS NULL"
	queryString = "* from aus_ads where Ad_Type='Video'"
	queryResult = scraperwiki.sqlite.select(queryString)
	for row in queryResult:
		# print(row)
		video_results = getVideoId(row['Ad_URL'])
		row['video_id'] = video_results['video_id']
		row['video_type'] = video_results['video_type']
		row['video_url'] = video_results['video_url']
		# print(row)
		scraperwiki.sqlite.save(unique_keys=["Ad_ID"], data=row, table_name="aus_ads")
		# time.sleep(0.1)

# parseVideos()

# Gets YouTube transcripts

formatter = TextFormatter()

def getTranscript(id):
	
	try:
		transcript = YouTubeTranscriptApi.get_transcript(id)
		text = formatter.format_transcript(transcript)
		return text
	except youtube_transcript_api.TranscriptsDisabled:
		print("Transcripts disabled")
		return None
	except youtube_transcript_api.NoTranscriptFound:
		print("No transcripts found")
		return None

# Gets Youtube titles and transcripts, adds to a database table

def addYoutubeInfo():

	queryString = "* from aus_ads where video_type='youtube'"
	queryResult = scraperwiki.sqlite.select(queryString)
	
	queryString2 = "* from youtube_ads"
	queryResult2 = scraperwiki.sqlite.select(queryString2)

	unique_vids_list_done = list(set([x['vid_id'] for x in queryResult2]))
	print(unique_vids_list_done)
	unique_vids_list = list(set([x['video_id'] for x in queryResult if x['video_id'] not in unique_vids_list_done]))
	print(unique_vids_list)

	vids_transcripts = {}
	vids_titles = {}
	
	if len(unique_vids_list) == 0:
		print("No YouTube videos to get")

	for vid_id in unique_vids_list:
		yt_ads = {}
		print("Getting transcript for", f"https://www.youtube.com/watch?v={vid_id}")
		yt_ads['url'] = f"https://www.youtube.com/watch?v={vid_id}"
		transcript = getTranscript(vid_id)
		vids_transcripts[vid_id] = transcript
		yt_ads['transcript'] = transcript
		print("Getting title for", f"https://www.youtube.com/oembed?format=json&url=https://www.youtube.com/watch?v={vid_id}")
		vid_info = requests.get(f"https://www.youtube.com/oembed?format=json&url=https://www.youtube.com/watch?v={vid_id}")
		if vid_info.text == "Not Found":
			vids_titles[vid_id] = "Removed"
		else:	
			vids_titles[vid_id] = vid_info.json()['title']

		yt_ads['title'] = vids_titles[vid_id]	
		yt_ads['vid_id'] = vid_id

		scraperwiki.sqlite.save(unique_keys=["vid_id"], data=yt_ads, table_name="youtube_ads")	

	# for row in queryResult:

	# 	row['yt_title'] = vids_titles[row['video_id']]
	# 	row['yt_transcript'] = vids_transcripts[row['video_id']]

	# 	print(row)
	# 	scraperwiki.sqlite.save(unique_keys=["Ad_ID"], data=row, table_name="aus_ads")
	# 	time.sleep(0.1)		

# addYoutubeInfo()

def addYoutubeInfoToAds():
	queryString1 = "* from youtube_ads"
	queryResult1 = scraperwiki.sqlite.select(queryString1)
	unique_yt_vids = {v['vid_id']:v for v in queryResult1}
	# print(unique_yt_vids)
	queryString2 = "* from aus_ads where video_type='youtube'"
	queryResult2 = scraperwiki.sqlite.select(queryString2)
	for row in queryResult2:
		row['yt_title'] = unique_yt_vids[row['video_id']]['title']
		row['yt_transcript'] = unique_yt_vids[row['video_id']]['transcript']

		print(row)
		scraperwiki.sqlite.save(unique_keys=["Ad_ID"], data=row, table_name="aus_ads")
		time.sleep(0.1)	

# addYoutubeInfoToAds()

# To do: speech recognition for doubleclick ad files https://towardsdatascience.com/transcribing-interview-data-from-video-to-text-with-python-5cdb6689eea1

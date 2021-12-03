import requests
import simplejson as json

# Text ad example https://transparencyreport.google.com/transparencyreport/api/v3/politicalads/creatives/details?entity_id=AR117485875444580352&creative_id=CR113556358325862400&hl=en

def getAdText(ad_url):
	url_split = ad_url.split("/")
	ar_id = url_split[6]
	cr_id = url_split[8]
	# print(ar_id, cr_id)
	ad_api_url = f"https://transparencyreport.google.com/transparencyreport/api/v3/politicalads/creatives/details?entity_id={ar_id}&creative_id={cr_id}&hl=en"
	print(ad_api_url)
	ad_results = requests.get(ad_api_url)
	results_text = ad_results.text.replace(")]}'","").strip()
	ad_results_json = json.loads(results_text)

def parseTextAds():
	# queryString = "* from aus_ads where Ad_Type='Video' AND video_id IS NULL"
	queryString = "* from aus_ads where Ad_Type='Text'"
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
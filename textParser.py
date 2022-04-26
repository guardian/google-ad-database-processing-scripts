import requests
import simplejson as json
import scraperwiki
import time

# Text ad example https://transparencyreport.google.com/transparencyreport/api/v3/politicalads/creatives/details?entity_id=AR117485875444580352&creative_id=CR113556358325862400&hl=en

def getFullAdText(ad_text_json):
	full_text = ""
	for thing in ad_text_json:
		if type(thing) is str:
			full_text =  full_text + thing + "\n"
		elif type(thing) is list:
			for things in thing:
				full_text = full_text + things + " "
			full_text =  full_text + "\n"	
	return full_text			


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
	if len(ad_results_json[0][3]) == 0:
		print("Removed?")
	else:
		ad_text_json = ad_results_json[0][3][3][8]
		print(ad_text_json)
		full_text = getFullAdText(ad_text_json)
		print(full_text)
		return full_text

def parseTextAds():
	# queryString = "* from aus_ads where Ad_Type='Video' AND video_id IS NULL"
	queryString = "* from aus_ads where Ad_Type='Text' AND ad_text IS NULL"
	queryResult = scraperwiki.sqlite.select(queryString)
	for row in queryResult:
		# print(row)
		row['ad_text'] = getAdText(row['Ad_URL'])
		# print(row)
		scraperwiki.sqlite.save(unique_keys=["Ad_ID"], data=row, table_name="aus_ads")
		time.sleep(0.1)

parseTextAds()		
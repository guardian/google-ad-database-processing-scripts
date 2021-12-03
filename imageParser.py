import requests
import simplejson as json
import scraperwiki
import time

# Get image Urls, download images, OCR and get the text, put text in database

# What to do with GIF frames? https://stackoverflow.com/questions/58464617/how-to-extract-text-from-web-gif-file-using-python

# https://tpc.googlesyndication.com/simgad/14920829860683001032
# https://transparencyreport.google.com/political-ads/advertiser/AR133579976896151552/creative/CR128161583594471424
# https://displayads-formats.googleusercontent.com/ads/preview/content.js?client=political-transparency&creativeId=505393888518&obfuscatedCustomerId=8447481120&uiFeatures=12&adGroupId=118004459246&versionId=0&sig=ACiVB_zWMQEbV-KCvJglCpWKYQSAbaENEA
# \x3e\x3cimg src\x3d\x22 and \x22

# url("media/803787d99edeff158f2ec41370277250.png")

def getImage(ad_url):
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
		return None
	else:
		# print(ad_results_json[0][3][4][3][3])
		ad_url = ad_results_json[0][3][4][3][3]
		print(ad_url)
		ad_js = requests.get(ad_url).text
		if "https://tpc.googlesyndication.com/simgad/" in ad_js:
			start = ad_js.index("https://tpc.googlesyndication.com/simgad/")
			ad_img_url = ad_js[start:]
			ad_img_url = ad_img_url.split("\\x22 border")[0]
			print(ad_img_url)
			return {"image_url":ad_img_url, "image_type":"image"}
		elif "https://tpc.googlesyndication.com/sadbundle/" in ad_js:
			start = ad_js.index("https://tpc.googlesyndication.com/sadbundle/")
			ad_img_url = ad_js[start:]
			ad_img_url = ad_img_url.split(";frame-src")[0]
			print(ad_img_url)
			return {"image_url":ad_img_url, "image_type":"html"}
				
		else:
			print("Not an image or html?")
			return {"image_url":None,"image_type":None}

def addImageUrls():
	# queryString = "* from aus_ads where Ad_Type='Video' AND video_id IS NULL"
	queryString = "* from aus_ads where Ad_Type='Image' AND image_url IS NULL"
	queryResult = scraperwiki.sqlite.select(queryString)
	for row in queryResult:
		print(row['Ad_URL'])
		image_results = getImage(row['Ad_URL'])
		row['image_url'] = image_results['image_url']
		row['image_type'] = image_results['image_type']
		scraperwiki.sqlite.save(unique_keys=["Ad_ID"], data=row, table_name="aus_ads")
		# time.sleep(0.1)

addImageUrls()	

# test = requests.get("https://transparencyreport.google.com/political-ads/advertiser/AR146135025295818752/creative/CR111531195346452480")

# print(test.text)
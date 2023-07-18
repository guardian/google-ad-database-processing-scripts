import requests
import simplejson as json
import scraperwiki
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.firefox.options import Options
import lxml.html

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)


# Get image Urls, download images, OCR and get the text, put text in database

# What to do with GIF frames? https://stackoverflow.com/questions/58464617/how-to-extract-text-from-web-gif-file-using-python

# https://tpc.googlesyndication.com/simgad/14920829860683001032
# https://transparencyreport.google.com/political-ads/advertiser/AR133579976896151552/creative/CR128161583594471424
# https://displayads-formats.googleusercontent.com/ads/preview/content.js?client=political-transparency&creativeId=505393888518&obfuscatedCustomerId=8447481120&uiFeatures=12&adGroupId=118004459246&versionId=0&sig=ACiVB_zWMQEbV-KCvJglCpWKYQSAbaENEA
# \x3e\x3cimg src\x3d\x22 and \x22

# url("media/803787d99edeff158f2ec41370277250.png")

images = ["png","jpg","jpeg","gif","tiff","tif"]

def getFileExtension(url):
	ext = url.split(".")[-1]
	if ext in images:
		return ext
	else:
		return "unknown_image"	

# Rewrite this to load the ad preview element, then figure out the type of element rather than checking for iframe etc

# Gif ad type

# <div class="creative-container _ngcontent-pdh-34"><div class="left-arrow-container _ngcontent-pdh-34"><!----></div><!----><creative class="has-variation _nghost-pdh-39 _ngcontent-pdh-34" interactive=""><!----><!----><div class="creative-container _ngcontent-pdh-39" style="width: 160px; height: 600px;"><div class="_ngcontent-pdh-39" style="transform: scale(1);"><!----><!----><html-renderer class="_ngcontent-pdh-39 _nghost-pdh-40"><div class="html-container _ngcontent-pdh-40"><img src="https://s0.2mdn.net/10313294/ScoMo_Banner_Ad-160x600-px.gif" width="160" height="600"></div></html-renderer><!----></div></div><!----></creative><div class="right-arrow-container _ngcontent-pdh-34"><!----></div><!----></div>

# Iframe ad type

# <div class="creative-container _ngcontent-owy-34"><div class="left-arrow-container _ngcontent-owy-34"><!----></div><!----><creative class="has-variation _nghost-owy-39 _ngcontent-owy-34" interactive=""><!----><!----><div class="creative-container _ngcontent-owy-39" style="width: 160px; height: 600px;"><div class="_ngcontent-owy-39" style="transform: scale(1);"><!----><!----><html-renderer class="_ngcontent-owy-39 _nghost-owy-40"><div class="html-container _ngcontent-owy-40"><iframe src="https://tpc.googlesyndication.com/archive/sadbundle/$csp%3Darchive$/13051226123090467654/index.html" style="border: 0" sandbox="allow-scripts" scrolling="no" width="160" height="600"></iframe></div></html-renderer><!----></div></div><!----></creative><div class="right-arrow-container _ngcontent-owy-34"><!----></div><!----></div>

# Policy violation

# <div class="creative-container _ngcontent-fpv-34"><div class="left-arrow-container _ngcontent-fpv-34"><!----></div><!----><creative class="has-variation _nghost-fpv-39 _ngcontent-fpv-34 click-shield" interactive=""><!----><!----><div class="loading-pulse delay-0 _ngcontent-fpv-39"></div><div class="creative-container _ngcontent-fpv-39 hidden-in-dom"><div class="_ngcontent-fpv-39"><!----><!----><!----></div></div><!----><div class="render-failed-container _ngcontent-fpv-39"><!----><!----><div class="policy-violation _ngcontent-fpv-39"><material-icon class="visibility-icon _nghost-fpv-20 _ngcontent-fpv-39" icon="hide_image"><i class="material-icon-i material-icons-extended _ngcontent-fpv-20" role="img" aria-hidden="true">hide_image</i></material-icon><span class="text _ngcontent-fpv-39">Sorry, we are unable to show you this variation</span><ad-policies-explorer class="popup-button _nghost-fpv-40 _ngcontent-fpv-39"><div class="ad-policies _ngcontent-fpv-40"><material-button animated="true" class="policy-button _nghost-fpv-11 _ngcontent-fpv-40" tabindex="0" role="button" aria-disabled="false" elevation="1"><div class="content _ngcontent-fpv-11">Our ad policies</div><material-ripple aria-hidden="true" class="_ngcontent-fpv-11"></material-ripple><div class="touch-target _ngcontent-fpv-11"></div><div class="focus-ring _ngcontent-fpv-11"></div></material-button></div><modal class="_ngcontent-fpv-40" pane-id="default--4">    <!---->
#   </modal></ad-policies-explorer></div></div></creative><div class="right-arrow-container _ngcontent-fpv-34"><!----></div><!----></div>


def getImage(ad_url):
	
	driver.get(ad_url)
	ad_iframe = None
	ad_removed = False
	policy_violation = False
	try:
		ad_container = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".creative-container"))).get_attribute('outerHTML')
		ad_img_url = None
		image_type = None
		# Ad content sometimes loads more slowly than the container
		time.sleep(5)
		if "<img" in ad_container:
			ad_img_url = driver.find_element(By.CSS_SELECTOR, "html-renderer img").get_attribute('src')
			image_type = getFileExtension(ad_img_url)
			print("Found image")
			return {"image_url":ad_img_url, "image_type":image_type, "ad_removed":ad_removed, "policy_violation":policy_violation}
		
		elif "<iframe" in ad_container:
			ad_iframe = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".creative-container iframe"))).get_attribute('src')
			print("Going to", ad_iframe)
			driver.get(ad_iframe)
			# If image-based ad
			iframe_html = driver.find_element(By.CSS_SELECTOR, "body").get_attribute('outerHTML')
			# print(iframe_html)
			if "google_image_div" in iframe_html:
				print("Image within an iframe")
				ad_img_url = driver.find_element(By.CSS_SELECTOR, "#google_image_div img").get_attribute('src')
				image_type = getFileExtension(ad_img_url)
			else:
				print("probably HTML etc")
				ad_img_url = ad_iframe
				image_type = "html"
			return {"image_url":ad_img_url, "image_type":image_type, "ad_removed":ad_removed, "policy_violation":policy_violation}
		
		elif "policy-violation" in ad_container:
			print("Ad removed, policy violation")
			ad_removed = True
			policy_violation = True
			return {"image_url":None, "image_type":None, "ad_removed":ad_removed, "policy_violation":policy_violation}
		
		else:
			print("Didn't find anything")
			return {"image_url":None, "image_type":None, "ad_removed":ad_removed, "policy_violation":policy_violation}
	except:
		print("Totally removed")
		return {"image_url":None, "image_type":None, "ad_removed":True, "policy_violation":policy_violation}

def addImageUrls():
	queryString = "* from aus_ads where (Ad_Type='Image' OR Ad_Type='IMAGE') AND image_url IS NULL AND ad_removed IS NOT 1"
	# queryString = "* from aus_ads where Ad_ID = 'CR07159689179394211841' OR Ad_ID = 'CR11008861203899351041' OR Ad_ID = 'CR13326603402826743809' OR Ad_ID = 'CR07159689179394211841' OR Ad_ID = 'CR87365235437993984' OR Ad_ID = 'CR08499488799858884609'"
	queryResult = scraperwiki.sqlite.select(queryString)
	for row in queryResult:
		print(row['Ad_URL'])
		image_results = getImage(row['Ad_URL'])
		row['image_url'] = image_results['image_url']
		row['image_type'] = image_results['image_type']
		row['ad_removed'] = image_results['ad_removed']
		row['policy_violation'] = image_results['policy_violation']
		scraperwiki.sqlite.save(unique_keys=["Ad_ID"], data=row, table_name="aus_ads")
		time.sleep(0.1)

def downloadImage(url):

	# Check if the content has an image extension or is HTML

	ext = url.split(".")[-1]
	print(ext)
	# If it is an image

	if ext in images:

		print("yeh")

		r = requests.get(url)

		img_name = url.split("/")[-1]

		with open(f'adimages/{img_name}', 'wb') as f:
			f.write(r.content)

		return img_name    

	# If it is HTML	

	else:

		# print("nah")
		r = requests.get(url)
	
		img_name = url.split("/")[-1]

		def getFileExtension(contentType):
			return contentType.split("/")[-1]

		ext = getFileExtension(r.headers['Content-Type'])

		if ext in images:
			with open(f'adimages/{img_name}.{ext}', 'wb') as f:
				f.write(r.content)

			return f'{img_name}.{ext}'
		else:
			print("Probs not an image")	    
			return None

def getImages():
	queryString = "* from aus_ads where (Ad_Type='Image' OR Ad_Type='IMAGE') AND image_type IS NOT NULL AND image_name IS NULL AND ad_removed IS NOT 1"
	queryResult = scraperwiki.sqlite.select(queryString)
	for row in queryResult:
		if "png" in row['image_url']:
			image_name = downloadImage(row['image_url'])
			print(image_name)
			row['image_name'] = image_name
			scraperwiki.sqlite.save(unique_keys=["Ad_ID"], data=row, table_name="aus_ads")
			time.sleep(0.1)
		else:			
			print(row['image_url'])
			image_name = downloadImage(row['image_url'])
			print(image_name)
			row['image_name'] = image_name
			scraperwiki.sqlite.save(unique_keys=["Ad_ID"], data=row, table_name="aus_ads")
			time.sleep(0.1)

def fixImages():
	queryString = "* from aus_ads where Ad_Type='Image' AND image_type='image'"
	queryResult = scraperwiki.sqlite.select(queryString)
	for row in queryResult:
		if len(row['image_url']) > 200:
			row['image_url'] = row['image_url'].split("?")[0].split(");")[0].split("\\x27")[0]
			scraperwiki.sqlite.save(unique_keys=["Ad_ID"], data=row, table_name="aus_ads")
			time.sleep(0.1)


def doImageStuff():
	print("adding image URLs")
	# addImageUrls()
	print("downloading images")
	getImages()	

# fixImages()
doImageStuff()
# test = requests.get("https://transparencyreport.google.com/political-ads/advertiser/AR146135025295818752/creative/CR111531195346452480")

# test_urls = ['https://adstransparency.google.com/advertiser/AR02720549520713711617/creative/CR10324419613655302145?political=&region=AU', 'https://adstransparency.google.com/advertiser/AR15294722344598110209/creative/CR07847368350345723905?political=&region=AU']

# for url in test_urls:
# 	getImage(url)
# print(test.text)



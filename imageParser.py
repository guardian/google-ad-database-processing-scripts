import requests
import simplejson as json
import scraperwiki
import time
import re 
import os

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
		return {"image_url":None,"image_type":None}
	elif len(ad_results_json[0][3]) > 3:
		# print(ad_results_json[0][3][4][3][3])
		ad_url = ad_results_json[0][3][4][3][3]
		print(ad_url)
		ad_js = requests.get(ad_url).text
		if "https://tpc.googlesyndication.com/simgad/" in ad_js:
			start = ad_js.index("https://tpc.googlesyndication.com/simgad/")
			ad_img_url = ad_js[start:]
			ad_img_url = ad_img_url.split("\\x22 border")[0]
			ad_img_url = ad_img_url.split("?")[0].split(");")[0].split("\\x27")[0]
	

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
	else:
		ad_url = ad_results_json[0][3][2][0][0][0][0]
		print(ad_url)
		ad_img_url = ad_results_json[0][3][2][0][0][1][0]
		print(ad_img_url)
		image_type = getFileExtension(ad_img_url )
		return {"image_url":ad_img_url, "image_type":image_type}

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
		time.sleep(0.1)
        
        
def parse_HTML(url):
    
    #extracting html object and storing it as text in page 
    r = requests.get(url)
    page = r.text
    
    #removing unneeded characters
    page = page.replace('"','')
            
    #defining regex pattern to find url endings
    pattern = re.compile("localUrl:(.*?)}")
            
    #applying pattern over page
    sub_urls = list(re.findall(pattern, page))
    
    return sub_urls



url_i = "https://tpc.googlesyndication.com/sadbundle/$csp%3Der3$/3760334257784916408/index.html"
url = "https://tpc.googlesyndication.com/simgad/11634816136131995676"

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
        
        
        r = requests.get(url)
        
        img_name = url.split("/")[-1]
        
        def getFileExtension(contentType):
             return contentType.split("/")[-1]

        ext = getFileExtension(r.headers['Content-Type'])
        
        #this keeps giving errors unles I makedir every time (idk)
        filename = "adimages/{img_name}"
        os.makedirs(os.path.dirname(filename), exist_ok = True)
        
        if ext in images:
            with open(f'adimages/{img_name}.{ext}', 'wb') as f:
                f.write(r.content)
                
            return f'{img_name}.{ext}'
        

        elif ext == "html": 
            #initialising required url suffix
            urls = parse_HTML(url)
        
            #replacing index suffix with needed media suffix
            new_url = url.replace("index.html", "media/")
            
            #this indexing should be generalised (remove hard coding)
            img_name = url.split("/")[-2]
            print(img_name)
            
            #new ext 
            ext = urls[1].split(".")[-1]
            
           
    
            #need to update this to identify image type for extension before loop
            #is currently just sampling the urls list
            for i in range(len(urls)):
                
                #I couldnt see this being created anywhere so did it here
                filename = "adimages/{img_name}"
                os.makedirs(os.path.dirname(filename), exist_ok = True)
                
                with open(f'adimages/{img_name}/img_{i}_{len(urls)}.{ext}', 'wb') as f:
                #concantenating image sub_url to new base url
                    sub_url = new_url + urls[i]
                    r = requests.get(sub_url)
                    f.write(r.content)
                    
            return img_name
           
        else:
            
            print("Probs not an image")	    
            return None

def getImages():
	queryString = "* from aus_ads where Ad_Type='Image' AND image_type IS NOT NULL AND image_name IS NULL"
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
	addImageUrls()
	print("downloading images")
	getImages()	

# fixImages()
# doImageStuff()
# test = requests.get("https://transparencyreport.google.com/political-ads/advertiser/AR146135025295818752/creative/CR111531195346452480")

# print(test.text)
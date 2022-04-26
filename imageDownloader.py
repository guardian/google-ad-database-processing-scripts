import requests
import simplejson as json
import scraperwiki

images = ["png","jpg","jpeg","gif","tiff","tif"]

def downloadImage(url):
	
	# Check if the content has an image extension or is HTML

	ext = url.split(".")[-1]
	
	# If it is an image

	if ext in images:

		r = requests.get(url)
		print(r.headers)

		img_name = url.split("/")[-1]

		with open(f'adimages/{img_name}', 'wb') as f:
		    f.write(r.content)
	
	# If it is HTML	

	else:

		r = requests.get(url)
		print(r.headers)

		img_name = url.split("/")[-1]

		def getFileExtension(contentType):
			return contentType.split("/")[-1]

		ext = getFileExtension(r.headers['Content-Type'])

		if ext in images:
			with open(f'adimages/{img_name}.{ext}', 'wb') as f:
			    f.write(r.content)
		else:
			print("Probs not an image")	    

downloadImage("https://s0.2mdn.net//8701942/8595a940-e2e9-4b83-af9e-680e94812034.png")

# https://s0.2mdn.net//8701942/8595a940-e2e9-4b83-af9e-680e94812034.png
# https://tpc.googlesyndication.com/simgad/17843993487467456159
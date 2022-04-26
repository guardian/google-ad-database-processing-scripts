import scraperwiki
import cv2
import os
import pytesseract
import time
from PIL import Image

def readImage(fileName):
	print("Converting {fileName} to greyscale".format(fileName=fileName))
	filePath = "adimages/" + fileName

	if ".gif" in fileName:
		text = ""
		img = Image.open(filePath)
		for frame in range(0,img.n_frames):
			img.seek(frame)
			imgrgb = img.convert('RGBA')
			# imgrgb.show()
			text = text + pytesseract.image_to_string(imgrgb)
			print(text)
		return text	
	else:	
		image = cv2.imread(filePath)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		ext = fileName.split(".")[1]
		tempFile = "temp." + ext
		cv2.imwrite(tempFile, gray)
		text = pytesseract.image_to_string(Image.open(tempFile))
		os.remove(tempFile)
		print(text)
		return text

def ocrImages(test):
	
	queryString = "* from aus_ads where image_type='image' AND image_text is NULL"
	queryResult = scraperwiki.sqlite.select(queryString)

	for row in queryResult:
		row['image_text'] = ""

		if row['image_name'] != "":
				print(row['image_name'])
				row['image_text'] = readImage(row['image_name'])
				# except Exception as e:
				# 	row['imageText'] = ""
				# 	print("error")
				# 	print(e)

		time.sleep(0.1)
		if not test:		
			scraperwiki.sqlite.save(unique_keys=["Ad_ID"], data=row, table_name="aus_ads")
			

ocrImages(False)
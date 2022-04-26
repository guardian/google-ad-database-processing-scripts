import scraperwiki
import cv2
import os
import pytesseract
import time
from PIL import Image


#the html part of this function is not picking up the text in the png images
#I think may be because they are transparent, need to change background with cv2 
#otherwise everything should work
def readImage(fileName, val = None):
    
    print("Converting {fileName} to greyscale".format(fileName=fileName))
    filePath = "adimages/" + fileName

    
    def process_img(filePath):
        image = cv2.imread(filePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ext = filePath.split(".")[1]
        tempFile = "temp." + ext
        cv2.imwrite(tempFile, gray)
        text = pytesseract.image_to_string(Image.open(tempFile))
        os.remove(tempFile)
        print(text)
        return text
    
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
    
    
    elif val and val in "html":
        
        text = ""

        for img in os.listdir(filePath):
            print(img)
            path_new = os.path.join(filePath, img)
            text += process_img(path_new)
            
        return text
        
        
    else: 
        return process_img(filePath)


#this can be merged with ocrImages, just seperated them for ease of construction
def ocr_HTML(test):
    queryString = "* from aus_ads where image_type='html' AND image_text is NULL"
    queryResult = scraperwiki.sqlite.select(queryString)

    for row in queryResult:
        val = row["image_type"]
        row['image_text'] = ""

        if row['image_name'] != "":
            print(row['image_name'])
            row['image_text'] = readImage(row['image_name'], val)
                # except Exception as e:
                #     row['imageText'] = ""
                #     print("error")
                #     print(e)

        
        time.sleep(0.1)
        if not test:        
            scraperwiki.sqlite.save(unique_keys=["Ad_ID"], data=row, table_name="aus_ads")
    
def ocrImages(test):
    
    queryString = "* from aus_ads where image_type='image' AND image_text is NULL"
    queryResult = scraperwiki.sqlite.select(queryString)

    for row in queryResult:
        row['image_text'] = ""

        if row['image_name'] != "":
                print(row['image_name'])
                row['image_text'] = readImage(row['image_name'])
                # except Exception as e:
                #     row['imageText'] = ""
                #     print("error")
                #     print(e)

        time.sleep(0.1)
        if not test:        
            scraperwiki.sqlite.save(unique_keys=["Ad_ID"], data=row, table_name="aus_ads")
            

ocrImages(False)
# adds the results to s3 

import boto3
import os
import io
import scraperwiki
import time
import simplejson as json
import gzip
import pandas as pd

def upload(test):

	AWS_KEY = os.environ['AWS_KEY_ID']
	AWS_SECRET = os.environ['AWS_SECRET_KEY']

	queryString = "* from aus_ads"
	queryResult = scraperwiki.sqlite.select(queryString)

	pd.DataFrame(queryResult).to_csv('aus-google-ad-data.csv.gz',compression='gzip', index=False)

	results = json.dumps(queryResult, indent=4)

	with open('aus-google-ad-data.json','w') as fileOut:
			fileOut.write(results)
		
	if not test:		
		print("Uploading JSON to S3")
		bucket = 'gdn-cdn'
		session = boto3.Session(
		aws_access_key_id=AWS_KEY,
		aws_secret_access_key=AWS_SECRET,
		)
		s3 = session.resource('s3')
		key = "2021/11/google-ad-data/aus-google-ad-data.json"
		object = s3.Object(bucket, key)
		object.put(Body=results, CacheControl="max-age=300", ACL='public-read')
		print("Done")

		print("Uploading CSV to S3")
		key2 = "2021/11/google-ad-data/aus-google-ad-data.csv.gz"
		s3.meta.client.upload_file('aus-google-ad-data.csv.gz', bucket, key2, ExtraArgs={"CacheControl":"max-age=300", 'ACL':'public-read'})
		print("Done")

upload(False)		
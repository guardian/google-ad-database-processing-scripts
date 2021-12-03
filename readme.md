# Making Google's political ad transparency library suck less

This is a series of scripts that takes Google's [political ad transparency data](https://transparencyreport.google.com/political-ads/home?hl=en) and makes the ad content searchable as, ironically, the world's most powerful search company does not make their ad data searchable.

It can also takes the ad targeting information and map it to electorates, but this only works for postcodes at the moment so isn't in the main group of scripts yet.

It is aimed at Australian content, but most of the scripts could be applied to all ad content if you'd like to use it elsewhere.

## Get the data

The current output is a work-in-progress, but you can find the latest file here as [gzipped csv](https://interactive.guim.co.uk/2021/11/google-ad-data/aus-google-ad-data.csv.gz) or [json](https://interactive.guim.co.uk/2021/11/google-ad-data/aus-google-ad-data.json)

## What it does:

- Gets the text content from text ads
- Gets the YouTube title for YouTube ads
- Gets the YouTube transcript for YouTube ads if it is available
- Gets the image URL for image ads

## Still to do:

- OCR images and put the text in the database
- Figure out if there's a good way to get text from animated html ads
- Run the non-YouTube video ads through speech-to-text and put the text in the database
- Archive ad content to S3 as Google removes it entirely when an ad is removed (eg UAP ads)
- Archive ad database daily to S3 with a timestamp
- Add electorates for Australian ads




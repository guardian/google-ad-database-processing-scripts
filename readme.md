# Making Google's political ad transparency library suck less

This is a series of scripts that takes Google's [political ad transparency data](https://transparencyreport.google.com/political-ads/home?hl=en) and makes the ad content searchable as, ironically, the world's most powerful search company does not make their ad data searchable.

It can also takes the ad targeting information and map it to electorates, but this only works for postcodes at the moment so isn't in the main group of scripts yet

## To do:

-OCR images and put the text in the database
-Figure out if there's a good way to get text from animated html ads
-Run the non-YouTube video ads through speech-to-text and put the text in the database
-Archive ad content to S3 as Google removes it entirely when an ad is removed (eg UAP ads)
-Archive ad database daily to S3 with a timestamp




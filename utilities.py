import scraperwiki
import time

queryString = "* from aus_ads where ad_removed = 1"
queryResult = scraperwiki.sqlite.select(queryString)
for row in queryResult:
    row['ad_removed'] = None
    scraperwiki.sqlite.save(unique_keys=["Ad_ID"], data=row, table_name="aus_ads")
    time.sleep(0.1)
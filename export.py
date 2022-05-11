#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import scraperwiki

queryString = f"* from aus_ads"
queryResult = scraperwiki.sqlite.select(queryString)
output = pd.DataFrame(queryResult)
output.to_csv("analysis/temp.csv", index=False)

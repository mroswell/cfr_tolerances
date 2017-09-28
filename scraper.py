# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

import scraperwiki
import lxml.html

# Read in a page
html = scraperwiki.scrape("https://www.law.cornell.edu/cfr/text/40/part-180/subpart-C")
# We'll build a second scraper for: 
# https://www.ecfr.gov/cgi-bin/retrieveECFR?gp=1&SID=0d522d57c79aa7c6bd629bce51d61a7f&h=L&mc=true&n=pt40.26.180&r=PART&ty=HTML
# and compare

# Find something on the page using css selectors
root = lxml.html.fromstring(html)
lis = root.cssselect("li")

for li in lis:
  record = {"li" : li.text}
  scraperwiki.sqlite.save(unique_keys=['li'], data=record)

  
# Write out to the sqlite database using scraperwiki library
#scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})

# An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".

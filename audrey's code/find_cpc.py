#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
***Note: DO NOT RUN  ***
This will likely take a very long time.

Web Scraping for Patent Classification and Year

This script creates a file for any patent in citation_backward_forward
that does not have a classification or year (e.g. pre-1976, plant, reissue, 
etc.) by searching for the patent details on Google Patents. 

The file produced is outputs/found_na_cpc.csv, which has the header:
    patent, year, subsection_id.
    
@author: Audrey Yang (auyang@seas.upenn.edu)
"""

import time
import csv
from urllib.request import urlopen
from urllib.error import HTTPError
import re

print('***\nBEGIN PROCESS')
start_time = time.ctime()

# Load citations_forward_backward
na_patents_file = open('../outputs/no_cpc.csv', encoding='utf-8-sig')
na_patents = csv.DictReader(na_patents_file, delimiter=',')

with open('../outputs/found_na_cpc.csv', 'w', newline="\n", 
          encoding='utf-8-sig') as output_file:
    output = csv.writer(output_file, delimiter=',')
    header = ['patent', 'year', 'subsection_id']
    
    for row in na_patents:
        sub, match = 'N/A', 'N/A'
        
        try:
            # Open Google Patents page
            page = urlopen("https://patents.google.com/patent/US" + 
                           row['citation_id'])
            html = page.read().decode("utf-8")
            
            # Match first cpc subsection
            pattern_sub = ('</li>\n          <li itemprop="cpcs" ' 
                           + 'itemscope repeat>\n            ' 
                           + '<span itemprop="Code">.*?</span>')
            res = re.search(pattern_sub, html, re.IGNORECASE)
            if res:
                match = res.group()
                sub = re.sub("<.*?>", "", match).strip()
            
            # Match year
            pattern_year = '<meta name="DC.date" content=".*?" scheme="issue">'
            res = re.search(pattern_year, html, re.IGNORECASE)
            if res:
                match = res.group()
                year = re.sub("<.* content=\"", "", match)
                year = re.sub("\" .*>", "", year).strip()[:4]
            
            if not (sub == 'N/A' and match == 'N/A'):
                output.writerow([row['citation_id'],'',''])       
        except HTTPError: # if the page doesn't exist
            pass


print('***\nEND OF PROCESS')
end_time = time.ctime()

print('Start Time: ' + start_time)
print('End Time: ' + end_time)
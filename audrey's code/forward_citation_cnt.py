#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Foward Citation Count

This script counts the forward citations per patent for 4 different year 
ranges. The year ranges are 4, 5, 6, and 7 years after the publication year 
of the patent.

Ths file produced is outputs/forward_citation_cnt.csv, which has the header:
    ipo_firm, year, forward_cnt4, forward_cnt5, forward_cnt6, forward_cnt7.

@author: Audrey Yang (auyang@seas.upenn.edu)
"""

import time
import csv

print('***\nBEGIN PROCESS')
start_time = time.ctime()

# Load in citations_forward_backward.csv
citations_file = open('../outputs/citations_forward_backward.csv', 
                      encoding='utf-8-sig')
citations = csv.DictReader(citations_file, delimiter=',')

# Create output file
print('WRITING TO FILE\n...')
with open('../outputs/forward_citation_cnt.csv', 'w', 
          newline='\n', encoding='utf-8-sig') as output_file:
    output = csv.writer(output_file, delimiter=',')
    header = ['ipo_firm', 'year', 'forward_cnt4', 'forward_cnt5', 
              'forward_cnt6', 'forward_cnt7']
    output.writerow(header)
    
    # Keep track of current state 
    last_year = 0
    last_firm = ''
    last_patent = ''
    count4, count5, count6, count7 = 0, 0, 0, 0
    
    for row in citations:
        if row['citation_type'] == '1':
            if row['sequence'] == '0':                
                if not (int(row['date_patent']) == last_year and 
                        row['ipo_firm'] == last_firm):
                    # Write to file
                    if last_year:
                        output.writerow([
                                last_firm, 
                                last_year, 
                                count4, 
                                count5,
                                count6, 
                                count7
                            ])
        
                    # Reset + update
                    last_year = int(row['date_patent'])
                    last_firm = row['ipo_firm']
                    count4, count5, count6, count7 = 0, 0, 0, 0
                    
                curr = int(row['date_citation'])
                if curr - last_year <= 4:
                    count4 += 1
                if curr - last_year <= 5:
                    count5 += 1
                if curr - last_year <= 6:
                    count6 += 1
                if curr - last_year <= 7:
                    count7 += 1   
    
    # Write last thing            
    if last_year:
        output.writerow([
                last_firm, 
                last_year, 
                count4, 
                count5,
                count6, 
                count7
            ])
        
print('***\nEND OF PROCESS')
end_time = time.ctime()

print('Start Time: ' + start_time)
print('End Time: ' + end_time)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Maps firm, year to the number of inventors

Outputs file firm_year_inventor_cnt.csv with header: 
    ipo_firm, year, num_inventors, loss, gain

@author: Audrey Yang (auyang@seas.upenn.edu)
"""

import time
import csv

print('***\nBEGIN PROCESS')
start_time = time.ctime()

# Load inventor_year_dominant_firm
dominant_firm_file = open('../outputs/inventor_year_dominant_firm.csv', 
                      encoding='utf-8-sig')
dominant_firm = csv.DictReader(dominant_firm_file, delimiter=',')

# Create firm year to inventor dict
print('Creating inventor to granted patent year dict\n...')
firm_year_inventor = {}
for row in dominant_firm:
    # Skip if N/A
    if row['extrapolated_dominant_assignee'] == 'N/A':
        continue

    # Get firms -> years
    years = firm_year_inventor.get(row['extrapolated_dominant_assignee'], {})
    # Get years -> inventors
    inventors = years.get(int(row['year']), set())
    # Add to inventor set
    inventors.add(row['inventor_id'])
    years[int(row['year'])] = inventors
    firm_year_inventor[row['extrapolated_dominant_assignee']] = years

this_year = 2021

# Write to output file
print('Writing to output file\n...')
with open('../outputs/firm_year_inventor_cnt.csv', 'w', 
          newline='\n', encoding='utf-8-sig') as output_file:
    output = csv.writer(output_file, delimiter=',')
    header = ['ipo_firm', 'year', 'num_inventors', 'loss', 'gain']
    output.writerow(header)

    for firm, years in firm_year_inventor.items():
        start = min(years.keys())
        output.writerow([firm, start, len(years[start]), 0, 0])
        last = start
        for i in range(start + 1, this_year):
            if i not in years:
                output.writerow([firm, i, len(years[last]), 0, 0])
            else:
                intersect = years[i].intersection(years[last])
                loss = len(years[last].difference(intersect))
                gain = len(years[i].difference(intersect))
                output.writerow([firm, i, len(years[i]), loss, gain])
                last = i


print('***\nEND OF PROCESS')
end_time = time.ctime()

print('Start Time: ' + start_time)
print('End Time: ' + end_time)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Maps inventor to the dominant firm (meaning inventor contibuted the most 
    patents to that firm) and if they contributed to more than
    one firm in a year.

Outputs file inventor_year_dominant_firm.csv with header: 
    inventor_id, year, dominant_assignee, more_than_one

@author: Audrey Yang (auyang@seas.upenn.edu)
"""

import time
import csv
from collections import Counter

print('***\nBEGIN PROCESS')
start_time = time.ctime()

# Load application
app_file = open('../patent_data/application.tsv', 
                        encoding='utf-8-sig')
application = csv.DictReader(app_file, delimiter='\t') 
    
# Create patent to year dictionary
print('Creating year dict\n...')
patent_to_year = {}
for row in application:
    patent_to_year[row['patent_id']] = int(row['date'][:4])

# Load inventor_year_patents
inventor_patents_file = open('../outputs/inventor_patent.csv', 
                      encoding='utf-8-sig')
inventor_patents = csv.DictReader(inventor_patents_file, delimiter=',')

# Load assignee_firms
assignee_firms_file = open('../patent_data/assignee.tsv', 
                      encoding='utf-8-sig')
assignee_firms = csv.DictReader(assignee_firms_file, delimiter='\t') 

# Create assignee id to firm name dict
print('Creating assignee_id to firm dict\n...')
assignee_id_to_name = {}
for row in assignee_firms:
    if row['organization']:
        assignee_id_to_name[row['id']] = row['organization']

# Load name_matches
name_matches_file = open('../outputs/name_matches_2.csv', 
                      encoding='utf-8-sig')
name_matches = csv.DictReader(name_matches_file, delimiter=',')

# Create assignee id to ipo firm dict
print('Creating assignee_id to ipo name dict\n...')
ipo_name = {}
for row in name_matches:
    ipo_name[row['assignee_id']] = row['ipo_firm']
    
# Get first inventor
next(inventor_patents)
curr_inv = next(inventor_patents)['inventor_id']
inventor_patents_file.seek(0)
next(inventor_patents)

this_year = 2020

# Create output file
print('WRITING TO FILE\n')
with open('../outputs/inventor_year_dominant_firm.csv', 'w', 
          newline='\n', encoding='utf-8-sig') as output_file:
    output = csv.writer(output_file, delimiter=',')
    header = ['inventor_id', 'year', 'dominant_assignee', 'more_than_one']
    output.writerow(header)
    
    year_assignee = {}
    firm = ''

    for row in inventor_patents:
        # Write to file (first year -> this year)
        if not row['inventor_id'] == curr_inv:
            if year_assignee:
                start = min(year_assignee)
                for i in range(start, this_year + 1):
                    if i in year_assignee:
                        firm_freq = Counter(year_assignee[i])
                        dominant = firm_freq.most_common(1)[0][0];
                        more = int(len(firm_freq) > 1)
                        output.writerow([curr_inv, i, dominant, more])
                    else:
                        output.writerow([curr_inv, i, 'N/A', 0])
                
            curr_inv = row['inventor_id']
            year_assignee = {}
        
        # Track assignees
        if row['assignee_id'] in ipo_name:
            firm = ipo_name[row['assignee_id']]
        else:
            firm = assignee_id_to_name.get(row['assignee_id'], 'N/A')
        
        # Track year
        year = int(patent_to_year.get(row['patent_id'], this_year + 1))
        if year < this_year:
            assignee_in_year = year_assignee.get(year, [])
            assignee_in_year.append(firm)
            year_assignee[year] = assignee_in_year

    if year_assignee:
        start = min(year_assignee)
        for i in range(start, this_year + 1):
            if i in year_assignee:
                firm_freq = Counter(year_assignee[i])
                dominant = firm_freq.most_common(1)[0];
                more = int(len(firm_freq) > 1)
                output.writerow([curr_inv, i, dominant, more])
            else:
                output.writerow([curr_inv, i, 'N/A', 0])

print('***\nEND OF PROCESS')
end_time = time.ctime()

print('Start Time: ' + start_time)
print('End Time: ' + end_time)
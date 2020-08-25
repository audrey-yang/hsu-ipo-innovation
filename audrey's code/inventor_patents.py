#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inventor to Patents and Citation

@author: Audrey Yang (auyang@seas.upenn.edu)
"""

import time
import csv

print('***\nBEGIN PROCESS')
start_time = time.ctime()

# Load patent_assignee
patent_assignee_file = open('../patent_data/patent_assignee.tsv', 
                            encoding='utf-8-sig')
patent_assignee = csv.DictReader(patent_assignee_file, delimiter='\t')

# Create patent to assignee dictionary
print('Creating patent to assignee dict\n...')
patent_to_assignee = {}
for row in patent_assignee:
    patent_to_assignee[row['patent_id']] = row['assignee_id']

# Load cpc_current
cpc_current_file = open('../patent_data/cpc_current.tsv', 
                            encoding='utf-8-sig')
cpc_current = csv.DictReader(cpc_current_file, delimiter='\t')

# Create patent to subsection_id and sequence dictionary
print('Creating subsection dict\n...') 
patent_to_subsection = {}
for row in cpc_current:
    if row['sequence'] == '0':
        patent_to_subsection[row['patent_id']] = row['subsection_id']
    
# Load patent
patent_file = open('../patent_data/patent.tsv', 
                        encoding='utf-8-sig')
patent = csv.DictReader(patent_file, delimiter='\t') 
    
# Create patent to year dictionary
print('Creating year dict\n...')
patent_to_year = {}
for row in patent:
    patent_to_year[row['number']] = int(row['date'][:4])
 
# Load uspatentcitation
uspatentcitation_file = open('../patent_data/uspatentcitation.tsv', 
                            encoding='utf-8-sig')
uspatentcitation = csv.DictReader(uspatentcitation_file, delimiter='\t')

# Year range (for forward citations)
year_range = 7

# Create patent to citation dictionary, fw and bk
print('Creating citations dict\n...')
patent_to_citationbk = {}
patent_to_citationfw = {}
for row in uspatentcitation:
    # Adding to backward citations
    lstbk = patent_to_citationbk.get(row['patent_id'], [])
    lstbk.append(row['citation_id'])
    patent_to_citationbk[row['patent_id']] = lstbk
    
    # Adding to forward citations
    if row['date']:
        if patent_to_year.get(row['patent_id'],  
                              20000) - int(row['date'][:4]) <= year_range:
            lstfw = patent_to_citationfw.get(row['citation_id'], [])
            lstfw.append(row['patent_id'])
            patent_to_citationfw[row['citation_id']] = lstfw

# Load inventor_patent
inventor_to_patent_file = open('../outputs/inventor_patent.csv', 
                               encoding='utf-8-sig')
inventor_to_patent = csv.DictReader(inventor_to_patent_file)

# Write to output file
print('Creating output file \n...')
with open('../outputs/inventor_year_patents.csv', 'w', 
              newline="\n", encoding='utf-8-sig') as output_file:
    output = csv.writer(output_file, delimiter=',')
    header = ['inventor_id', 
              'assignee_patent', 
              'patent_id', 
              'date_patent',
              'assignee_citation',
              'citation_id', 
              'date_citation', 
              'subsection_id', 
              'citation_type',
              ]
    output.writerow(header)   

    for row in inventor_to_patent:
        # Writing backward citation (citation_type = 0)
        patent = row['patent_id']
        for cit in patent_to_citationbk.get(patent, []):
            output.writerow([
                    row['inventor_id'], 
                    row['assignee_id'],
                    patent,
                    patent_to_year.get(patent, 'N/A'),
                    patent_to_assignee.get(cit, 'N/A'),
                    cit,
                    patent_to_year.get(cit, 'N/A'),
                    'Design' if cit[0] == 'D' else (
                            patent_to_subsection.get(cit, 'N/A')),
                    0
                ]) 
        
        # Writing forward citation (citation_type = 1)
        for cit in patent_to_citationfw.get(patent, []):
            output.writerow([
                row['inventor_id'], 
                row['assignee_id'],
                patent,
                patent_to_year.get(patent, 'N/A'),
                patent_to_assignee.get(cit, 'N/A'),
                cit,
                patent_to_year.get(cit, 'N/A'),
                'Design' if cit[0] == 'D' else (
                            patent_to_subsection.get(cit, 'N/A')),
                1
            ]) 
    
print('***\nEND OF PROCESS')
end_time = time.ctime()

print('Start Time: ' + start_time)
print('End Time: ' + end_time)
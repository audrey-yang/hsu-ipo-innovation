#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backward and Forwards Citations

@author: Audrey Yang (auyang@seas.upenn.edu)
"""

import time
import csv

from urllib.request import urlopen
from urllib.error import HTTPError
import re

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

# Load assignee
'''
assignee_file = open('../patent_data/assignee.tsv', encoding='utf-8-sig')
assignee = csv.DictReader(assignee_file, delimiter='\t')

# Create organization to assignee_id dictionary
print('Creating assignee to org dict\n...')
id_to_org = {}
for row in assignee:
    id_to_org[row['id']] = row['organization']
'''

# Load cpc_current
cpc_current_file = open('../patent_data/cpc_current.tsv', 
                            encoding='utf-8-sig')
cpc_current = csv.DictReader(cpc_current_file, delimiter='\t')

# Create patent to subsection_id and sequence dictionary
print('Creating subsection dict\n...') 
patent_to_subsection = {}
for row in cpc_current:
    lst = patent_to_subsection.get(row['patent_id'], [])
    lst.append([row['subsection_id'], row['group_id'], row['sequence']])
    patent_to_subsection[row['patent_id']] = lst

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

# Load Kenneth table
firm_year_patentcnt_file = open('../outputs/firm_year_patentcnt.csv', 
                            encoding='utf-8-sig')
firm_year_patentcnt = csv.DictReader(firm_year_patentcnt_file, delimiter=',')

# Helper function for checking if org patents cites another org patent
'''
def cites_self(patent, citation):
    assignee1 = patent_to_assignee.get(patent) 
    assignee2 = patent_to_assignee.get(citation) 
    if not assignee1 or not assignee2:
        return False
    return True if assignee1 == assignee2 else (
            id_to_org.get(assignee1, '1') == id_to_org.get(assignee2))
'''

# Write to output file
with open('../outputs/citations_forward_backward.csv', 'w', 
              newline="\n", encoding='utf-8-sig') as output_file:
    output = csv.writer(output_file, delimiter=',')
    header = ['ipo_firm', 
              'assignee_patent', 
              'patent_id', 
              'date_patent',
              'assignee_citation',
              'citation_id', 
              'date_citation', 
              'subsection_id', 
              'group_id',
              'sequence', 
              'citation_type',
              #'self_cite'
          ]
    output.writerow(header)
    
    print('Writing to output file\n...')
    na = ['N/A', 'N/A', 'N/A']
    for row in firm_year_patentcnt:
        if int(row['patent_cnt']) > 0:
            for patent in row['patent_ids'].split('; '):
                # Writing backward citation (citation_type = 0)
                for cit in patent_to_citationbk.get(patent, []):
                    if not cit in patent_to_subsection:
                        # Web scraping if cit isn't in cpc dictionary
                        sub, grp, year = 'N/A', 'N/A', 'N/A'
                        if cit[0] == 'D':
                            sub, grp = 'Design', 'Design'
                        elif cit[0] == 'P':
                            sub, grp = 'Plant', 'Plant'
                        elif not cit in patent_to_year:
                            try:
                                page = urlopen("https://patents.google.com/patent/US" + 
                                               cit)
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
                            except HTTPError:
                                pass
                        
                        output.writerow([
                                    row['ipo_firm'], 
                                    patent_to_assignee.get(patent, 'N/A'), 
                                    patent,
                                    row['year'],
                                    patent_to_assignee.get(cit, 'N/A'), 
                                    cit,
                                    patent_to_year.get(cit, year),
                                    sub,
                                    grp,
                                    0,
                                    0,
                                    #int(cites_self(patent, cit))
                                ]) 
                    else:
                        for sec in patent_to_subsection.get(cit, [na]):
                            output.writerow([
                                    row['ipo_firm'], 
                                    patent_to_assignee.get(patent, 'N/A'), 
                                    patent,
                                    row['year'],
                                    patent_to_assignee.get(cit, 'N/A'), 
                                    cit,
                                    patent_to_year.get(cit),
                                    sec[0],
                                    sec[1],
                                    sec[2],
                                    0,
                                    #int(cites_self(patent, cit))
                                ]) 
                
                # Writing forward citation (citation_type = 1)
                for cit in patent_to_citationfw.get(patent, []):
                    for sec in patent_to_subsection.get(cit, [na]):
                        output.writerow([
                                row['ipo_firm'], 
                                patent_to_assignee.get(patent, 'N/A'), 
                                patent,
                                row['year'],
                                patent_to_assignee.get(cit, 'N/A'), 
                                cit,
                                patent_to_year.get(cit),
                                'Design' if cit[0] == 'D' else sec[0],
                                'Design' if cit[0] == 'D' else sec[1],
                                0 if cit[0] == 'D' else sec[2],
                                1,
                                #int(cites_self(patent, cit))
                            ])

print('***\nEND OF PROCESS')
end_time = time.ctime()

print('Start Time: ' + start_time)
print('End Time: ' + end_time)
    
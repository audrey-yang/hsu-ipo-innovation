#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patent Originality and Generality

@author: Audrey Yang (auyang@seas.upenn.edu)
"""

import time
import csv

print('***\nBEGIN PROCESS')
start_time = time.ctime()

# Load citations_forward_backward
citations_file = open('../outputs/citations_forward_backward.csv', 
                            encoding='utf-8-sig')
citations = csv.DictReader(citations_file, delimiter=',')

print('Creating originality and generality dicts\n...')
originality = {}
generality = {}

for row in citations:
    # Only processing citations where sequence is 0 and has subsection_id
    if row['sequence'] == '0' and not row['subsection_id'] == 'N/A':
        # Backward citations -> originality
        if row['citation_type'] == '0':
            # Track subsection_id -> freq
            c = originality.get(row['patent_id'], {})
            c[row['subsection_id']] = c.get(row['subsection_id'], 0) + 1
            originality[row['patent_id']] = c
        # Forward citations -> generality
        elif row['citation_type'] == '1':
             # Track subsection_id -> freq
            c = generality.get(row['patent_id'], {})
            c[row['subsection_id']] = c.get(row['subsection_id'], 0) + 1
            generality[row['patent_id']] = c
 
# Load Kenneth table
firm_year_patentcnt_file = open('../outputs/firm_year_patentcnt.csv', 
                            encoding='utf-8-sig')
firm_year_patentcnt = csv.DictReader(firm_year_patentcnt_file, delimiter=',')
       
print('Creating output file\n...')
with open('../outputs/originality_generality.csv', 'w', 
              newline="\n", encoding='utf-8-sig') as output_file:
    output = csv.writer(output_file, delimiter=',')
    header = ['ipo_firm', 'year', 'patent_id', 'originality', 'generality']
    output.writerow(header)
    
    print('Writing to output file\n...')
    for row in firm_year_patentcnt:
        if not row['patent_cnt'] == '0':
            for patent in row['patent_ids'].split('; '):
                orig = 0
                gen = 0
                
                # Calculating originality measure
                if patent in originality:
                    len_cit = sum(originality.get(patent).values())
                    for _, sec in originality.get(patent).items():
                        orig += (sec / len_cit) ** 2
                    orig = 1 - orig
                else:
                    # N/A if doesn't cite anything (with a subsection_id)
                    orig = 'N/A'
                
                # Calculating generality measure
                if patent in generality:
                    len_cit = sum(generality.get(patent, {}).values())
                    for _, sec in generality.get(patent, {}).items():
                        gen += (sec / len_cit) ** 2
                    gen = 1 - gen
                else:
                    # N/A if isn't cited by anything (with a subsection_id)
                    gen = 'N/A'
                
                output.writerow([
                        row['ipo_firm'],
                        row['year'],
                        patent,
                        orig,
                        gen
                    ])
        

print('***\nEND OF PROCESS')
end_time = time.ctime()

print('Start Time: ' + start_time)
print('End Time: ' + end_time)
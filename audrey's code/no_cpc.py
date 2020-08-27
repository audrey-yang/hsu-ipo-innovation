#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
All Patents Without Classification

@author: Audrey Yang (auyang@seas.upenn.edu)
"""

import csv

print("Looking for patents.......\n")
citations_file = open('../outputs/citations_forward_backward.csv', 
                            encoding='utf-8-sig')
citations = csv.DictReader(citations_file, delimiter=',')

no_classification = set()

for row in citations:
    if row['subsection_id'] == 'N/A':
        no_classification.add((row['patent_id'], row['citation_id']))

with open('../outputs/no_cpc.csv', 'w', newline='\n',
          encoding='utf-8-sig') as output_file:
    output = csv.writer(output_file, delimiter=',')
    header = ['patent', 'citation']
    output.writerow(header)
    
    print("NO CLASSIFICATION")
    for cit in no_classification:
        output.writerow([cit[0], cit[1]])
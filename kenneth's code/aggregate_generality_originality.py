# Kenneth Shinn
# kshinn@sas.upenn.edu
#
# This code takes in a file called "originality_generality.csv" with the schema 
# ['ipo_firm', 'year', 'patent_id', 'originality', 'generality']
#
# Aggregates this dataset into schema
# ['ipo_firm', 'year', 'originality', 'generality']
#
# Uses a simple average
#
#########################################################################################

import csv
import math
import time

# start time
start_time = time.ctime()

print('READING FILES\n')
# load in the ipo_match file
og_file = open('dependent_data/firm_originality_generality.csv', encoding='utf-8-sig')
og = csv.DictReader(og_file, delimiter=",")

# load in the firm year patent file
firm_year_patentcnt_file = open('dependent_data/firm_year_patentcnt.csv', encoding='utf-8-sig')
firm_year_patentcnt = csv.DictReader(firm_year_patentcnt_file, delimiter=",")

# create an output file (firm year patent cnt)
output = open('outputs/firm_year_innovation.csv', 'w', newline="\n", encoding='utf-8-sig')
firm_year_innovation = csv.writer(output, delimiter=',')
header = ['ipo_firm', 'year', 'originality', 'generality4', 'generality5', 'generality7']
firm_year_innovation.writerow(header)

# create a dictionary of ipo_firms (firm, year) -> 
# (o_sum, g4_sum, g5_sum, g7_sum, o_cnt, g4_cnt, g5_cnt, g7_cnt)
innovation_dict = {}

# find all the potential firm years
print('CALCULATING ALL POTENTIAL FIRM YEAR\n')
for row in firm_year_patentcnt:
	firm = row['ipo_firm']
	year = row['year']
	firm_year = (firm, year)
	innovation_dict[firm_year] = (0, 0, 0, 0, 0, 0, 0, 0)

print('AGGREGATING ORIGINALITY AND GENERALITY SCORES\n')
for row in og:
	firm = row['ipo_firm']
	year = row['year']
	originality = row['originality']
	generality4 = row['generality4']
	generality5 = row['generality5']
	generality7 = row['generality7']

	firm_year = (firm, year)

	if firm_year in innovation_dict:
		o_sum, g4_sum, g5_sum, g7_sum, o_cnt, g4_cnt, g5_cnt, g7_cnt = innovation_dict[firm_year]
		if not originality == 'N/A':
			o_sum += float(originality)
			o_cnt += 1
		if not generality4 == 'N/A':
			g4_sum += float(generality4)
			g4_cnt += 1
		if not generality5 == 'N/A':
			g5_sum += float(generality5)
			g5_cnt += 1
		if not generality7 == 'N/A':
			g7_sum += float(generality7)
			g7_cnt += 1
		innovation_dict[firm_year] = (o_sum, g4_sum, g5_sum, g7_sum, o_cnt, g4_cnt, g5_cnt, g7_cnt)
	else:
		print('ERROR FIRM YEAR NOT FOUND!!')
		break

for key, value in innovation_dict.items():
	firm, year = key
	o_sum, g4_sum, g5_sum, g7_sum, o_cnt, g4_cnt, g5_cnt, g7_cnt = value

	if o_cnt > 0:
		o_avg = o_sum/o_cnt
	else:
		o_avg = 0

	if g4_cnt > 0:
		g4_avg = g4_sum/g4_cnt
	else:
		g4_avg = 0

	if g5_cnt > 0:
		g5_avg = g5_sum/g5_cnt
	else:
		g5_avg = 0

	if g7_cnt > 0:
		g7_avg = g7_sum/g7_cnt
	else:
		g7_avg = 0

	firm_year_innovation.writerow([firm, year, o_avg, g4_avg, g5_avg, g7_avg])


# END OF PROCESS ##
print('\nEND OF PROCESS\n')

end_time = time.ctime()

print('Start Time: ' + start_time)
print('End Time: ' + end_time + '\n')

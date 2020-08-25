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
og_file = open('dependent_data/originality_generality.csv', encoding='utf-8-sig')
og = csv.DictReader(og_file, delimiter=",")

# load in the firm year patent file
firm_year_patentcnt_file = open('dependent_data/firm_year_patentcnt.csv', encoding='utf-8-sig')
firm_year_patentcnt = csv.DictReader(firm_year_patentcnt_file, delimiter=",")

# create an output file (firm year patent cnt)
output = open('outputs/firm_year_innovation.csv', 'w', newline="\n", encoding='utf-8-sig')
firm_year_innovation = csv.writer(output, delimiter=',')
header = ['ipo_firm', 'year', 'originality', 'generality']
firm_year_innovation.writerow(header)

# create a dictionary of ipo_firms (firm, year) -> (originality_sum, generality_sum, cnt)
innovation_dict = {}

# find all the potential firm years
print('CALCULATING ALL POTENTIAL FIRM YEAR\n')
for row in firm_year_patentcnt:
	firm = row['ipo_firm']
	year = row['year']
	firm_year = (firm, year)
	innovation_dict[firm_year] = (0, 0, 0, 0)

print('AGGREGATING ORIGINALITY AND GENERALITY SCORES\n')
for row in og:
	firm = row['ipo_firm']
	year = row['year']
	originality = row['originality']
	generality = row['generality']

	firm_year = (firm, year)

	if firm_year in innovation_dict:
		originality_sum, generality_sum, o_cnt, g_cnt = innovation_dict[firm_year]
		if not originality == 'N/A':
			originality_sum += float(originality)
			o_cnt += 1
		if not generality == 'N/A':
			generality_sum += float(generality)
			g_cnt += 1
		innovation_dict[firm_year] = (originality_sum, generality_sum, o_cnt, g_cnt)
	else:
		print('ERROR FIRM YEAR NOT FOUND!!')
		break
		# if originality == 'N/A' and originality == 'N/A':
		# 	innovation_dict[firm_year] = (0, 0, 0, 0)
		# elif originality == 'N/A':
		# 	innovation_dict[firm_year] = (0, float(generality), 0, 1)
		# elif generality == 'N/A':
		# 	innovation_dict[firm_year] = (float(originality), 0, 1, 0)
		# else:
		# 	innovation_dict[firm_year] = (float(originality), float(generality), 1, 1)

for key, value in innovation_dict.items():
	firm, year = key
	originality_sum, generality_sum, o_cnt, g_cnt = value

	if o_cnt > 0:
		o_avg = originality_sum/o_cnt
	else:
		o_avg = 0

	if g_cnt > 0:
		g_avg = generality_sum/g_cnt
	else:
		g_avg = 0

	firm_year_innovation.writerow([firm, year, o_avg, g_avg])


# END OF PROCESS ##
print('\nEND OF PROCESS\n')

end_time = time.ctime()

print('Start Time: ' + start_time)
print('End Time: ' + end_time + '\n')

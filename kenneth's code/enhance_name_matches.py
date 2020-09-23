########################################################################################################################
# Enhance Name Matches
#
# Kenneth Shinn
# kshinn@seas.upenn.edu
#
# Directions: put the assignee firms and names matches in a folder 'dependent data'.
# Creates a new file call "name_matches_2.csv"
#
########################################################################################################################

import csv
import math
import time

# start time
start_time = time.ctime()

# load in the assignee file
assignee_file = open('dependent_data/assignee_firms.tsv', encoding='utf-8-sig')
assignee = csv.DictReader(assignee_file, delimiter="\t")

# load in the name matches file
name_matches_file = open('dependent_data/name_matches.csv', encoding='utf-8-sig')
name_matches = csv.reader(name_matches_file, delimiter=",")

# create an output file (enhanced name matches)
output = open('outputs/name_matches_2.csv', 'w', newline="\n", encoding='utf-8-sig')
name_matches_2 = csv.writer(output, delimiter=',')
header = ['ipo_firm', 'assignee_firm', 'ticker', 'is_common', 'patent_cnt', 'assignee_id']
name_matches_2.writerow(header)

firm_to_id_dict = {}
for row in assignee:
	firm = row['firm'].strip()
	assignee_id = row['id'].strip()
	firm_to_id_dict[firm] = assignee_id

print(len(firm_to_id_dict))

skip_header = True
for row in name_matches:
	if skip_header:
		skip_header = False
		continue

	assignee_firm = row[1].strip()
	assignee_id = firm_to_id_dict[assignee_firm]
	row.append(assignee_id)
	name_matches_2.writerow(row)


# END OF PROCESS ##
print('\nEND OF PROCESS\n')

end_time = time.ctime()

print('Start Time: ' + start_time)
print('End Time: ' + end_time)

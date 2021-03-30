import csv

# Load name_matches
name_matches_file = open('../outputs/name_matches.csv', 
                      encoding='utf-8-sig')
name_matches = csv.DictReader(name_matches_file, delimiter=',')

# Create assignee id to ipo firm dict
print('Creating assignee_id to ipo name dict\n...')
ipo_name_to_name = {}
for row in name_matches:
    ipo_name_to_name[row['assignee_firm']] = row['ipo_firm']

# Load assignee_firms
assignee_firms_file = open('../patent_data/assignee.tsv', 
                      encoding='utf-8-sig')
assignee_firms = csv.DictReader(assignee_firms_file, delimiter='\t') 

total = 0
name_match = 0

# Create assignee id to firm name dict
print('Testing assignee_id, organization\n...')
for row in assignee_firms:
    if row['organization'] in ipo_name_to_name:
        name_match += 1
    if row['organization']:
        total += 1

print("Name match", name_match)
print("Total orgs", total)
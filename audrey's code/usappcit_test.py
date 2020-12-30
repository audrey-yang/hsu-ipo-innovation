import csv

# Load application
app_file = open('../patent_data/application.tsv', 
                        encoding='utf-8-sig')
application = csv.DictReader(app_file, delimiter='\t') 
    
# Create patent to year dictionary
print('Creating year dict and application to patent dict\n...')
app_to_patent = {}
for row in application:
    app_to_patent[row['number']] = row['patent_id']

# Load usapplicationcitation
usappcitation_file = open('../patent_data/usapplicationcitation.tsv', 
                                encoding='utf-8-sig')
usappcitation = csv.DictReader(usappcitation_file, delimiter='\t')

row_cnt = 0
no_match = 0
# Add application citations
print('Adding application citation\n...')
app_to_citationfw = {}
for row in usappcitation:
    if row['date']:
        cit = app_to_patent.get(row['application_id'])
        if not cit:
            no_match += 1
        row_cnt += 1

print("Row count", row_cnt)
print("No match count", no_match)
import csv

# Load inventor_patent
inventor_to_patent_file = open('../outputs/inventor_patent.csv', 
                               encoding='utf-8-sig')
inventor_to_patent = csv.DictReader(inventor_to_patent_file)

not_same = 0
total = 0

for row in inventor_to_patent:
    total += 1
    try:
        ind = row['inventor_id'].index('-')
        patent_num = row['inventor_id'][:ind]
        if row['patent_id'] != patent_num:
            not_same += 1
    except ValueError:
        print(row['inventor_id'], row['patent_id'])

print("Not same", not_same)
print("Total", total)
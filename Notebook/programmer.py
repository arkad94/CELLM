import csv
import json

def process_row(row):
    # Check POS value to determine which template to use
    if row['POS'] == 'REFERENCE FOUND!':
        return f"1.For {row['CAT']},{row['CComp']} Lowest Cost is found at {row['DQID']} which is {row['DPID']}- the savings are {row['DCost']} per unit for a total of {row['IMP']}."
    elif row['POS'] == 'COST REFERENCE':
        return f"1.For {row['CAT']},{row['CComp']}, this is the lowest cost at {row['LCost']}."

def create_json_object(cqid, rows):
    prompt_lines = [
        f"{i+1}.in {row['CAT']},{row['CComp']} lowest cost for this is {row['CCost']}" 
        for i, row in enumerate(rows)
    ]
    prompt = "Check the Quote for {}:\n".format(rows[0]['CPID']) + "\n".join(prompt_lines)
    
    completion_lines = [process_row(row) for row in rows]
    completion = "I have checked the quote for {} and the results are as follows:\n".format(rows[0]['CPID']) + "\n".join(completion_lines)
    
    return {
        "prompt": prompt,
        "completion": completion
    }

def process_csv(file_path, max_quotes):
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        data = list(reader)
    
    # Organize rows by CQID
    cqid_groups = {}
    for row in data:
        cqid = int(row['CQID'])
        if cqid <= max_quotes:
            if cqid not in cqid_groups:
                cqid_groups[cqid] = []
            cqid_groups[cqid].append(row)
    
    # Create JSON objects
    json_objects = []
    for cqid, rows in cqid_groups.items():
        json_object = create_json_object(cqid, rows)
        json_objects.append(json_object)
    
    # Save to file
    with open('output.json', 'w', encoding='utf-8') as json_file:
        json.dump(json_objects, json_file, indent=4)

if __name__ == "__main__":
    file_path = input("Enter the path to the CSV file: ")
    max_quotes = int(input("Enter the maximum number of quotes to process: "))
    process_csv(file_path, max_quotes)

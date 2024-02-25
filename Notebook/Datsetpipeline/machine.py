import csv

# Define the input and output file names
input_file = '/Users/arkad94/Wonder/Cellm/Notebook/Datsetpipeline/c.csv'  # Replace with your actual input file name
output_file = 'e.csv'

# Function to process each row
def process_row(row):
    try:
        # Multiply the value in column 16 (index 15) by 1,000,000
        row[15] = str(float(row[15]) * 1000000)
    except ValueError:
        # Handle the case where the conversion to float fails (e.g., header or invalid data)
        pass
    return row

# Read the input CSV, process each row, and write to the output CSV
with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
     open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        processed_row = process_row(row)
        writer.writerow(processed_row)

print(f"File processed. Output saved to '{output_file}'")

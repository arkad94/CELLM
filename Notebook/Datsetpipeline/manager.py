import csv
import random

def find_min_max_per_column(file_path):
    min_max_values = {}
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            for i, value in enumerate(row):
                if i > 0 and value.replace('.', '', 1).isdigit():  # Numeric values from 2nd column onwards
                    value = float(value)
                    if i in min_max_values:
                        min_max_values[i] = (min(min_max_values[i][0], value), max(min_max_values[i][1], value))
                    else:
                        min_max_values[i] = (value, value)
    return min_max_values

def randomize_data(file_path, min_max_values):
    randomized_data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i > 0:  # Skip header row
                for j in range(1, len(row)):  # Start from 2nd column
                    if j in min_max_values and row[j].replace('.', '', 1).isdigit():
                        min_val, max_val = min_max_values[j]
                        row[j] = str(round(random.uniform(min_val, max_val), 2))  # Randomize within range
            randomized_data.append(row)
    return randomized_data

def save_randomized_data(randomized_data, output_file_path):
    with open(output_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(randomized_data)

input_file_path = 'Notebook/Datsetpipeline/a.csv'  # Replace with your actual file path
output_file_path = 'randomized_output.csv'

min_max_values = find_min_max_per_column(input_file_path)
randomized_data = randomize_data(input_file_path, min_max_values)
save_randomized_data(randomized_data, output_file_path)

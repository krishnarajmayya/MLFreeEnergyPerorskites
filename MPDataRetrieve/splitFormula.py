import csv
import re

def split_column(filename, column_index):
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        data = list(reader)

    max_splits = 0
    for row in data:
        column_data = row[column_index]
        splits = len(re.findall('[A-Z]', column_data))
        max_splits = max(max_splits, splits)

        split_values = re.findall('[A-Z][^A-Z]*', column_data)
        new_columns = [val.strip() for val in split_values if val.strip()]
        row[column_index:column_index+1] = new_columns

    header_row = data[0]
    for i in range(max_splits):
        new_column_name = f'NewColumn{i+1}'
        header_row.insert(column_index + i + 1, new_column_name)

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

# Usage example
csv_file = 'input.csv'
column_index_to_split = 11

split_column(csv_file, column_index_to_split)
print('CSV file updated successfully!')


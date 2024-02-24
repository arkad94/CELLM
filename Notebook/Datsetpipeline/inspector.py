import pandas as pd

# Load the CSV files
a_df = pd.read_csv('/Users/arkad94/Wonder/Cellm/Notebook/Datsetpipeline/a.csv')
b_df = pd.read_csv('/Users/arkad94/Wonder/Cellm/Notebook/Datsetpipeline/b.csv')

# Function to find the lowest price for a component in b_df
def find_lowest_price(quote_id, column_index, component_name):
    component_values = b_df[b_df.iloc[:, column_index] == component_name]
    if not component_values.empty:
        lowest_price_row = component_values.iloc[:, column_index + 1].idxmin()
        lowest_price = component_values.at[lowest_price_row, component_values.columns[column_index + 1]]
        lowest_quote_id = component_values.at[lowest_price_row, 'Quote ID']
        return f"For Quote ID {quote_id:03d}, {product_name} the lowest possible value is at Quote ID {lowest_quote_id:03d} value at column {column_index + 1} for quote ID {lowest_quote_id:03d} and value at column {column_index + 2} for quote ID {lowest_quote_id:03d}"
    else:
        return f"No matches found in b.csv for Quote ID {quote_id:03d}, {product_name}"

# Ask for the maximum quote ID to process
max_quote_id = int(input("Enter the maximum quote ID (up to 999): "))
max_quote_id = min(max_quote_id, 999)  # Ensuring it doesn't exceed 999

# Processing each quote ID
for quote_id in range(1, max_quote_id + 1):
    if quote_id in a_df['Quote ID'].values:
        row = a_df[a_df['Quote ID'] == quote_id]
        product_name = row.iloc[0]['Product']

        # Process for columns 5, 19, 21
        results = []
        for col in [5, 19, 21]:
            component_name = row.iloc[0, col]
            result = find_lowest_price(quote_id, col, component_name)
            results.append(result)

        # Print results for each component
        for result in results:
            print(result)

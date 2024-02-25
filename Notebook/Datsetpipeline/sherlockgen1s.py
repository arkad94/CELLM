import pandas as pd

# Function to find the lowest cost for a component in the quotes
def find_lowest_cost(a_df, b_df, quote_id, a_col_index, b_col_index):
    try:
        # Selecting the row where 'Quote ID' matches the given quote_id
        a_row = a_df[a_df['Quote ID'] == quote_id]
        
        # Check if the row is not empty and the column index is within range
        if not a_row.empty and a_row.shape[1] > a_col_index:
            # Retrieve component name for the current quote ID
            component_name = a_row.iloc[0, a_col_index]
            # Find all rows in b_df where the component name matches
            matching_rows = b_df[b_df.iloc[:, a_col_index] == component_name]

            # Check if matching rows exist and column index is in range
            if not matching_rows.empty and matching_rows.shape[1] > b_col_index:
                # Find the index of the row with the lowest cost
                lowest_cost_row = matching_rows.iloc[:, b_col_index].idxmin()
                # Get the quote ID of the lowest cost row
                lowest_cost_quote_id = matching_rows.at[lowest_cost_row, 'Quote ID']

                # Handling self-reference by comparing quote IDs
                if lowest_cost_quote_id == quote_id:
                    lcost = '[self reference]'
                else:
                    # Retrieve the lowest cost if not a self-reference
                    lcost = matching_rows.at[lowest_cost_row, matching_rows.columns[b_col_index]]

                # Returning a dictionary of the processed data
                return {
                    'CQID': quote_id,
                    'CPID': a_row.iloc[0]['Product'],
                    'CComp': component_name,
                    'LCost': lcost,
                    'DQID': lowest_cost_quote_id,
                    'DPID': matching_rows.at[lowest_cost_row, 'Product']
                }
        return None
    except Exception as e:
        # Error handling for exceptions during processing
        print(f"Error processing Quote ID {quote_id} for component at index {a_col_index}: {e}")
        return None

# Function to process all quotes and compile the output data
def process_quotes(a_df, b_df, max_quote_id):
    output_data = []
    # Iterating over each quote ID
    for quote_id in range(1, max_quote_id + 1):
        # Check if the quote ID exists in the DataFrame
        if quote_id in a_df['Quote ID'].values:
            # Iterating over specified column pairs
            for col_pair in [(4, 5), (18, 19), (20, 21)]:
                # Using the find_lowest_cost function for each column pair
                result = find_lowest_cost(a_df, b_df, quote_id, col_pair[0], col_pair[1])
                if result:
                    # Appending the result to the output data
                    output_data.append(result)
    return output_data

# Load the CSV files
a_df = pd.read_csv('/Users/arkad94/Wonder/Cellm/Notebook/Datsetpipeline/c.csv')
b_df = pd.read_csv('/Users/arkad94/Wonder/Cellm/Notebook/Datsetpipeline/c.csv')

# Ask for the maximum quote ID to process
max_quote_id = int(input("Enter the maximum quote ID (up to 999): "))
max_quote_id = min(max_quote_id, 999)

# Process quotes and compile the output data
output_data = process_quotes(a_df, b_df, max_quote_id)

# Convert output data to DataFrame and save to CSV
output_df = pd.DataFrame(output_data)
output_df.to_csv('output.csv', index=False)

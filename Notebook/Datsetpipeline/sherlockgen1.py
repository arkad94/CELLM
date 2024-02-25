import pandas as pd

def find_lowest_cost(a_df, b_df, quote_id, a_col_index, b_col_index):
    try:
        a_row = a_df[a_df['Quote ID'] == quote_id]
        if not a_row.empty and a_row.shape[1] > a_col_index:
            component_name = a_row.iloc[0, a_col_index]
            matching_rows = b_df[b_df.iloc[:, a_col_index] == component_name]

            if not matching_rows.empty and matching_rows.shape[1] > b_col_index:
                # Find the row with the lowest cost
                lowest_cost_row = matching_rows.iloc[:, b_col_index].idxmin()
                lowest_cost_quote_id = matching_rows.at[lowest_cost_row, 'Quote ID']

                # Check for self-reference
                if lowest_cost_quote_id == quote_id:
                    lcost = '[self reference]'
                else:
                    lcost = matching_rows.at[lowest_cost_row, matching_rows.columns[b_col_index]]

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
        print(f"Error processing Quote ID {quote_id} for component at index {a_col_index}: {e}")
        return None

def process_quotes(a_df, b_df, max_quote_id):
    output_data = []
    for quote_id in range(1, max_quote_id + 1):
        if quote_id in a_df['Quote ID'].values:
            for col_pair in [(4, 5), (18, 19), (20, 21)]:
                result = find_lowest_cost(a_df, b_df, quote_id, col_pair[0], col_pair[1])
                if result:
                    output_data.append(result)
    return output_data

# Load the CSV files
a_df = pd.read_csv('/Users/arkad94/Wonder/Cellm/Notebook/Datsetpipeline/c.csv')
b_df = pd.read_csv('/Users/arkad94/Wonder/Cellm/Notebook/Datsetpipeline/d.csv')

# Ask for the maximum quote ID to process
max_quote_id = int(input("Enter the maximum quote ID (up to 999): "))
max_quote_id = min(max_quote_id, 999)

# Process quotes and get output data
output_data = process_quotes(a_df, b_df, max_quote_id)

# Convert output data to DataFrame and save to CSV
output_df = pd.DataFrame(output_data)
output_df.to_csv('output.csv', index=False)

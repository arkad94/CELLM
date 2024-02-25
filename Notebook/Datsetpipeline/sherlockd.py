import pandas as pd

def find_lowest_cost(a_df, b_df, quote_id, a_col_index, b_col_index):
    try:
        print(f"Processing Quote ID {quote_id}, column pair ({a_col_index}, {b_col_index})")
        if a_col_index >= len(a_df.columns) or b_col_index >= len(b_df.columns):
            raise ValueError(f"Column index out of range: a_col_index={a_col_index}, b_col_index={b_col_index}")

        a_row = a_df[a_df['Quote ID'] == quote_id]
        if a_row.empty:
            raise ValueError(f"No matching row for Quote ID {quote_id} in a_df")

        component_name = a_row.iloc[0, a_col_index]
        matching_rows = b_df[b_df.iloc[:, a_col_index] == component_name]

        if matching_rows.empty:
            raise ValueError(f"No matching rows for component '{component_name}' in b_df")

        matching_rows_excluding_self = matching_rows[matching_rows['Quote ID'] != quote_id]
        if matching_rows_excluding_self.empty:
            print(f"All matches are self-references for Quote ID {quote_id}, component '{component_name}'")
            return {
                'CQID': quote_id,
                'CPID': a_row.iloc[0]['Product'],
                'CComp': component_name,
                'LCost': '[self reference]',
                'DQID': quote_id,
                'DPID': a_row.iloc[0]['Product']
            }

        lowest_cost_row_idx = matching_rows_excluding_self[b_col_index].idxmin()
        lowest_cost_row = matching_rows_excluding_self.loc[lowest_cost_row_idx]

        return {
            'CQID': quote_id,
            'CPID': a_row.iloc[0]['Product'],
            'CComp': component_name,
            'LCost': lowest_cost_row[b_col_index],
            'DQID': lowest_cost_row['Quote ID'],
            'DPID': lowest_cost_row['Product']
        }
    except Exception as e:
        print(f"Error processing Quote ID {quote_id}: {e}")
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
output_df.to_csv('outputd.csv', index=False)

import pandas as pd

def find_lowest_cost(a_df, b_df, quote_id, a_col_index, b_col_index, c_cost_col, category, q_col):
    try:
        a_row = a_df[a_df['Quote ID'] == quote_id]
        if not a_row.empty and a_row.shape[1] > a_col_index:
            component_name = a_row.iloc[0, a_col_index]
            c_cost = a_row.iloc[0, c_cost_col]
            q_value = a_row.iloc[0, q_col]  # Retrieve quantity from column 16
            cpid = a_row.iloc[0]['Product']
            matching_rows = b_df[b_df.iloc[:, a_col_index] == component_name]

            # Determine product type (pType) based on CPID value
            if 'TPS' in cpid:
                pType = 'TPS'
            elif 'O2-Sensor' in cpid:
                pType = 'O2-Sensor'
            elif 'ECU' in cpid:
                pType = 'ECU'
            else:
                pType = 'Other'

            if not matching_rows.empty and matching_rows.shape[1] > b_col_index:
                lowest_cost_row = matching_rows.iloc[:, b_col_index].idxmin()
                lowest_cost_quote_id = matching_rows.at[lowest_cost_row, 'Quote ID']

                if lowest_cost_quote_id == quote_id:
                    lcost = c_cost  # Use CCost as LCost for self-references
                    pos = "COST REFERENCE"
                else:
                    lcost = matching_rows.at[lowest_cost_row, matching_rows.columns[b_col_index]]
                    pos = "REFERENCE FOUND!"

                dcost = round(c_cost - lcost, 3)  # Calculate and round off DCost
                imp = round(q_value * dcost, 3)   # Calculate IMP

                return {
                    'CQID': quote_id,
                    'pType': pType,
                    'CAT': category,
                    'CPID': cpid,
                    'CComp': component_name,
                    'CCost': c_cost,
                    'LCost': lcost,
                    'DCost': dcost,
                    'DQID': lowest_cost_quote_id,
                    'DPID': matching_rows.at[lowest_cost_row, 'Product'],
                    '[Q]': q_value,
                    'IMP': imp,
                    'POS': pos
                }
        return None
    except Exception as e:
        print(f"Error processing Quote ID {quote_id} for component at index {a_col_index}: {e}")
        return None

def process_quotes(a_df, b_df, max_quote_id):
    output_data = []
    category = "Electronic Component"  # Current category for all components
    q_col = 15  # Column index for quantity in a_df
    for quote_id in range(1, max_quote_id + 1):
        if quote_id in a_df['Quote ID'].values:
            # Define column pairs with corresponding CCost column index
            col_pairs = [(4, 5, 5), (18, 19, 19), (20, 21, 21)]
            for col_pair in col_pairs:
                result = find_lowest_cost(a_df, b_df, quote_id, col_pair[0], col_pair[1], col_pair[2], category, q_col)
                if result:
                    output_data.append(result)
    return output_data

# Load the CSV files
a_df = pd.read_csv('/Users/arkad94/Wonder/Cellm/Notebook/Datsetpipeline/e.csv')
b_df = pd.read_csv('/Users/arkad94/Wonder/Cellm/Notebook/Datsetpipeline/f.csv')

# Ask for the maximum quote ID to process
max_quote_id = int(input("Enter the maximum quote ID (up to 999): "))
max_quote_id = min(max_quote_id, 999)

# Process quotes and get output data
output_data = process_quotes(a_df, b_df, max_quote_id)

# Convert output data to DataFrame and save to CSV
output_df = pd.DataFrame(output_data)
output_df.to_csv('outputnew.csv', index=False)

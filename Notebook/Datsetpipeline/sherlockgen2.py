import pandas as pd

def create_lowest_cost_map(b_df):
    lowest_cost_map = {}
    electronic_indices = [4, 18, 20]
    mechanical_indices = [6, 22, 24]
    for index, row in b_df.iterrows():
        for col_index in electronic_indices + mechanical_indices:
            component = row.iloc[col_index]
            cost = row.iloc[col_index + 1]
            if pd.notna(component):
                if component not in lowest_cost_map or cost < lowest_cost_map[component][0]:
                    lowest_cost_map[component] = (cost, row['Quote ID'], row['Product'])
    return lowest_cost_map


def find_lowest_cost(a_row, lowest_cost_map, col_index, category, q_col):
    component_name = a_row.iloc[col_index]
    c_cost = a_row.iloc[col_index + 1]
    q_value = a_row[q_col]
    cpid = a_row['Product']
    pType = 'TPS' if 'TPS' in cpid else 'O2-Sensor' if 'O2-Sensor' in cpid else 'ECU' if 'ECU' in cpid else 'Other'

    lcost, dqid, dpid = lowest_cost_map.get(component_name, (c_cost, a_row['Quote ID'], cpid))
    pos = "REFERENCE FOUND!" if lcost < c_cost else "COST REFERENCE"
    dcost = round(c_cost - lcost, 2)
    imp = round(q_value * dcost, 2)

    return {
        'CQID': a_row['Quote ID'],
        'pType': pType,
        'CAT': category,
        'CPID': cpid,
        'CComp': component_name,
        'CCost': c_cost,
        'LCost': lcost,
        'DCost': dcost,
        'DQID': dqid,
        'DPID': dpid,
        '[Q]': q_value,
        'IMP': imp,
        'POS': pos
    }

def process_quotes(a_df, b_df, max_quote_id):
    output_data = []
    electronic_indices = [4, 18, 20]
    mechanical_indices = [6, 22, 24]
    q_col = 'Quantity'

    lowest_cost_map = create_lowest_cost_map(b_df)

    for quote_id in range(1, max_quote_id + 1):
        quote_rows = a_df[a_df['Quote ID'] == quote_id]
        for _, a_row in quote_rows.iterrows():
            for col_index in electronic_indices:
                if pd.notna(a_row.iloc[col_index]):
                    result = find_lowest_cost(a_row, lowest_cost_map, col_index, "Electronic Component", q_col)
                    output_data.append(result)
            for col_index in mechanical_indices:
                if pd.notna(a_row.iloc[col_index]):
                    result = find_lowest_cost(a_row, lowest_cost_map, col_index, "Mechanical Components", q_col)
                    output_data.append(result)

    return output_data

# Load CSV files
a_df = pd.read_csv('/Users/arkad94/Wonder/Cellm/Notebook/Datsetpipeline/e.csv')
b_df = pd.read_csv('/Users/arkad94/Wonder/Cellm/Notebook/Datsetpipeline/f.csv')

# Get maximum quote ID
max_quote_id = int(input("Enter the maximum quote ID (up to 999): "))
max_quote_id = min(max_quote_id, 999)

# Process quotes and get output data
output_data = process_quotes(a_df, b_df, max_quote_id)

# Convert to DataFrame and save to CSV
output_df = pd.DataFrame(output_data)
output_df.to_csv('outputy.csv', index=False)

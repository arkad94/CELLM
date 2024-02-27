import pandas as pd

def create_lowest_cost_map(b_df):
    # Create a dictionary to store the lowest cost information for each component
    lowest_cost_map = {}
    electronic_indices = [4, 18, 20]  # Indices of electronic components in the dataframe
    mechanical_indices = [6, 22, 24]  # Indices of mechanical components in the dataframe

    # Iterate over each row in the dataframe
    for index, row in b_df.iterrows():
        # Check both electronic and mechanical components
        for col_index in electronic_indices + mechanical_indices:
            component = row.iloc[col_index]
            cost = row.iloc[col_index + 1]
            # If the component exists and is cheaper than the current known cost, update the map
            if pd.notna(component):
                if component not in lowest_cost_map or cost < lowest_cost_map[component][0]:
                    lowest_cost_map[component] = (cost, row['Quote ID'], row['Product'])
    return lowest_cost_map

def find_lowest_cost(a_row, lowest_cost_map, col_index, category, q_col):
    # Extract component details from the row
    component_name = a_row.iloc[col_index]
    c_cost = a_row.iloc[col_index + 1]
    q_value = a_row[q_col]
    cpid = a_row['Product']
    
    # Determine the product type based on the product ID
    pType = 'TPS' if 'TPS' in cpid else 'O2-Sensor' if 'O2-Sensor' in cpid else 'ECU' if 'ECU' in cpid else 'Other'

    # Get the lowest cost from the map, or use the current cost if not found
    lcost, dqid, dpid = lowest_cost_map.get(component_name, (c_cost, a_row['Quote ID'], cpid))

    # Determine position/status of the component based on cost comparison
    pos = "REFERENCE FOUND!" if lcost < c_cost else "COST REFERENCE"
    dcost = round(c_cost - lcost, 2)
    imp = round(q_value * dcost, 2)  # Calculate the impact

    # Return the findings as a dictionary
    return {
        # Various details about the quote and component
    }

def process_quotes(a_df, b_df, max_quote_id):
    output_data = []
    electronic_indices = [4, 18, 20]  # Indices for electronic components
    mechanical_indices = [6, 22, 24]  # Indices for mechanical components
    q_col = 'Quantity'  # Column name for quantity

    # Create a map of the lowest cost for each component
    lowest_cost_map = create_lowest_cost_map(b_df)

    # Process each quote up to the maximum specified quote ID
    for quote_id in range(1, max_quote_id + 1):
        quote_rows = a_df[a_df['Quote ID'] == quote_id]
        for _, a_row in quote_rows.iterrows():
            # Process each component in the quote
            for col_index in electronic_indices + mechanical_indices:
                if pd.notna(a_row.iloc[col_index]):
                    result = find_lowest_cost(a_row, lowest_cost_map, col_index, "Electronic Component", q_col)
                    output_data.append(result)

    return output_data

# Load CSV files
a_df = pd.read_csv('/workspaces/CELLM/Notebook/Datsetpipeline/e.csv')
b_df = pd.read_csv('/workspaces/CELLM/Notebook/Datsetpipeline/f.csv')

# Get maximum quote ID
max_quote_id = int(input("Enter the maximum quote ID (up to 999): "))
max_quote_id = min(max_quote_id, 999)

# Process quotes and get output data
output_data = process_quotes(a_df, b_df, max_quote_id)

# Convert to DataFrame and save to CSV
output_df = pd.DataFrame(output_data)
output_df.to_csv('outputr.csv', index=False)

##Explanation and Preprocessing Impact:
##Preprocessing: The script starts by creating a map (lowest_cost_map) of the lowest known cost for each component. This is crucial as it establishes a baseline for cost comparison. By preprocessing this data, we ensure that each component's lowest cost is consistently used throughout the analysis.
##Cost Comparison: In find_lowest_cost, the script compares the cost of each component in the current quote with its lowest known cost. This comparison is made possible and consistent due to the preprocessing step.
##Data Aggregation: By iterating over all quotes and components, the script aggregates data, including the cost difference (DCost), which is the difference between the current cost and the lowest known cost. This aggregated data provides a comprehensive view of cost variations across quotes.
##Impact Calculation: The script also calculates the impact (IMP), which is a product of the quantity and the cost difference. This gives an idea of how significant the cost difference is in terms of the total impact on the quote.
##Output Generation: Finally, the script generates a detailed output for each component in each quote, capturing various data points like current cost, lowest cost, cost difference, and impact. This output is then saved to a new CSV file (outputy.csv).
##By preprocessing the data to establish the lowest cost for each component, the script ensures that the cost comparison is based on consistent and accurate data, leading to reliable and meaningful output.
#Use this script when using github codespaces
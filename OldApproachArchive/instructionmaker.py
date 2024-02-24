import pandas as pd

# Load your dataset
data = pd.read_csv('/Users/arkad94/Wonder/Cellm/CELLM/Datasets/synthdataset.csv')

# Function to create the combined instructional format
def create_instruction(row):
    # Initial instruction for detailed cost breakdown
    instruction = f"<s> [INST] Analyze the supplier quote for Quote ID {row['Quote ID']}. Detail the costs and components. [/INST] "
    response = f"For Quote ID {row['Quote ID']} from {row['Supplier']} for {row['Product']}, the costs are as follows: "

    # Extracting and formatting component details
    components = [
        f"{row['Electronic Component 1 Name']} costs {row['Electronic Component 1 Cost']}",
        f"{row['Mechanical Component 1 Name']} costs {row['Mechanical Component 1 Cost']}",
        f"{row['Raw Material 1 Name']} costs {row['Raw Material 1 Cost']}",
        f"{row['Conversion Cost 1 Type']} ({row['Conversion Cost 1 Detail']}) costs {row['Conversion Cost 1 Cost']}",
        f"{row['Electronic Component 2 Name']} costs {row['Electronic Component 2 Cost']}",
        f"{row['Electronic Component 3 Name']} costs {row['Electronic Component 3 Cost']}",
        f"{row['Mechanical Component 2 Name']} costs {row['Mechanical Component 2 Cost']}",
        f"{row['Mechanical Component 3 Name']} costs {row['Mechanical Component 3 Cost']}",
        f"{row['Raw Material 2 Name']} costs {row['Raw Material 2 Cost']}",
        f"{row['Conversion Cost 2 Type']} ({row['Conversion Cost 2 Detail']}) costs {row['Conversion Cost 2 Cost']}",
        f"{row['Conversion Cost 3 Type']} ({row['Conversion Cost 3 Detail']}) costs {row['Conversion Cost 3 Cost']}",
        f"{row['Quality Control 1 Type']} ({row['Quality Control 1 Detail']}) costs {row['Quality Control 1 Cost']}",
        f"{row['Quality Control 2 Type']} ({row['Quality Control 2 Detail']}) costs {row['Quality Control 2 Cost']}"
    ]
    response += ", ".join(components)
    response += f". Logistic choice is {row['Logistic Choice']} with an estimated delivery cost of {row['Estimated Delivery Cost']}. "
    response += f"The total cost per unit is {row['Total Cost per Unit']}, the quantity is {row['Quantity']}, and the total project cost is {row['Total Project Cost']}."

    # Additional instruction for cost-effectiveness evaluation
    response += f" </s> [INST] Now, evaluate the cost-effectiveness of the electronic components used in this quote compared to similar components in other quotes. [/INST]"

    return instruction + response

# Apply the function to each row
data['instruction'] = data.apply(create_instruction, axis=1)

# Save to a new file
data['instruction'].to_csv('converted_dataset.csv', index=False)

import pandas as pd
from transformers import AutoTokenizer

# Load your dataset
data = pd.read_csv('/workspaces/CELLM/Datasets/synthdataset.csv')

# Initialize your tokenizer here
tokenizer = AutoTokenizer.from_pretrained('mistralai/Mixtral-8x7B-Instruct-v0.1')

def tokenize(text):
    return tokenizer.encode(text, add_special_tokens=False)

def create_instruction(row, tokenized=False):
    # Building the instruction and response text
    instruction_text = f"[INST] Analyze the supplier quote for Quote ID {row['Quote ID']}. Detail the costs and components. [/INST]"

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
    component_details = ", ".join(components)
    response_text = f"For Quote ID {row['Quote ID']} from {row['Supplier']} for {row['Product']}, the costs are as follows: {component_details}. Logistic choice is {row['Logistic Choice']} with an estimated delivery cost of {row['Estimated Delivery Cost']}. The total cost per unit is {row['Total Cost per Unit']}, the quantity is {row['Quantity']}, and the total project cost is {row['Total Project Cost']}."

    # Additional instruction for cost-effectiveness evaluation
    final_text = instruction_text + " " + response_text + " </s> [INST] Now, evaluate the cost-effectiveness of the electronic components used in this quote compared to similar components in other quotes. [/INST]"

    if tokenized:
        # Tokenize and concatenate
        tokens = tokenize(final_text)
        return ' '.join(map(str, tokens))
    else:
        return final_text

# User choice for tokenization
tokenize_choice = input("Do you want a tokenized version? (Y/N): ").strip().upper() == 'Y'

# Apply the function to each row based on user choice
data['instruction'] = data.apply(lambda row: create_instruction(row, tokenized=tokenize_choice), axis=1)

# Create a new DataFrame with only the 'instruction' column
instructions_only = data[['instruction']]

# Save the new DataFrame to a file
instructions_only.to_csv('converted_dataset_with_instructions.csv', index=False)

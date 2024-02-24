import pandas as pd
from transformers import AutoTokenizer

# Load your dataset
data = pd.read_csv('/Users/arkad94/Wonder/Cellm/CELLM/Datasets/synthdataset.csv')

# Initialize your tokenizer here
tokenizer = AutoTokenizer.from_pretrained('mistralai/Mixtral-8x7B-Instruct-v0.1')

def tokenize(text):
    return tokenizer.encode(text, add_special_tokens=False)

def create_tokenized_instruction(row):
    # Building the instruction and response text
    instruction_text = f"[INST] Analyze the supplier quote for Quote ID {row['Quote ID']}. Detail the costs and components. [/INST]"
    response_text = f"For Quote ID {row['Quote ID']} from {row['Supplier']} for {row['Product']}, the costs are as follows: " # Add component details here

    # Tokenize and concatenate
    tokens = tokenize(instruction_text) + tokenize(response_text)
    return ' '.join(map(str, tokens))

def create_plain_instruction(row):
    # Building the instruction and response text
    instruction_text = f"[INST] Analyze the supplier quote for Quote ID {row['Quote ID']}. Detail the costs and components. [/INST]"
    response_text = f"For Quote ID {row['Quote ID']} from {row['Supplier']} for {row['Product']}, the costs are as follows: " # Add component details here

    # Concatenate instruction and response text
    return instruction_text + " " + response_text

# Ask user for choice
choice = input("Do you want a tokenized version? (Y/N): ").strip().upper()
if choice == 'Y':
    new_data = pd.DataFrame(data.apply(create_tokenized_instruction, axis=1), columns=['instruction'])
else:
    new_data = pd.DataFrame(data.apply(create_plain_instruction, axis=1), columns=['instruction'])

# Save to a new file
new_data.to_csv('converted_dataset.csv', index=False)

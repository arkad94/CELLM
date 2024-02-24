# CELLM
"Repository with datasets for an AI prototype PoC to analyze and identify fictional references in fictitious quotations. Curated with fabricated quotes, it offers a safe foundation for AI to learn in a fictional realm."

Old approach is archived, The synthetic datasets are going to be produced with a different approach, with a different approach to generate the scripts as well. The below text will detail the approach until  I write the relevant documentation.



### Component Generation for Quotes

1. **Number of Components**: The number of components you should generate depends on the diversity and complexity you want in your quotes. For a dataset of 100 quotes covering various types of sensors and ECUs, you might want a sufficiently large component pool to ensure variability but also enough commonality for meaningful comparisons. 

   - A good starting point might be to have around 15-30 unique components per category (electronic components, mechanical components, etc.). This range should provide enough diversity for 100 quotes while ensuring overlaps for comparison.
   - Remember, the components should vary not only in type but also in associated costs, manufacturers, and other relevant details to make the comparisons informative.

### Practicality of the Idea

2. **Feasibility and Suitability**:
   - **Pros**:
     - Random pairing from two separate CSVs increases the natural variability in the dataset.
     - The approach allows for organic comparisons without falling into a fixed pattern, which is great for a proof of concept.
     - Generating the prompt dynamically based on the quotes being compared can lead to more realistic training data.

   - **Cons**:
     - It requires careful scripting to ensure the data generation and pairing logic work as intended.
     - Manual oversight might be necessary to ensure the generated comparisons are meaningful and the prompts accurately reflect the comparison task.

### Implementation Steps

- **Create a Component Bank**: Generate a list of components with variations in type, cost, and other attributes.
- **Quote Generation**: Use these components to create 100 varied quotes, ensuring commonalities for potential comparisons.
- **Random Pairing**: Develop a script to randomly pair quotes from two separate datasets for comparison.
- **Prompt and Completion Scripting**: Automate the creation of prompts based on the quotes being compared and script the completion part to reflect the comparative analysis.

### Template Structure

```json
{
    "prompt": "Compare the supplier quote for Product Name X with Product Name Y. Identify cost-effective components and potential negotiation points.\n\n### Instruction:\n[Detailed comparison instruction based on the specific quotes]\n\n",
    "completion": "[Model-generated response detailing the comparison between the two products, highlighting differences in costs, components, and suggesting negotiation points.]"
}
```

### Final Thoughts

This idea seems both practical and well-suited for creating a proof-of-concept dataset. It aligns with the goal of training a model to perform complex comparative analyses of supplier quotes, which is a nuanced task in the domain of procurement and supply chain management. 

The success of this approach will largely depend on the quality and diversity of the component bank and the logic of the scripts for generating quotes and pairing them for comparison. This method also provides the flexibility to scale and refine your dataset as needed, based on initial results and model performance.
